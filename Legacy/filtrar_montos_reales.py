import pandas as pd
import numpy as np

def filtrar_montos_reales():
    """
    Filtra los montos reales ofrecidos, eliminando montos bajos que son costos de inscripción
    """
    
    # Leer el archivo CSV con montos extraídos
    try:
        df = pd.read_csv('Data/oportunidades_agosto_2024_con_montos.csv')
        print(f"Archivo leído exitosamente. Total de oportunidades: {len(df)}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Crear copia para trabajar
    df_filtrado = df.copy()
    
    # Contadores para estadísticas
    montos_originales = len(df[df['Monto_Ofrecido'].notna()])
    montos_filtrados = 0
    montos_eliminados = 0
    
    print(f"\n🔍 FILTRANDO MONTOS REALES OFRECIDOS...")
    print(f"Montos originales: {montos_originales}")
    
    # Aplicar filtros para identificar montos que son costos de inscripción
    for index, row in df_filtrado.iterrows():
        if pd.notna(row['Monto_Ofrecido']):
            monto = row['Monto_Ofrecido']
            moneda = row['Moneda']
            nombre = row['Nombre']
            og_resumida = str(row['Og_Resumida'])
            
            # Criterios para identificar costos de inscripción vs montos ofrecidos
            es_costo_inscripcion = False
            
            # 1. Montos bajos en USD (menores a $75)
            if moneda == 'USD' and monto < 75:
                es_costo_inscripcion = True
                print(f"❌ {nombre[:50]}... - ${monto} USD (costo inscripción)")
            
            # 2. Montos bajos en EUR (menores a €70)
            elif moneda == 'EUR' and monto < 70:
                es_costo_inscripcion = True
                print(f"❌ {nombre[:50]}... - €{monto} EUR (costo inscripción)")
            
            # 3. Montos bajos en GBP (menores a £60)
            elif moneda == 'GBP' and monto < 60:
                es_costo_inscripcion = True
                print(f"❌ {nombre[:50]}... - £{monto} GBP (costo inscripción)")
            
            # 4. Buscar palabras clave en el texto que indiquen costo de inscripción
            elif any(palabra in og_resumida.lower() for palabra in [
                'tasa de inscripción', 'costo de inscripción', 'tarifa de inscripción',
                'pago de inscripción', 'cuota de inscripción', 'fee', 'registration fee',
                'application fee', 'entry fee', 'submission fee', 'inscripción requiere',
                'costo para participar', 'tarifa para participar'
            ]):
                es_costo_inscripcion = True
                print(f"❌ {nombre[:50]}... - {monto} {moneda} (palabras clave de costo)")
            
            # Si es costo de inscripción, limpiar el monto
            if es_costo_inscripcion:
                df_filtrado.at[index, 'Monto_Ofrecido'] = None
                df_filtrado.at[index, 'Moneda'] = ''
                montos_eliminados += 1
            else:
                montos_filtrados += 1
                print(f"✅ {nombre[:50]}... - {monto} {moneda} (monto real ofrecido)")
    
    # Guardar archivo filtrado
    output_file = 'Data/oportunidades_agosto_2024_montos_reales.csv'
    df_filtrado.to_csv(output_file, index=False, encoding='utf-8')
    
    # Generar estadísticas
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE FILTRADO DE MONTOS")
    print(f"{'='*60}")
    print(f"Total de oportunidades: {len(df_filtrado)}")
    print(f"Montos originales: {montos_originales}")
    print(f"Montos filtrados (reales): {montos_filtrados}")
    print(f"Montos eliminados (costos): {montos_eliminados}")
    print(f"Porcentaje de montos reales: {(montos_filtrados/montos_originales)*100:.1f}%")
    print(f"Archivo generado: {output_file}")
    
    # Mostrar distribución de monedas después del filtrado
    monedas_filtradas = df_filtrado[df_filtrado['Monto_Ofrecido'].notna()]['Moneda'].value_counts()
    if not monedas_filtradas.empty:
        print(f"\n💰 Distribución de monedas (montos reales):")
        for moneda, count in monedas_filtradas.items():
            print(f"  {moneda}: {count} oportunidades")
    
    # Mostrar top 10 montos más altos después del filtrado
    df_montos = df_filtrado[df_filtrado['Monto_Ofrecido'].notna()].copy()
    if not df_montos.empty:
        df_montos = df_montos.sort_values('Monto_Ofrecido', ascending=False)
        print(f"\n🏆 Top 10 montos más altos (reales):")
        for i, (_, row) in enumerate(df_montos.head(10).iterrows(), 1):
            print(f"  {i}. {row['Nombre'][:40]}...: {row['Monto_Ofrecido']} {row['Moneda']}")
    
    # Crear resumen de cambios
    crear_resumen_cambios(df, df_filtrado)

def crear_resumen_cambios(df_original, df_filtrado):
    """
    Crea un resumen de los cambios realizados
    """
    cambios = []
    
    for index, row_original in df_original.iterrows():
        row_filtrado = df_filtrado.iloc[index]
        
        # Si había monto original pero no en el filtrado
        if pd.notna(row_original['Monto_Ofrecido']) and pd.isna(row_filtrado['Monto_Ofrecido']):
            cambios.append({
                'Nombre': row_original['Nombre'],
                'Monto_Original': f"{row_original['Monto_Ofrecido']} {row_original['Moneda']}",
                'Razon': 'Costo de inscripción identificado'
            })
    
    if cambios:
        print(f"\n📋 RESUMEN DE CAMBIOS:")
        print(f"Se eliminaron {len(cambios)} montos identificados como costos de inscripción:")
        for cambio in cambios[:5]:  # Mostrar solo los primeros 5
            print(f"  • {cambio['Nombre'][:50]}...: {cambio['Monto_Original']}")
        if len(cambios) > 5:
            print(f"  ... y {len(cambios) - 5} más")

if __name__ == "__main__":
    filtrar_montos_reales()
