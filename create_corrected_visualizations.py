import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter

# Set style for professional-looking charts
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def millions_formatter(x, pos):
    """Format numbers in millions"""
    return f'${x/1e6:.1f}M'

def thousands_formatter(x, pos):
    """Format numbers in thousands"""
    return f'${x/1e3:.0f}K'

def create_corrected_charts():
    """Create corrected visualizations for international opportunities only"""
    
    # Load the corrected data
    international_only = pd.read_csv('international_opportunities_only.csv')
    
    print(f"Creating corrected visualizations for {len(international_only)} international opportunities...")
    
    # 1. Corrected Country Investment Chart
    create_corrected_country_chart(international_only)
    
    # 2. Corrected Category Chart  
    create_corrected_category_chart(international_only)
    
    # 3. Corrected vs Original Comparison
    create_comparison_chart(international_only)
    
    # 4. Corrected Geographic Distribution
    create_geographic_reality_chart(international_only)
    
    print("All corrected visualizations created!")

def create_corrected_country_chart(df):
    """Create corrected top countries chart for international opportunities"""
    
    country_stats = df.groupby('País')['Monto_USD'].agg(['count', 'sum']).sort_values('sum', ascending=False)
    top_10 = country_stats.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(top_10)), top_10['sum'], color='steelblue', alpha=0.8)
    
    ax.set_yticks(range(len(top_10)))
    ax.set_yticklabels(top_10.index)
    ax.set_xlabel('Total Investment (USD)', fontsize=12, fontweight='bold')
    ax.set_title('CORRECTED: Top 10 Countries by International Investment\nOpportunities Truly Available to Latin American Artists', 
                 fontsize=14, fontweight='bold', pad=20, color='darkred')
    
    # Format x-axis
    ax.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        if width > 1000000:
            label = f'${width/1e6:.1f}M'
        else:
            label = f'${width/1e3:.0f}K'
        ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                label, ha='left', va='center', fontweight='bold')
    
    # Add correction note
    ax.text(0.02, 0.98, 'Note: Excludes domestic government programs (PECDA, INCAA, etc.)', 
            transform=ax.transAxes, fontsize=10, va='top', 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('corrected_international_countries.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_corrected_category_chart(df):
    """Create corrected category distribution for international opportunities"""
    
    category_stats = df.groupby('Categoría')['Monto_USD'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(category_stats.values, 
                                      labels=category_stats.index,
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      explode=[0.1 if cat == 'Premio' else 0 for cat in category_stats.index])
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax.set_title('CORRECTED: International Investment by Category\nMerit-Based Model (Total: $11.96M USD)', 
                 fontsize=14, fontweight='bold', pad=20, color='darkred')
    
    # Add correction note
    fig.text(0.02, 0.02, 'Note: Excludes domestic "Fondos" programs', 
             fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('corrected_international_categories.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_comparison_chart(international_df):
    """Create before/after comparison chart"""
    
    # Load original analysis for comparison
    original_countries = pd.read_csv('analysis_by_country.csv')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Original analysis (top 5)
    orig_top5 = original_countries.head(5)
    bars1 = ax1.barh(range(len(orig_top5)), orig_top5['Total_Investment_USD'], 
                     color='lightcoral', alpha=0.8)
    ax1.set_yticks(range(len(orig_top5)))
    ax1.set_yticklabels(orig_top5['País'])
    ax1.set_title('ORIGINAL ANALYSIS\n(Including Domestic Programs)', fontweight='bold', color='red')
    ax1.set_xlabel('Investment (USD)')
    ax1.xaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Add labels
    for bar in bars1:
        width = bar.get_width()
        ax1.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
                f'${width/1e6:.1f}M', ha='left', va='center', fontweight='bold')
    
    # Corrected analysis (top 5)
    intl_countries = international_df.groupby('País')['Monto_USD'].sum().sort_values(ascending=False)
    intl_top5 = intl_countries.head(5)
    
    bars2 = ax2.barh(range(len(intl_top5)), intl_top5.values, 
                     color='steelblue', alpha=0.8)
    ax2.set_yticks(range(len(intl_top5)))
    ax2.set_yticklabels(intl_top5.index)
    ax2.set_title('CORRECTED ANALYSIS\n(International Only)', fontweight='bold', color='darkblue')
    ax2.set_xlabel('Investment (USD)')
    ax2.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
    # Add labels
    for bar in bars2:
        width = bar.get_width()
        if width > 1000000:
            label = f'${width/1e6:.1f}M'
        else:
            label = f'${width/1e3:.0f}K'
        ax2.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
                label, ha='left', va='center', fontweight='bold')
    
    plt.suptitle('CRITICAL CORRECTION: Domestic vs International Reality', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.savefig('before_after_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_geographic_reality_chart(df):
    """Create geographic reality chart showing true accessibility"""
    
    # Count opportunities and investment by region
    europe_countries = ['España', 'Francia', 'Alemania', 'Reino Unido', 'Italia', 'Austria', 'Portugal', 'Malta']
    north_america = ['EEUU', 'Canadá']
    multi_country = ['Múltiples Países']
    
    def categorize_region(country):
        if country in europe_countries:
            return 'Europe'
        elif country in north_america:
            return 'North America'
        elif country in multi_country:
            return 'Multi-Country'
        else:
            return 'Other'
    
    df['Region'] = df['País'].apply(categorize_region)
    
    region_stats = df.groupby('Region')['Monto_USD'].agg(['count', 'sum'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Investment by region
    bars1 = ax1.bar(region_stats.index, region_stats['sum'], 
                    color=['darkblue', 'lightgreen', 'orange', 'gray'], alpha=0.8)
    ax1.set_title('International Investment by Region', fontweight='bold')
    ax1.set_ylabel('Total Investment (USD)')
    ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
    # Add percentage labels
    total_investment = region_stats['sum'].sum()
    for bar in bars1:
        height = bar.get_height()
        percentage = (height/total_investment)*100
        if height > 1000000:
            label = f'${height/1e6:.1f}M\n({percentage:.1f}%)'
        else:
            label = f'${height/1e3:.0f}K\n({percentage:.1f}%)'
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                label, ha='center', va='bottom', fontweight='bold')
    
    # Opportunities by region
    bars2 = ax2.bar(region_stats.index, region_stats['count'],
                    color=['darkblue', 'lightgreen', 'orange', 'gray'], alpha=0.8)
    ax2.set_title('International Opportunities by Region', fontweight='bold')
    ax2.set_ylabel('Number of Opportunities')
    
    # Add count labels
    total_opportunities = region_stats['count'].sum()
    for bar in bars2:
        height = bar.get_height()
        percentage = (height/total_opportunities)*100
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle('Geographic Reality: European Dominance of International Opportunities', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('geographic_reality.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_corrected_charts() 