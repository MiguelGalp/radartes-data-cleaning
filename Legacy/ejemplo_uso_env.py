import os
from dotenv import load_dotenv

def cargar_variables_entorno():
    """
    Carga las variables de entorno desde el archivo .env
    """
    # Cargar variables desde .env
    load_dotenv()
    
    # Obtener la API key
    api_key = os.getenv('PPLX_API_KEY')
    
    if api_key:
        print(f"✅ API Key cargada exitosamente: {api_key[:20]}...")
        return api_key
    else:
        print("❌ Error: No se pudo cargar la API key desde .env")
        return None

def ejemplo_uso_perplexity(api_key):
    """
    Ejemplo de cómo usar la API key de Perplexity
    """
    if not api_key:
        print("❌ No hay API key disponible")
        return
    
    print(f"🔑 API Key disponible para usar con Perplexity: {api_key[:20]}...")
    
    # Aquí puedes agregar el código para usar la API de Perplexity
    # Por ejemplo:
    # import perplexity
    # client = perplexity.Client(api_key=api_key)
    # response = client.chat(...)

if __name__ == "__main__":
    # Cargar variables de entorno
    api_key = cargar_variables_entorno()
    
    # Ejemplo de uso
    ejemplo_uso_perplexity(api_key)
    
    print("\n📝 Para usar en otros scripts:")
    print("1. Importa: from dotenv import load_dotenv")
    print("2. Carga: load_dotenv()")
    print("3. Usa: os.getenv('PPLX_API_KEY')")
