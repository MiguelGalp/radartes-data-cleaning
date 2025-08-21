import pandas as pd
import re
from typing import Optional, Tuple
import sys
import os

# Importar la función parse_amount del script existente
sys.path.append('.')
from clean_radartes_dataset import parse_amount

def extraer_montos_oportunidades():
    """
    Extrae montos ofrecidos del campo Og_Resumida y agrega una nueva columna
    al CSV de oportunidades de agosto
    """
    
    # Leer el archivo CSV de oportunidades de agosto
    try:
        df = pd.read_csv('Data/oportunidades_agosto_2024_procesado.csv')
        print(f"Archivo leído exitosamente. Total de oportunidades: {len(df)}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Verificar que existe la columna Og_Resumida
    if 'Og_Resumida' not in df.columns:
        print("Error: No se encontró la columna 'Og_Resumida'")
        return
    
    # Crear nueva columna para montos extraídos
    montos_extraidos = []
    monedas_extraidas = []
    
    print("Procesando montos...")
    
    for index, row in df.iterrows():
        og_resumida = str(row['Og_Resumida']) if pd.notna(row['Og_Resumida']) else ""
        
        if og_resumida and og_resumida.strip():
            # Usar la función parse_amount del script existente
            monto, moneda = parse_amount(og_resumida)
            
            if monto is not None:
                montos_extraidos.append(monto)
                monedas_extraidas.append(moneda if moneda else "")
                print(f"✅ Oportunidad {index + 1}: {row['Nombre'][:50]}... - Monto: {monto} {moneda}")
            else:
                montos_extraidos.append(None)
                monedas_extraidas.append("")
                print(f"❌ Oportunidad {index + 1}: {row['Nombre'][:50]}... - Sin monto encontrado")
        else:
            montos_extraidos.append(None)
            monedas_extraidas.append("")
            print(f"⚠️  Oportunidad {index + 1}: {row['Nombre'][:50]}... - Campo Og_Resumida vacío")
    
    # Agregar las nuevas columnas al DataFrame
    df['Monto_Ofrecido'] = montos_extraidos
    df['Moneda'] = monedas_extraidas
    
    # Guardar el archivo actualizado
    output_file = 'Data/oportunidades_agosto_2024_con_montos.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Generar estadísticas
    montos_encontrados = sum(1 for m in montos_extraidos if m is not None)
    total_oportunidades = len(df)
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE EXTRACCIÓN DE MONTOS")
    print(f"{'='*60}")
    print(f"Total de oportunidades procesadas: {total_oportunidades}")
    print(f"Montos extraídos exitosamente: {montos_encontrados}")
    print(f"Porcentaje de éxito: {(montos_encontrados/total_oportunidades)*100:.1f}%")
    print(f"Archivo generado: {output_file}")
    
    # Mostrar distribución de monedas
    monedas_count = {}
    for moneda in monedas_extraidas:
        if moneda:
            monedas_count[moneda] = monedas_count.get(moneda, 0) + 1
    
    if monedas_count:
        print(f"\n💰 Distribución de monedas:")
        for moneda, count in sorted(monedas_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {moneda}: {count} oportunidades")
    
    # Mostrar algunos ejemplos de montos extraídos
    print(f"\n💡 Ejemplos de montos extraídos:")
    ejemplos = 0
    for index, row in df.iterrows():
        if row['Monto_Ofrecido'] is not None and ejemplos < 5:
            print(f"  • {row['Nombre'][:40]}...: {row['Monto_Ofrecido']} {row['Moneda']}")
            ejemplos += 1

if __name__ == "__main__":
    extraer_montos_oportunidades()
