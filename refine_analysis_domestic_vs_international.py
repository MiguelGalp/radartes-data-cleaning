import pandas as pd
import numpy as np
import re

def identify_domestic_opportunities():
    """Identify and categorize opportunities based on domestic vs international accessibility"""
    
    # Load the datasets
    abril = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-abril.csv')
    mayo = pd.read_csv('enriched_radartes-mayo.csv')
    junio = pd.read_csv('Dataset Abril Corregido por Escrapeo - enriched_radartes-junio.csv')
    
    # Standardize columns - use common columns available in all datasets
    common_cols = ['Resumen generado por la IA', 'País', 'Entidad', 'Categoría', 'Disciplina Limpia', 'Inscripcion', 'Monto_USD']
    
    # For abril, add the Nombre column if it exists
    abril_cols = common_cols.copy()
    if 'Nombre' in abril.columns:
        abril_cols.insert(0, 'Nombre')
    abril_clean = abril[abril_cols].copy()
    abril_clean['Mes'] = 'Abril'
    
    # For mayo, add the Nombre column if it exists
    mayo_cols = common_cols.copy()
    if 'Nombre' in mayo.columns:
        mayo_cols.insert(0, 'Nombre')
    mayo_clean = mayo[mayo_cols].copy()
    mayo_clean['Mes'] = 'Mayo'
    
    # Junio doesn't have Nombre column
    junio_clean = junio[common_cols].copy()
    junio_clean['Mes'] = 'Junio'
    if 'Nombre' not in junio_clean.columns:
        junio_clean['Nombre'] = junio_clean['Resumen generado por la IA'].str[:50] + '...'
    
    # Combine datasets
    combined = pd.concat([abril_clean, mayo_clean, junio_clean], ignore_index=True)
    combined['Monto_USD'] = pd.to_numeric(combined['Monto_USD'], errors='coerce').fillna(0)
    
    # Replace "Residencia" values with 3500 USD
    combined.loc[combined['Monto_USD'].astype(str).str.contains('Residencia', case=False, na=False), 'Monto_USD'] = 3500
    
    # Define patterns for domestic-only opportunities
    domestic_patterns = {
        'México': [
            'PECDA', 'Sistema de Apoyos a la Creación', 'SACPC', 'Secretaría de Cultura.*México',
            'Ministerio de Cultura.*México', 'FONCA', 'Fondo Nacional para la Cultura',
            'Instituto Nacional.*México', 'Gobierno.*México', 'Ciudad de.*México',
            'mexicanos', 'residencia.*México', 'nacionalidad.*mexicana'
        ],
        'Argentina': [
            'INCAA', 'Instituto Nacional de Cine.*Argentina', 'Ministerio de Cultura.*Argentina',
            'Secretaría de Cultura.*Argentina', 'Gobierno.*Argentina', 'argentinos',
            'residencia.*Argentina', 'nacionalidad.*argentina', 'Fundación.*Argentina',
            'Buenos Aires.*Gobierno'
        ],
        'Chile': [
            'CNCA', 'Consejo Nacional.*Chile', 'Ministerio.*Cultura.*Chile',
            'Gobierno de Chile', 'chilenos', 'residencia.*Chile', 'nacionalidad.*chilena',
            'Fondo.*Chile', 'FONDART'
        ]
    }
    
    # Patterns for truly international opportunities
    international_patterns = [
        'todo el mundo', 'cualquier nacionalidad', 'artistas internacionales',
        'Latinoamérica', 'América Latina', 'latinoamericanos', 'iberoamericanos',
        'sin restricción.*nacionalidad', 'abierto a todos', 'internacional'
    ]
    
    def categorize_opportunity(row):
        """Categorize each opportunity as domestic, international, or ambiguous"""
        nombre = row.get('Nombre', '')
        entidad = row.get('Entidad', '')
        resumen = row.get('Resumen generado por la IA', '')
        text_to_check = f"{nombre} {entidad} {resumen}".lower()
        
        country = row['País']
        
        # Check for domestic patterns
        if country in domestic_patterns:
            for pattern in domestic_patterns[country]:
                if re.search(pattern.lower(), text_to_check):
                    return 'Domestic'
        
        # Check for international patterns
        for pattern in international_patterns:
            if re.search(pattern.lower(), text_to_check):
                return 'International'
        
        # Special cases for Spanish institutions (more likely to be international)
        if country == 'España':
            spanish_international_entities = [
                'museo del prado', 'acción cultural española', 'cervantino',
                'festival internacional', 'premio internacional', 'residencia internacional'
            ]
            for entity in spanish_international_entities:
                if entity in text_to_check:
                    return 'International'
        
        # Default categorization based on patterns
        if country in ['México', 'Argentina', 'Chile']:
            return 'Likely_Domestic'
        else:
            return 'Likely_International'
    
    # Apply categorization
    combined['Accessibility'] = combined.apply(categorize_opportunity, axis=1)
    
    return combined

def generate_refined_analysis():
    """Generate refined analysis separating domestic vs international opportunities"""
    
    df = identify_domestic_opportunities()
    
    print("="*80)
    print("REFINED ANALYSIS: DOMESTIC vs INTERNATIONAL OPPORTUNITIES")
    print("="*80)
    
    # Overall breakdown
    accessibility_breakdown = df.groupby('Accessibility').agg({
        'Monto_USD': ['count', 'sum', 'mean'],
        'País': lambda x: x.value_counts().head(3).to_dict()
    }).round(2)
    
    print(f"\nOVERALL ACCESSIBILITY BREAKDOWN:")
    for category in df['Accessibility'].unique():
        subset = df[df['Accessibility'] == category]
        count = len(subset)
        total_investment = subset['Monto_USD'].sum()
        avg_investment = subset['Monto_USD'].mean()
        percentage = (count / len(df)) * 100
        
        print(f"\n{category.upper()}:")
        print(f"  • Opportunities: {count} ({percentage:.1f}%)")
        print(f"  • Total Investment: ${total_investment:,.2f} USD")
        print(f"  • Average Investment: ${avg_investment:,.2f} USD")
        print(f"  • Top Countries: {subset['País'].value_counts().head(3).to_dict()}")
    
    # True international opportunities analysis
    international_only = df[df['Accessibility'].isin(['International', 'Likely_International'])]
    
    print(f"\n" + "="*60)
    print("ANALYSIS OF TRULY INTERNATIONAL OPPORTUNITIES")
    print("="*60)
    
    print(f"\nTOTAL INTERNATIONAL OPPORTUNITIES:")
    print(f"• Count: {len(international_only)}")
    print(f"• Total Investment: ${international_only['Monto_USD'].sum():,.2f} USD")
    print(f"• Average Investment: ${international_only['Monto_USD'].mean():,.2f} USD")
    print(f"• Percentage of total opportunities: {(len(international_only)/len(df))*100:.1f}%")
    print(f"• Percentage of total investment: {(international_only['Monto_USD'].sum()/df['Monto_USD'].sum())*100:.1f}%")
    
    # International opportunities by country
    intl_by_country = international_only.groupby('País').agg({
        'Monto_USD': ['count', 'sum', 'mean']
    }).round(2)
    intl_by_country.columns = ['Count', 'Total_USD', 'Avg_USD']
    intl_by_country = intl_by_country.sort_values('Total_USD', ascending=False)
    
    print(f"\nINTERNATIONAL OPPORTUNITIES BY COUNTRY:")
    print(intl_by_country.head(10))
    
    # Comparison: Domestic Mexico vs International Mexico
    mexico_domestic = df[(df['País'] == 'México') & (df['Accessibility'].isin(['Domestic', 'Likely_Domestic']))]
    mexico_international = df[(df['País'] == 'México') & (df['Accessibility'].isin(['International', 'Likely_International']))]
    
    print(f"\nMEXICO COMPARISON:")
    print(f"Domestic Opportunities: {len(mexico_domestic)} | Investment: ${mexico_domestic['Monto_USD'].sum():,.2f}")
    print(f"International Opportunities: {len(mexico_international)} | Investment: ${mexico_international['Monto_USD'].sum():,.2f}")
    
    # Save refined datasets
    df.to_csv('complete_analysis_with_accessibility.csv', index=False)
    international_only.to_csv('international_opportunities_only.csv', index=False)
    
    # Generate summary for international opportunities
    intl_summary = {
        'total_opportunities': len(international_only),
        'total_investment': international_only['Monto_USD'].sum(),
        'avg_investment': international_only['Monto_USD'].mean(),
        'top_countries': international_only.groupby('País')['Monto_USD'].sum().sort_values(ascending=False).head(5).to_dict(),
        'top_categories': international_only.groupby('Categoría')['Monto_USD'].sum().sort_values(ascending=False).head(5).to_dict()
    }
    
    return df, international_only, intl_summary

def create_corrected_executive_summary(intl_summary):
    """Create corrected key findings for the executive summary"""
    
    print(f"\n" + "="*60)
    print("CORRECTED EXECUTIVE SUMMARY FINDINGS")
    print("="*60)
    
    total_intl_investment = intl_summary['total_investment']
    total_intl_opportunities = intl_summary['total_opportunities']
    
    print(f"\nKEY CORRECTIONS FOR REPORT:")
    print(f"• TRUE International Investment: ${total_intl_investment:,.2f} USD")
    print(f"• TRUE International Opportunities: {total_intl_opportunities}")
    print(f"• Average per International Opportunity: ${intl_summary['avg_investment']:,.2f} USD")
    
    print(f"\nTOP COUNTRIES FOR INTERNATIONAL OPPORTUNITIES:")
    for i, (country, investment) in enumerate(intl_summary['top_countries'].items(), 1):
        percentage = (investment / total_intl_investment) * 100
        print(f"  {i}. {country}: ${investment:,.2f} USD ({percentage:.1f}%)")
    
    print(f"\nTOP CATEGORIES FOR INTERNATIONAL OPPORTUNITIES:")
    for i, (category, investment) in enumerate(intl_summary['top_categories'].items(), 1):
        percentage = (investment / total_intl_investment) * 100
        print(f"  {i}. {category}: ${investment:,.2f} USD ({percentage:.1f}%)")

if __name__ == "__main__":
    df, international_only, intl_summary = generate_refined_analysis()
    create_corrected_executive_summary(intl_summary)
    
    print(f"\n" + "="*60)
    print("FILES GENERATED:")
    print("• complete_analysis_with_accessibility.csv")
    print("• international_opportunities_only.csv")
    print("="*60) 