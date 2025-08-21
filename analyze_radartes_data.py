import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data():
    """Load and standardize the three datasets"""
    print("Loading datasets...")
    
    # Load datasets
    abril = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-abril.csv')
    mayo = pd.read_csv('enriched_radartes-mayo.csv')
    junio = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-junio.csv')
    
    # Standardize columns - keep only common essential columns
    common_cols = ['País', 'Categoría', 'Disciplina Limpia', 'Inscripcion', 'Monto_USD']
    
    # Add month identifier
    abril_clean = abril[common_cols].copy()
    abril_clean['Mes'] = 'Abril'
    
    mayo_clean = mayo[common_cols].copy()
    mayo_clean['Mes'] = 'Mayo'
    
    junio_clean = junio[common_cols].copy()
    junio_clean['Mes'] = 'Junio'
    
    # Combine datasets
    combined = pd.concat([abril_clean, mayo_clean, junio_clean], ignore_index=True)
    
    # Clean and standardize data
    combined['Monto_USD'] = pd.to_numeric(combined['Monto_USD'], errors='coerce')
    
    # Replace "Residencia" values with 3500 USD as specified
    combined.loc[combined['Monto_USD'].astype(str).str.contains('Residencia', case=False, na=False), 'Monto_USD'] = 3500
    
    # Handle missing values in Monto_USD
    combined['Monto_USD'] = combined['Monto_USD'].fillna(0)
    
    # Clean categories and disciplines
    combined['Categoría'] = combined['Categoría'].str.strip()
    combined['Disciplina Limpia'] = combined['Disciplina Limpia'].str.strip()
    combined['País'] = combined['País'].str.strip()
    
    return combined

def analyze_by_country(df):
    """Analyze opportunities by country"""
    print("\n=== ANALYSIS BY COUNTRY ===")
    
    country_stats = df.groupby('País').agg({
        'Monto_USD': ['count', 'sum', 'mean', 'median'],
        'Categoría': lambda x: x.value_counts().index[0] if len(x) > 0 else 'N/A'
    }).round(2)
    
    country_stats.columns = ['Total_Opportunities', 'Total_Investment_USD', 'Avg_Investment_USD', 'Median_Investment_USD', 'Top_Category']
    country_stats = country_stats.sort_values('Total_Investment_USD', ascending=False)
    
    print("Top 15 countries by total investment:")
    print(country_stats.head(15))
    
    return country_stats

def analyze_by_category(df):
    """Analyze opportunities by category (type of call)"""
    print("\n=== ANALYSIS BY CATEGORY ===")
    
    category_stats = df.groupby('Categoría').agg({
        'Monto_USD': ['count', 'sum', 'mean', 'median']
    }).round(2)
    
    category_stats.columns = ['Total_Opportunities', 'Total_Investment_USD', 'Avg_Investment_USD', 'Median_Investment_USD']
    category_stats = category_stats.sort_values('Total_Investment_USD', ascending=False)
    
    print("Investment by category type:")
    print(category_stats)
    
    return category_stats

def analyze_by_discipline(df):
    """Analyze opportunities by artistic discipline"""
    print("\n=== ANALYSIS BY ARTISTIC DISCIPLINE ===")
    
    discipline_stats = df.groupby('Disciplina Limpia').agg({
        'Monto_USD': ['count', 'sum', 'mean', 'median']
    }).round(2)
    
    discipline_stats.columns = ['Total_Opportunities', 'Total_Investment_USD', 'Avg_Investment_USD', 'Median_Investment_USD']
    discipline_stats = discipline_stats.sort_values('Total_Investment_USD', ascending=False)
    
    print("Top 15 disciplines by total investment:")
    print(discipline_stats.head(15))
    
    return discipline_stats

def analyze_payment_requirements(df):
    """Analyze payment requirements"""
    print("\n=== ANALYSIS BY PAYMENT REQUIREMENTS ===")
    
    payment_stats = df.groupby('Inscripcion').agg({
        'Monto_USD': ['count', 'sum', 'mean', 'median']
    }).round(2)
    
    payment_stats.columns = ['Total_Opportunities', 'Total_Investment_USD', 'Avg_Investment_USD', 'Median_Investment_USD']
    
    print("Investment by payment requirement:")
    print(payment_stats)
    
    return payment_stats

def analyze_significant_opportunities(df):
    """Identify most significant opportunities (>= $1000 USD)"""
    print("\n=== HIGH-VALUE OPPORTUNITIES (>= $1000 USD) ===")
    
    significant = df[df['Monto_USD'] >= 1000].copy()
    
    if len(significant) > 0:
        print(f"Total high-value opportunities: {len(significant)}")
        print(f"Total investment in high-value opportunities: ${significant['Monto_USD'].sum():,.2f} USD")
        print(f"Average value: ${significant['Monto_USD'].mean():,.2f} USD")
        
        # Top countries for high-value opportunities
        top_countries_high_value = significant.groupby('País')['Monto_USD'].agg(['count', 'sum']).sort_values('sum', ascending=False).head(10)
        print("\nTop 10 countries by high-value investment:")
        print(top_countries_high_value)
        
        # Top categories for high-value opportunities
        top_categories_high_value = significant.groupby('Categoría')['Monto_USD'].agg(['count', 'sum']).sort_values('sum', ascending=False)
        print("\nHigh-value opportunities by category:")
        print(top_categories_high_value)
        
    return significant

def create_summary_report(df, country_stats, category_stats, discipline_stats, significant):
    """Create executive summary report"""
    
    total_opportunities = len(df)
    total_investment = df['Monto_USD'].sum()
    avg_investment = df['Monto_USD'].mean()
    
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY REPORT")
    print("CULTURAL OPPORTUNITIES FOR LATIN AMERICAN ARTISTS")
    print("Analysis Period: April - June 2025")
    print("="*60)
    
    print(f"\nTOTAL METRICS:")
    print(f"• Total opportunities analyzed: {total_opportunities:,}")
    print(f"• Total estimated investment: ${total_investment:,.2f} USD")
    print(f"• Average investment per opportunity: ${avg_investment:,.2f} USD")
    
    print(f"\nGEOGRAPHIC DISTRIBUTION:")
    print(f"• Number of countries offering opportunities: {df['País'].nunique()}")
    print(f"• Top 5 countries by total investment:")
    for i, (country, row) in enumerate(country_stats.head(5).iterrows(), 1):
        print(f"  {i}. {country}: ${row['Total_Investment_USD']:,.2f} USD ({row['Total_Opportunities']} opportunities)")
    
    print(f"\nOPPORTUNITY TYPES:")
    for i, (category, row) in enumerate(category_stats.head(5).iterrows(), 1):
        percentage = (row['Total_Investment_USD'] / total_investment) * 100
        print(f"  {i}. {category}: ${row['Total_Investment_USD']:,.2f} USD ({percentage:.1f}% of total)")
    
    print(f"\nARTISTIC DISCIPLINES:")
    print(f"• Number of disciplines represented: {df['Disciplina Limpia'].nunique()}")
    print(f"• Top 5 disciplines by investment:")
    for i, (discipline, row) in enumerate(discipline_stats.head(5).iterrows(), 1):
        print(f"  {i}. {discipline}: ${row['Total_Investment_USD']:,.2f} USD ({row['Total_Opportunities']} opportunities)")
    
    print(f"\nPAYMENT STRUCTURE:")
    free_opps = len(df[df['Inscripcion'] == 'Sin cargo'])
    paid_opps = len(df[df['Inscripcion'] == 'Pago'])
    print(f"• Free opportunities: {free_opps} ({(free_opps/total_opportunities)*100:.1f}%)")
    print(f"• Paid opportunities: {paid_opps} ({(paid_opps/total_opportunities)*100:.1f}%)")
    
    if len(significant) > 0:
        print(f"\nHIGH-VALUE OPPORTUNITIES (≥$1,000 USD):")
        print(f"• Number of high-value opportunities: {len(significant)} ({(len(significant)/total_opportunities)*100:.1f}%)")
        print(f"• Total high-value investment: ${significant['Monto_USD'].sum():,.2f} USD")
        print(f"• Average high-value amount: ${significant['Monto_USD'].mean():,.2f} USD")
    
    print(f"\nKEY INSIGHTS:")
    
    # Insight 1: Most generous countries
    top_avg_country = country_stats[country_stats['Total_Opportunities'] >= 3]['Avg_Investment_USD'].idxmax()
    top_avg_amount = country_stats.loc[top_avg_country, 'Avg_Investment_USD']
    print(f"• Most generous country (avg. investment): {top_avg_country} (${top_avg_amount:,.2f} USD per opportunity)")
    
    # Insight 2: Most valuable category
    top_category = category_stats['Avg_Investment_USD'].idxmax()
    top_category_amount = category_stats.loc[top_category, 'Avg_Investment_USD']
    print(f"• Most valuable opportunity type: {top_category} (${top_category_amount:,.2f} USD average)")
    
    # Insight 3: Accessibility
    free_percentage = (free_opps / total_opportunities) * 100
    if free_percentage > 70:
        print(f"• High accessibility: {free_percentage:.1f}% of opportunities are free to apply")
    elif free_percentage > 50:
        print(f"• Moderate accessibility: {free_percentage:.1f}% of opportunities are free to apply")
    else:
        print(f"• Limited accessibility: Only {free_percentage:.1f}% of opportunities are free to apply")

def main():
    """Main analysis function"""
    
    # Load and clean data
    df = load_and_clean_data()
    
    print(f"Total opportunities loaded: {len(df)}")
    print(f"Date range: April - June 2025")
    print(f"Total countries: {df['País'].nunique()}")
    print(f"Total investment mapped: ${df['Monto_USD'].sum():,.2f} USD")
    
    # Perform analyses
    country_stats = analyze_by_country(df)
    category_stats = analyze_by_category(df)
    discipline_stats = analyze_by_discipline(df)
    payment_stats = analyze_payment_requirements(df)
    significant = analyze_significant_opportunities(df)
    
    # Create summary report
    create_summary_report(df, country_stats, category_stats, discipline_stats, significant)
    
    # Export key data
    print(f"\n" + "="*60)
    print("DATA EXPORT")
    print("="*60)
    
    # Save summary tables
    country_stats.to_csv('analysis_by_country.csv')
    category_stats.to_csv('analysis_by_category.csv')
    discipline_stats.to_csv('analysis_by_discipline.csv')
    
    if len(significant) > 0:
        significant[['País', 'Categoría', 'Disciplina Limpia', 'Monto_USD']].to_csv('high_value_opportunities.csv', index=False)
    
    print("Analysis complete. Summary files exported:")
    print("• analysis_by_country.csv")
    print("• analysis_by_category.csv") 
    print("• analysis_by_discipline.csv")
    if len(significant) > 0:
        print("• high_value_opportunities.csv")

if __name__ == "__main__":
    main() 