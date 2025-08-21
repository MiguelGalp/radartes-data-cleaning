import os
import pandas as pd
import json
from dotenv import load_dotenv
from openai import OpenAI
import time

# --- Cargar variables de entorno desde .env ---
load_dotenv()

# --- Configuración Segura de la API Key ---
try:
    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        raise KeyError("API key no encontrada")
except KeyError:
    print("Error: La variable de entorno PPLX_API_KEY no está configurada.")
    print("Por favor, verifica que el archivo .env existe y contiene PPLX_API_KEY=tu_clave")
    exit()

# --- Cliente de OpenAI apuntando a la API de Perplexity ---
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

def extraer_monto_con_llm(texto_resumen):
    """
    Utiliza la API de Perplexity para extraer el monto y la moneda de un texto.
    """
    if not isinstance(texto_resumen, str) or not texto_resumen.strip():
        return None, None

    prompt = f"""
    Analiza el siguiente texto y extrae el monto numérico principal y su moneda.
    Texto: "{texto_resumen}"

    Responde únicamente con un objeto JSON válido con las claves "monto" y "moneda".
    - El monto debe ser un número (int o float), sin comas ni símbolos.
    - La moneda debe ser el código ISO de 3 letras (ej. USD, EUR, ARS).
    - Si no encuentras un monto claro o es cero, el valor de "monto" debe ser null.
    - No incluyas explicaciones, solo el JSON.

    Ejemplo de salida: {{"monto": 1000, "moneda": "EUR"}}
    """

    try:
        # ✅ *** MODELO CORREGIDO ***
        response = client.chat.completions.create(
            model="sonar-pro", 
            messages=[
                {"role": "system", "content": "Eres un asistente que solo responde con formato JSON."},
                {"role": "user", "content": prompt},
            ]
        )
        
        resultado_json = response.choices[0].message.content
        datos = json.loads(resultado_json)
        
        return datos.get('monto'), datos.get('moneda')

    except json.JSONDecodeError as e:
        print(f"  ⚠️ Error de formato JSON: {e}. Respuesta recibida: {resultado_json}")
        return None, None
    except Exception as e:
        print(f"  ❌ Error en API: {e}")
        return None, None

# --- Procesamiento del Archivo CSV ---
try:
    df = pd.read_csv('Data/AgostoHastaEl20.csv')
    print(f"✅ Archivo leído exitosamente. Total de registros: {len(df)}")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'Data/AgostoHastaEl20.csv'")
    exit()

df['Monto_Extraido_LLM'] = None
df['Moneda_Extraida_LLM'] = None

print(f"\n🔍 Procesando {len(df)} registros con Perplexity API...")
print("-" * 50)

for index, row in df.iterrows():
    print(f"  Procesando registro #{index + 1}/{len(df)}...", end='\r') 
    
    monto, moneda = extraer_monto_con_llm(row['Og_Resumida'])
    df.at[index, 'Monto_Extraido_LLM'] = monto
    df.at[index, 'Moneda_Extraida_LLM'] = moneda
    
    time.sleep(0.5) 

# --- Guardado y Resumen ---
output_file = 'Data/AgostoHastaEl20_con_montos_LLM.csv'
df.to_csv(output_file, index=False)

print("\n" + "-" * 50)
print(f"🎉 ¡Proceso completado!")
print(f"📁 Resultados guardados en: {output_file}")

montos_encontrados = df['Monto_Extraido_LLM'].notna().sum()
print(f"💰 Montos extraídos: {montos_encontrados}/{len(df)} ({montos_encontrados/len(df)*100:.1f}%)")