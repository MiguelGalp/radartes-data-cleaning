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

def create_country_investment_chart():
    """Create top countries by investment chart"""
    country_data = pd.read_csv('analysis_by_country.csv')
    top_10 = country_data.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(top_10)), top_10['Total_Investment_USD'], 
                   color='steelblue', alpha=0.8)
    
    ax.set_yticks(range(len(top_10)))
    ax.set_yticklabels(top_10['País'])
    ax.set_xlabel('Total Investment (USD)', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Countries by Total Investment\nCultural Opportunities for Latin American Artists', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                f'${width/1e6:.1f}M', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('top_countries_investment.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_category_pie_chart():
    """Create funding category distribution pie chart"""
    category_data = pd.read_csv('analysis_by_category.csv')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(category_data['Total_Investment_USD'], 
                                      labels=category_data['Categoría'],
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      explode=[0.1 if cat == 'Fondos' else 0 for cat in category_data['Categoría']])
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax.set_title('Investment Distribution by Funding Category\nTotal: $47.9M USD', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_discipline_comparison():
    """Create artistic discipline investment comparison"""
    discipline_data = pd.read_csv('analysis_by_discipline.csv')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Chart 1: Investment by discipline
    bars1 = ax1.bar(range(len(discipline_data)), discipline_data['Total_Investment_USD'], 
                    color='lightcoral', alpha=0.8)
    ax1.set_xticks(range(len(discipline_data)))
    ax1.set_xticklabels(discipline_data['Disciplina Limpia'], rotation=45, ha='right')
    ax1.set_ylabel('Total Investment (USD)', fontweight='bold')
    ax1.set_title('Investment by Artistic Discipline', fontweight='bold')
    ax1.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'${height/1e6:.1f}M', ha='center', va='bottom', fontweight='bold')
    
    # Chart 2: Number of opportunities by discipline
    bars2 = ax2.bar(range(len(discipline_data)), discipline_data['Total_Opportunities'], 
                    color='lightgreen', alpha=0.8)
    ax2.set_xticks(range(len(discipline_data)))
    ax2.set_xticklabels(discipline_data['Disciplina Limpia'], rotation=45, ha='right')
    ax2.set_ylabel('Number of Opportunities', fontweight='bold')
    ax2.set_title('Opportunities by Artistic Discipline', fontweight='bold')
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('discipline_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_accessibility_chart():
    """Create accessibility analysis chart"""
    # Calculate accessibility metrics
    abril = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-abril.csv')
    mayo = pd.read_csv('enriched_radartes-mayo.csv')
    junio = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-junio.csv')
    
    common_cols = ['Inscripcion', 'Monto_USD']
    combined = pd.concat([
        abril[common_cols],
        mayo[common_cols],
        junio[common_cols]
    ], ignore_index=True)
    
    combined['Monto_USD'] = pd.to_numeric(combined['Monto_USD'], errors='coerce').fillna(0)
    
    # Accessibility analysis
    payment_counts = combined['Inscripcion'].value_counts()
    payment_investment = combined.groupby('Inscripcion')['Monto_USD'].sum()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Chart 1: Opportunities by payment requirement
    colors = ['lightgreen', 'lightcoral']
    bars1 = ax1.bar(payment_counts.index, payment_counts.values, color=colors, alpha=0.8)
    ax1.set_ylabel('Number of Opportunities', fontweight='bold')
    ax1.set_title('Accessibility: Payment Requirements', fontweight='bold')
    
    # Add percentage labels
    total_opps = payment_counts.sum()
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        percentage = (height/total_opps)*100
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')
    
    # Chart 2: Investment by payment requirement
    bars2 = ax2.bar(payment_investment.index, payment_investment.values, color=colors, alpha=0.8)
    ax2.set_ylabel('Total Investment (USD)', fontweight='bold')
    ax2.set_title('Investment Distribution by Payment Type', fontweight='bold')
    ax2.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'${height/1e6:.1f}M', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('accessibility_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_summary_dashboard():
    """Create a summary dashboard with key metrics"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('RADARTES: Latin American Cultural Opportunities Dashboard', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Load data
    country_data = pd.read_csv('analysis_by_country.csv')
    category_data = pd.read_csv('analysis_by_category.csv')
    
    # Chart 1: Top 5 countries
    top_5_countries = country_data.head(5)
    bars1 = ax1.barh(range(len(top_5_countries)), top_5_countries['Total_Investment_USD'], 
                     color='steelblue', alpha=0.8)
    ax1.set_yticks(range(len(top_5_countries)))
    ax1.set_yticklabels(top_5_countries['País'])
    ax1.set_title('Top 5 Countries by Investment', fontweight='bold')
    ax1.xaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Chart 2: Category distribution
    wedges, texts, autotexts = ax2.pie(category_data['Total_Investment_USD'], 
                                       labels=category_data['Categoría'],
                                       autopct='%1.1f%%',
                                       startangle=90)
    ax2.set_title('Investment by Category', fontweight='bold')
    
    # Chart 3: Investment vs Opportunities scatter
    ax3.scatter(country_data['Total_Opportunities'], country_data['Total_Investment_USD'], 
                alpha=0.6, s=60, color='green')
    ax3.set_xlabel('Number of Opportunities')
    ax3.set_ylabel('Total Investment (USD)')
    ax3.set_title('Investment vs Opportunities by Country', fontweight='bold')
    ax3.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Annotate key countries
    for i, row in country_data.head(3).iterrows():
        ax3.annotate(row['País'], 
                    (row['Total_Opportunities'], row['Total_Investment_USD']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Chart 4: Key metrics text
    ax4.axis('off')
    
    # Calculate key metrics
    total_investment = country_data['Total_Investment_USD'].sum()
    total_opportunities = country_data['Total_Opportunities'].sum()
    total_countries = len(country_data)
    avg_investment = total_investment / total_opportunities
    
    metrics_text = f"""
    KEY METRICS (Apr-Jun 2025)
    
    Total Investment: ${total_investment/1e6:.1f}M USD
    Total Opportunities: {total_opportunities:,}
    Countries Involved: {total_countries}
    Average per Opportunity: ${avg_investment/1e3:.1f}K USD
    
    TOP INSIGHTS:
    • Mexico dominates with 73.5% of investment
    • 81.3% of opportunities are free to apply
    • 38% are high-value (≥$1,000 USD)
    • 57 countries offer opportunities
    """
    
    ax4.text(0.1, 0.9, metrics_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('dashboard_summary.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all visualizations"""
    print("Creating visualizations...")
    
    create_country_investment_chart()
    print("✓ Country investment chart created")
    
    create_category_pie_chart()
    print("✓ Category distribution chart created")
    
    create_discipline_comparison()
    print("✓ Discipline analysis charts created")
    
    create_accessibility_chart()
    print("✓ Accessibility analysis charts created")
    
    create_summary_dashboard()
    print("✓ Summary dashboard created")
    
    print("\nVisualization files generated:")
    print("• top_countries_investment.png")
    print("• category_distribution.png")
    print("• discipline_analysis.png")
    print("• accessibility_analysis.png")
    print("• dashboard_summary.png")
    print("\nAll charts ready for presentations and reports!")

if __name__ == "__main__":
    main() 