import csv
import pandas as pd

def procesar_oportunidades_agosto():
    """
    Procesa el archivo CSV de oportunidades de agosto y genera un nuevo CSV
    con los campos: País, Categoría, Nombre y Og_Resumida
    """
    
    # Leer el archivo CSV original
    try:
        df = pd.read_csv('Data/AgostoHastaEl20.csv')
        print(f"Archivo leído exitosamente. Total de oportunidades: {len(df)}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Seleccionar solo las columnas necesarias
    columnas_requeridas = ['País', 'Categoría', 'Nombre', 'Og_Resumida']
    
    # Verificar que las columnas existan
    columnas_disponibles = df.columns.tolist()
    print(f"Columnas disponibles: {columnas_disponibles}")
    
    # Crear el nuevo DataFrame con las columnas requeridas
    df_procesado = df[columnas_requeridas].copy()
    
    # Limpiar datos: reemplazar valores NaN con cadenas vacías
    df_procesado = df_procesado.fillna('')
    
    # Guardar el nuevo CSV
    archivo_salida = 'oportunidades_agosto_2024_procesado.csv'
    df_procesado.to_csv(archivo_salida, index=False, encoding='utf-8')
    
    print(f"Archivo procesado guardado como: {archivo_salida}")
    print(f"Total de oportunidades procesadas: {len(df_procesado)}")
    
    # Mostrar estadísticas básicas
    print("\nEstadísticas:")
    print(f"- Oportunidades con país especificado: {len(df_procesado[df_procesado['País'] != ''])}")
    print(f"- Oportunidades con categoría especificada: {len(df_procesado[df_procesado['Categoría'] != ''])}")
    print(f"- Oportunidades con Og_Resumida: {len(df_procesado[df_procesado['Og_Resumida'] != ''])}")
    
    # Mostrar las primeras 5 filas como ejemplo
    print("\nPrimeras 5 oportunidades:")
    print(df_procesado.head().to_string(index=False))
    
    return df_procesado

if __name__ == "__main__":
    df_resultado = procesar_oportunidades_agosto()
