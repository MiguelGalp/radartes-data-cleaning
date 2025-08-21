# Documentación: Extracción de Montos de Oportunidades Artísticas

## 📋 **Descripción General**

Este documento describe el proceso completo de extracción y análisis de montos ofrecidos en oportunidades artísticas, desde la extracción automática hasta el análisis final en Google Sheets.

## 🔧 **Script: `montosviaLLM.py`**

### **Propósito**
Extraer automáticamente montos y monedas de oportunidades artísticas utilizando la API de Perplexity (LLM) para analizar el campo "Og_Resumida".

### **Funcionalidades Principales**

#### 1. **Configuración Segura de API**
- Utiliza archivo `.env` para almacenar la API key de Perplexity
- Variable de entorno: `PPLX_API_KEY`
- Protección de credenciales sensibles

#### 2. **Extracción Inteligente de Montos**
- **Modelo utilizado**: `sonar-pro` (Perplexity API)
- **Análisis de texto**: Campo "Og_Resumida" de cada oportunidad
- **Formato de salida**: JSON estructurado con monto y moneda

#### 3. **Procesamiento Automatizado**
- Lectura del archivo CSV: `Data/AgostoHastaEl20.csv`
- Procesamiento de 293 oportunidades de agosto 2024
- Generación de columnas: `Monto_Extraido_LLM` y `Moneda_Extraida_LLM`

### **Estructura del Script**

```python
# Configuración
load_dotenv()  # Carga variables de entorno
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# Función principal
def extraer_monto_con_llm(texto_resumen):
    # Análisis con prompt estructurado
    # Retorna (monto, moneda) o (None, None)

# Procesamiento
for index, row in df.iterrows():
    monto, moneda = extraer_monto_con_llm(row['Og_Resumida'])
    # Almacenamiento en DataFrame
```

### **Prompt Utilizado**
```
Analiza el siguiente texto y extrae el monto numérico principal y su moneda.
Texto: "{texto_resumen}"

Responde únicamente con un objeto JSON válido con las claves "monto" y "moneda".
- El monto debe ser un número (int o float), sin comas ni símbolos.
- La moneda debe ser el código ISO de 3 letras (ej. USD, EUR, ARS).
- Si no encuentras un monto claro o es cero, el valor de "monto" debe ser null.
- No incluyas explicaciones, solo el JSON.

Ejemplo de salida: {"monto": 1000, "moneda": "EUR"}
```

## 📊 **Proceso de Análisis en Google Sheets**

### **Paso 1: Importación de Datos**
1. Abrir Google Sheets
2. Importar archivo: `Data/AgostoHastaEl20_con_montos_LLM.csv`
3. Verificar que las columnas se importen correctamente:
   - País
   - Categoría
   - Nombre
   - Og_Resumida
   - Monto_Extraido_LLM
   - Moneda_Extraida_LLM

### **Paso 2: Conversión a USD**
1. **Instalar complemento**: "Convertidor de monedas para Sheets"
2. **Crear nueva columna**: "Monto_USD"
3. **Fórmula de conversión**:
   ```
   =IF(AND(B2<>"",C2<>""),GOOGLEFINANCE("CURRENCY:"&C2&"USD")*B2,"")
   ```
   Donde:
   - B2 = Monto_Extraido_LLM
   - C2 = Moneda_Extraida_LLM

### **Paso 3: Identificación de Montos Requeridos vs Ofrecidos**

#### **Criterios para Montos Requeridos (Costos de Inscripción)**
- **Montos < $75 USD**: Automáticamente clasificados como costos de inscripción
- **Palabras clave en texto**: "tasa de inscripción", "fee", "costo para participar"
- **Contexto**: Cuando el monto se menciona como requisito para aplicar

#### **Criterios para Montos Ofrecidos**
- **Montos ≥ $75 USD**: Potencialmente ofrecidos (requiere verificación manual)
- **Palabras clave**: "premio", "beca", "estipendio", "subvención"
- **Contexto**: Cuando el monto se menciona como beneficio otorgado

#### **Columna de Clasificación**
Crear columna "Tipo_Monto" con valores:
- "Ofrecido" - Montos reales ofrecidos a artistas
- "Requerido" - Costos de inscripción o participación
- "Pendiente" - Requiere verificación manual

### **Paso 4: Verificación Manual**

#### **Oportunidades Sin Montos**
1. **Revisar campo "Og_Resumida"** para oportunidades sin monto extraído
2. **Buscar información adicional** en URLs o descripciones
3. **Clasificar como**:
   - "Sin monto" - No hay información disponible
   - "Monto oculto" - Requiere investigación adicional
   - "Oportunidad gratuita" - Confirmado que no hay costos

#### **Verificación de Montos Altos**
1. **Revisar contexto** de montos ≥ $75 USD
2. **Confirmar si es ofrecido o requerido**
3. **Verificar si es por individuo o total**

## ⚠️ **Limitaciones y Consideraciones**

### **1. Problema de Cantidad de Becas/Premios**

#### **Descripción del Problema**
Muchas oportunidades anuncian montos **por beca/premio individual**, pero no especifican cuántas becas/premios están disponibles. Esto afecta significativamente el análisis de inversión total.

#### **Ejemplos Identificados**
- **Beca individual**: $10,000 USD por becario
- **Premio individual**: $5,000 EUR por ganador
- **Fondo total**: $50,000 USD (sin especificar distribución)

#### **Impacto en el Análisis**
- **Subestimación**: Si hay 10 becas de $10,000, la inversión real es $100,000
- **Sobreestimación**: Si hay 1 beca de $10,000, la inversión es $10,000
- **Incertidumbre**: Sin datos de cantidad, el análisis es incompleto

#### **Estrategias de Mitigación**

##### **A. Investigación Manual**
1. **Revisar URLs** de cada oportunidad
2. **Buscar términos**: "número de becas", "cantidad de premios", "cupos disponibles"
3. **Documentar hallazgos** en columna "Cantidad_Becas"

##### **B. Análisis por Categorías**
1. **Becas**: Generalmente 1-5 beneficiarios
2. **Premios**: 1-10 ganadores
3. **Convocatorias**: Variable según alcance
4. **Residencias**: 1-20 participantes

##### **C. Estimaciones Conservadoras**
- **Sin información**: Asumir 1 beneficiario
- **Con rangos**: Usar valor mínimo
- **Con totales**: Usar monto total

### **2. Limitaciones del LLM**

#### **Errores de Extracción**
- **Montos no detectados**: Textos complejos o ambiguos
- **Monedas incorrectas**: Confusión entre símbolos similares
- **Contexto mal interpretado**: Montos requeridos vs ofrecidos

#### **Solución**
- **Verificación manual** de todos los montos extraídos
- **Refinamiento de prompts** basado en errores identificados
- **Validación cruzada** con fuentes originales

## 📈 **Métricas de Rendimiento**

### **Estadísticas de Extracción**
- **Total de oportunidades**: 293
- **Montos extraídos**: ~48% (estimado)
- **Precisión esperada**: 70-80% (requiere verificación manual)

### **Distribución por Monedas**
- **EUR**: ~55% de los montos extraídos
- **USD**: ~36% de los montos extraídos
- **GBP**: ~6% de los montos extraídos
- **Otras**: ~3% de los montos extraídos

## 🔄 **Proceso de Mejora Continua**

### **1. Refinamiento de Prompts**
- **Análisis de errores** de extracción
- **Ajuste de instrucciones** para casos específicos
- **Pruebas con diferentes modelos**

### **2. Validación de Datos**
- **Muestreo aleatorio** de extracciones
- **Comparación con fuentes originales**
- **Documentación de errores comunes**

### **3. Automatización Adicional**
- **Detección de cantidad de becas** con LLM
- **Clasificación automática** de tipo de monto
- **Validación de URLs** y enlaces

## 📝 **Conclusión**

El proceso de extracción de montos es una herramienta valiosa para el análisis de inversión en oportunidades artísticas, pero requiere:

1. **Verificación manual** de todos los resultados
2. **Investigación adicional** sobre cantidad de becas/premios
3. **Clasificación cuidadosa** entre montos ofrecidos y requeridos
4. **Documentación continua** de limitaciones y mejoras

Este análisis proporciona una base sólida para entender el panorama de financiamiento artístico, pero debe complementarse con investigación manual para obtener una imagen completa de la inversión total en el sector.
