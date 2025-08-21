import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo y fuentes para español
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Cargar datos
all_data = pd.read_csv('complete_analysis_with_accessibility.csv')
international_data = pd.read_csv('international_opportunities_only.csv')

print("Creando visualizaciones integrales para análisis RADARTES en español...")

# Crear figura con múltiples subgráficos para dashboard integral
fig = plt.figure(figsize=(20, 24))

# 1. VISUALIZACIONES SECCIÓN 1 - RADARTES COMO PLATAFORMA

# 1.1 Distribución Geográfica Global
ax1 = plt.subplot(4, 2, 1)
country_counts = all_data['País'].value_counts().head(15)
bars = ax1.barh(range(len(country_counts)), country_counts.values, 
                color=sns.color_palette("viridis", len(country_counts)))
ax1.set_yticks(range(len(country_counts)))
ax1.set_yticklabels(country_counts.index)
ax1.set_xlabel('Número de Oportunidades')
ax1.set_title('Alcance Global RADARTES: Top 15 Países\n534 Oportunidades en 57 Países', 
              fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Agregar etiquetas de valores
for i, v in enumerate(country_counts.values):
    ax1.text(v + 1, i, str(v), va='center', fontsize=9)

# 1.2 Inversión por Categoría - Perspectiva de Plataforma
ax2 = plt.subplot(4, 2, 2)
category_analysis = all_data.groupby('Categoría').agg({
    'Monto_USD': ['sum', 'count', 'mean']
}).round(2)
category_analysis.columns = ['Inversión_Total', 'Cantidad', 'Inversión_Promedio']
category_analysis = category_analysis.sort_values('Inversión_Total', ascending=False)

# Crear barras mostrando tanto cantidad como inversión
bars1 = ax2.bar(category_analysis.index, category_analysis['Inversión_Total']/1000000, 
                alpha=0.8, label='Inversión Total (Millones USD)')
ax2_twin = ax2.twinx()
bars2 = ax2_twin.bar(category_analysis.index, category_analysis['Cantidad'], 
                     alpha=0.6, color='orange', label='Número de Oportunidades')

ax2.set_ylabel('Inversión (Millones USD)', color='blue')
ax2_twin.set_ylabel('Número de Oportunidades', color='orange')
ax2.set_title('Panorama de Inversión por Categoría\nDoble Perspectiva: Volumen vs. Cantidad', 
              fontsize=12, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# 1.3 Análisis de Accesibilidad
ax3 = plt.subplot(4, 2, 3)
accessibility = all_data['Inscripcion'].value_counts()
colors = ['#2E8B57', '#FF6B6B', '#4ECDC4']
wedges, texts, autotexts = ax3.pie(accessibility.values, labels=accessibility.index, 
                                   autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title('Accesibilidad: Requisitos de Cuota de Inscripción\n81.3% Gratuitas para Postular', 
              fontsize=12, fontweight='bold')

# 1.4 Distribución Disciplinaria
ax4 = plt.subplot(4, 2, 4)
discipline_counts = all_data['Disciplina Limpia'].value_counts()
bars = ax4.bar(discipline_counts.index, discipline_counts.values, 
               color=sns.color_palette("Set3", len(discipline_counts)))
ax4.set_xlabel('Disciplina Artística')
ax4.set_ylabel('Número de Oportunidades')
ax4.set_title('Oportunidades por Disciplina Artística\nArtes Visuales Lideran con 40.8%', 
              fontsize=12, fontweight='bold')
ax4.tick_params(axis='x', rotation=45)
ax4.grid(axis='y', alpha=0.3)

# Agregar etiquetas de porcentaje
total_ops = discipline_counts.sum()
for i, v in enumerate(discipline_counts.values):
    percentage = (v/total_ops)*100
    ax4.text(i, v + 5, f'{percentage:.1f}%', ha='center', fontsize=9)

# 2. VISUALIZACIONES SECCIÓN 2 - ANÁLISIS ESTRATÉGICO

# 2.1 Comparación Inversión Internacional vs Doméstica
ax5 = plt.subplot(4, 2, 5)
comparison_data = {
    'Domésticas/Restringidas': 35800000,  # De nuestro análisis
    'Verdaderamente Internacionales': 12100000   # De nuestro análisis
}
bars = ax5.bar(comparison_data.keys(), list(comparison_data.values()), 
               color=['#FF6B6B', '#2E8B57'], alpha=0.8)
ax5.set_ylabel('Inversión (USD)')
ax5.set_title('Realidad Estratégica: Inversión Doméstica vs Internacional\nDivisión 74.8% vs 25.2%', 
              fontsize=12, fontweight='bold')
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Agregar etiquetas de valores
for bar in bars:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 500000,
             f'${height/1e6:.1f}M\n({height/(sum(comparison_data.values()))*100:.1f}%)',
             ha='center', va='bottom', fontweight='bold')

# 2.2 Financiamiento Internacional Real por País
ax6 = plt.subplot(4, 2, 6)
international_by_country = international_data.groupby('País')['Monto_USD'].sum().sort_values(ascending=False).head(8)
bars = ax6.barh(range(len(international_by_country)), international_by_country.values, 
                color=sns.color_palette("plasma", len(international_by_country)))
ax6.set_yticks(range(len(international_by_country)))
ax6.set_yticklabels(international_by_country.index)
ax6.set_xlabel('Inversión Internacional (USD)')
ax6.set_title('Líderes en Financiamiento Internacional Real\nEspaña Domina con 88.7%', 
              fontsize=12, fontweight='bold')
ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Agregar etiquetas de porcentaje
total_intl = international_by_country.sum()
for i, v in enumerate(international_by_country.values):
    percentage = (v/total_intl)*100
    ax6.text(v + 100000, i, f'{percentage:.1f}%', va='center', fontsize=9)

# 2.3 Análisis Modelo de Inversión - Enfoque Internacional
ax7 = plt.subplot(4, 2, 7)
international_categories = international_data.groupby('Categoría')['Monto_USD'].sum().sort_values(ascending=False)
colors_cat = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
bars = ax7.bar(international_categories.index, international_categories.values, 
               color=colors_cat[:len(international_categories)])
ax7.set_ylabel('Inversión (USD)')
ax7.set_xlabel('Tipo de Categoría')
ax7.set_title('Modelo de Inversión Internacional\nPremios Basados en Mérito Dominan', 
              fontsize=12, fontweight='bold')
ax7.tick_params(axis='x', rotation=45)
ax7.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# Agregar etiquetas de porcentaje
total_intl_cat = international_categories.sum()
for i, v in enumerate(international_categories.values):
    percentage = (v/total_intl_cat)*100
    ax7.text(i, v + 50000, f'{percentage:.1f}%', ha='center', fontsize=9)

# 2.4 Distribución Oportunidades de Alto Valor
ax8 = plt.subplot(4, 2, 8)
high_value = all_data[all_data['Monto_USD'] >= 1000]
high_value_by_country = high_value.groupby('País').agg({
    'Monto_USD': 'count'
}).sort_values('Monto_USD', ascending=False).head(10)

bars = ax8.bar(range(len(high_value_by_country)), high_value_by_country['Monto_USD'], 
               color=sns.color_palette("coolwarm", len(high_value_by_country)))
ax8.set_xticks(range(len(high_value_by_country)))
ax8.set_xticklabels(high_value_by_country.index, rotation=45)
ax8.set_ylabel('Número de Oportunidades de Alto Valor')
ax8.set_title('Oportunidades de Alto Valor (≥$1,000)\n203 Oportunidades Totales por $47.9M', 
              fontsize=12, fontweight='bold')
ax8.grid(axis='y', alpha=0.3)

# Agregar etiquetas de valores
for i, v in enumerate(high_value_by_country['Monto_USD']):
    ax8.text(i, v + 1, str(v), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('analisis_integral_radartes_espanol.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear tabla de estadísticas resumen
print("\n" + "="*60)
print("RESUMEN ANÁLISIS INTEGRAL RADARTES")
print("="*60)

print(f"\nSECCIÓN 1 - PANORAMA DE PLATAFORMA:")
print(f"Total de Oportunidades: {len(all_data)}")
print(f"Países Representados: {all_data['País'].nunique()}")
print(f"Inversión Total Registrada: ${all_data['Monto_USD'].sum():,.2f}")
print(f"Tasa de Postulación Gratuita: {(all_data['Inscripcion'] == 'Sin cargo').mean()*100:.1f}%")
print(f"Oportunidades de Alto Valor (≥$1K): {len(all_data[all_data['Monto_USD'] >= 1000])} ({len(all_data[all_data['Monto_USD'] >= 1000])/len(all_data)*100:.1f}%)")

print(f"\nSECCIÓN 2 - ANÁLISIS ESTRATÉGICO:")
print(f"Oportunidades Verdaderamente Internacionales: {len(international_data)}")
print(f"Inversión Internacional: ${international_data['Monto_USD'].sum():,.2f}")
print(f"Inversión Doméstica: ${all_data['Monto_USD'].sum() - international_data['Monto_USD'].sum():,.2f}")
print(f"Participación de España en Internacional: {(international_data[international_data['País'] == 'España']['Monto_USD'].sum() / international_data['Monto_USD'].sum())*100:.1f}%")

print(f"\nPRINCIPALES FINANCIADORES INTERNACIONALES:")
top_international = international_data.groupby('País')['Monto_USD'].sum().sort_values(ascending=False).head(5)
for country, investment in top_international.items():
    percentage = (investment / international_data['Monto_USD'].sum()) * 100
    print(f"  {country}: ${investment:,.2f} ({percentage:.1f}%)")

print(f"\nDESGLOSE DISCIPLINARIO:")
discipline_breakdown = all_data['Disciplina Limpia'].value_counts()
for discipline, count in discipline_breakdown.items():
    percentage = (count / len(all_data)) * 100
    print(f"  {discipline}: {count} oportunidades ({percentage:.1f}%)")

print("\nVisualización guardada como 'analisis_integral_radartes_espanol.png'")
print("¡Análisis completo!") 