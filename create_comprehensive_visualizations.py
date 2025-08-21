import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Load data
all_data = pd.read_csv('complete_analysis_with_accessibility.csv')
international_data = pd.read_csv('international_opportunities_only.csv')

print("Creating comprehensive visualizations for RADARTES analysis...")

# Create figure with multiple subplots for comprehensive dashboard
fig = plt.figure(figsize=(20, 24))

# 1. SECTION 1 VISUALIZATIONS - RADARTES AS PLATFORM

# 1.1 Global Geographic Distribution
ax1 = plt.subplot(4, 2, 1)
country_counts = all_data['País'].value_counts().head(15)
bars = ax1.barh(range(len(country_counts)), country_counts.values, 
                color=sns.color_palette("viridis", len(country_counts)))
ax1.set_yticks(range(len(country_counts)))
ax1.set_yticklabels(country_counts.index)
ax1.set_xlabel('Number of Opportunities')
ax1.set_title('RADARTES Global Reach: Top 15 Countries\n534 Opportunities Across 57 Countries', 
              fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, v in enumerate(country_counts.values):
    ax1.text(v + 1, i, str(v), va='center', fontsize=9)

# 1.2 Investment by Category - Platform Perspective
ax2 = plt.subplot(4, 2, 2)
category_analysis = all_data.groupby('Categoría').agg({
    'Monto_USD': ['sum', 'count', 'mean']
}).round(2)
category_analysis.columns = ['Total_Investment', 'Count', 'Avg_Investment']
category_analysis = category_analysis.sort_values('Total_Investment', ascending=False)

# Create stacked bar showing both count and investment
bars1 = ax2.bar(category_analysis.index, category_analysis['Total_Investment']/1000000, 
                alpha=0.8, label='Total Investment (Millions USD)')
ax2_twin = ax2.twinx()
bars2 = ax2_twin.bar(category_analysis.index, category_analysis['Count'], 
                     alpha=0.6, color='orange', label='Number of Opportunities')

ax2.set_ylabel('Investment (Millions USD)', color='blue')
ax2_twin.set_ylabel('Number of Opportunities', color='orange')
ax2.set_title('Investment Landscape by Category\nDual Perspective: Volume vs. Count', 
              fontsize=12, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# 1.3 Accessibility Analysis
ax3 = plt.subplot(4, 2, 3)
accessibility = all_data['Inscripcion'].value_counts()
colors = ['#2E8B57', '#FF6B6B', '#4ECDC4']
wedges, texts, autotexts = ax3.pie(accessibility.values, labels=accessibility.index, 
                                   autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title('Accessibility: Application Fee Requirements\n81.3% Free to Apply', 
              fontsize=12, fontweight='bold')

# 1.4 Disciplinary Distribution
ax4 = plt.subplot(4, 2, 4)
discipline_counts = all_data['Disciplina Limpia'].value_counts()
bars = ax4.bar(discipline_counts.index, discipline_counts.values, 
               color=sns.color_palette("Set3", len(discipline_counts)))
ax4.set_xlabel('Artistic Discipline')
ax4.set_ylabel('Number of Opportunities')
ax4.set_title('Opportunities by Artistic Discipline\nVisual Arts Leads with 40.8%', 
              fontsize=12, fontweight='bold')
ax4.tick_params(axis='x', rotation=45)
ax4.grid(axis='y', alpha=0.3)

# Add percentage labels
total_ops = discipline_counts.sum()
for i, v in enumerate(discipline_counts.values):
    percentage = (v/total_ops)*100
    ax4.text(i, v + 5, f'{percentage:.1f}%', ha='center', fontsize=9)

# 2. SECTION 2 VISUALIZATIONS - STRATEGIC ANALYSIS

# 2.1 International vs Domestic Investment Comparison
ax5 = plt.subplot(4, 2, 5)
comparison_data = {
    'Domestic/Restricted': 35800000,  # From our analysis
    'Truly International': 12100000   # From our analysis
}
bars = ax5.bar(comparison_data.keys(), list(comparison_data.values()), 
               color=['#FF6B6B', '#2E8B57'], alpha=0.8)
ax5.set_ylabel('Investment (USD)')
ax5.set_title('Strategic Reality: Domestic vs International Investment\n74.8% vs 25.2% Split', 
              fontsize=12, fontweight='bold')
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 500000,
             f'${height/1e6:.1f}M\n({height/(sum(comparison_data.values()))*100:.1f}%)',
             ha='center', va='bottom', fontweight='bold')

# 2.2 True International Funding by Country
ax6 = plt.subplot(4, 2, 6)
international_by_country = international_data.groupby('País')['Monto_USD'].sum().sort_values(ascending=False).head(8)
bars = ax6.barh(range(len(international_by_country)), international_by_country.values, 
                color=sns.color_palette("plasma", len(international_by_country)))
ax6.set_yticks(range(len(international_by_country)))
ax6.set_yticklabels(international_by_country.index)
ax6.set_xlabel('International Investment (USD)')
ax6.set_title('True International Funding Leaders\nSpain Dominates with 88.7%', 
              fontsize=12, fontweight='bold')
ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Add percentage labels
total_intl = international_by_country.sum()
for i, v in enumerate(international_by_country.values):
    percentage = (v/total_intl)*100
    ax6.text(v + 100000, i, f'{percentage:.1f}%', va='center', fontsize=9)

# 2.3 Investment Model Analysis - International Focus
ax7 = plt.subplot(4, 2, 7)
international_categories = international_data.groupby('Categoría')['Monto_USD'].sum().sort_values(ascending=False)
colors_cat = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
bars = ax7.bar(international_categories.index, international_categories.values, 
               color=colors_cat[:len(international_categories)])
ax7.set_ylabel('Investment (USD)')
ax7.set_xlabel('Category Type')
ax7.set_title('International Investment Model\nMerit-Based Awards Dominate', 
              fontsize=12, fontweight='bold')
ax7.tick_params(axis='x', rotation=45)
ax7.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Add percentage labels
total_intl_cat = international_categories.sum()
for i, v in enumerate(international_categories.values):
    percentage = (v/total_intl_cat)*100
    ax7.text(i, v + 50000, f'{percentage:.1f}%', ha='center', fontsize=9)

# 2.4 High-Value Opportunities Distribution
ax8 = plt.subplot(4, 2, 8)
high_value = all_data[all_data['Monto_USD'] >= 1000]
high_value_by_country = high_value.groupby('País').agg({
    'Monto_USD': 'count'
}).sort_values('Monto_USD', ascending=False).head(10)

bars = ax8.bar(range(len(high_value_by_country)), high_value_by_country['Monto_USD'], 
               color=sns.color_palette("coolwarm", len(high_value_by_country)))
ax8.set_xticks(range(len(high_value_by_country)))
ax8.set_xticklabels(high_value_by_country.index, rotation=45)
ax8.set_ylabel('Number of High-Value Opportunities')
ax8.set_title('High-Value Opportunities (≥$1,000)\n203 Total Opportunities Worth $47.9M', 
              fontsize=12, fontweight='bold')
ax8.grid(axis='y', alpha=0.3)

# Add value labels
for i, v in enumerate(high_value_by_country['Monto_USD']):
    ax8.text(i, v + 1, str(v), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('comprehensive_radartes_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a summary statistics table
print("\n" + "="*60)
print("COMPREHENSIVE RADARTES ANALYSIS SUMMARY")
print("="*60)

print(f"\nSECTION 1 - PLATFORM OVERVIEW:")
print(f"Total Opportunities: {len(all_data)}")
print(f"Countries Represented: {all_data['País'].nunique()}")
print(f"Total Investment Tracked: ${all_data['Monto_USD'].sum():,.2f}")
print(f"Free Application Rate: {(all_data['Inscripcion'] == 'Sin cargo').mean()*100:.1f}%")
print(f"High-Value Opportunities (≥$1K): {len(all_data[all_data['Monto_USD'] >= 1000])} ({len(all_data[all_data['Monto_USD'] >= 1000])/len(all_data)*100:.1f}%)")

print(f"\nSECTION 2 - STRATEGIC ANALYSIS:")
print(f"Truly International Opportunities: {len(international_data)}")
print(f"International Investment: ${international_data['Monto_USD'].sum():,.2f}")
print(f"Domestic Investment: ${all_data['Monto_USD'].sum() - international_data['Monto_USD'].sum():,.2f}")
print(f"Spain's Share of International: {(international_data[international_data['País'] == 'España']['Monto_USD'].sum() / international_data['Monto_USD'].sum())*100:.1f}%")

print(f"\nTOP INTERNATIONAL FUNDERS:")
top_international = international_data.groupby('País')['Monto_USD'].sum().sort_values(ascending=False).head(5)
for country, investment in top_international.items():
    percentage = (investment / international_data['Monto_USD'].sum()) * 100
    print(f"  {country}: ${investment:,.2f} ({percentage:.1f}%)")

print(f"\nDISCIPLINARY BREAKDOWN:")
discipline_breakdown = all_data['Disciplina Limpia'].value_counts()
for discipline, count in discipline_breakdown.items():
    percentage = (count / len(all_data)) * 100
    print(f"  {discipline}: {count} opportunities ({percentage:.1f}%)")

print("\nVisualization saved as 'comprehensive_radartes_analysis.png'")
print("Analysis complete!") 