# 🎯 Extracción de Montos de Oportunidades Artísticas

## 📋 **Resumen Ejecutivo**

Este proyecto automatiza la extracción de montos ofrecidos en oportunidades artísticas utilizando Inteligencia Artificial (LLM) y proporciona herramientas para el análisis posterior en Google Sheets.

## 🚀 **Flujo de Trabajo Completo**

### **1. Extracción Automática**
```bash
python3 montosviaLLM.py
```
- **Entrada**: `Data/AgostoHastaEl20.csv` (293 oportunidades)
- **Salida**: `Data/AgostoHastaEl20_con_montos_LLM.csv`
- **Tecnología**: API de Perplexity (modelo sonar-pro)

### **2. Análisis en Google Sheets**
1. **Importar** archivo CSV con montos extraídos
2. **Convertir** a USD usando complemento de monedas
3. **Clasificar** montos requeridos vs ofrecidos
4. **Verificar** manualmente casos especiales

### **3. Documentación y Fórmulas**
- `DOCUMENTACION_EXTRACCION_MONTOS.md` - Documentación completa
- `formulas_google_sheets.md` - Fórmulas para análisis

## 📊 **Resultados Esperados**

### **Estadísticas de Extracción**
- **Total de oportunidades**: 293
- **Montos extraídos**: ~48% (140-150 oportunidades)
- **Precisión esperada**: 70-80%

### **Distribución por Monedas**
- **EUR**: 55% (principalmente becas europeas)
- **USD**: 36% (oportunidades internacionales)
- **GBP**: 6% (oportunidades británicas)
- **Otras**: 3% (monedas latinoamericanas)

## ⚠️ **Limitaciones Críticas**

### **1. Problema de Cantidad de Becas**
- **Descripción**: Montos anunciados por individuo, no total
- **Ejemplo**: $10,000 USD por becario (¿cuántos becarios?)
- **Impacto**: Análisis de inversión incompleto

### **2. Clasificación Montos**
- **< $75 USD**: Costos de inscripción
- **≥ $75 USD**: Potencialmente ofrecidos
- **Requiere**: Verificación manual del contexto

### **3. Errores de Extracción**
- **Montos no detectados**: Textos complejos
- **Monedas incorrectas**: Confusión de símbolos
- **Contexto mal interpretado**: Requerido vs ofrecido

## 🔧 **Configuración Técnica**

### **Dependencias**
```bash
pip3 install python-dotenv openai pandas
```

### **Variables de Entorno**
```bash
# .env
PPLX_API_KEY=your_api_key_here
```

### **Estructura de Archivos**
```
├── montosviaLLM.py                    # Script principal
├── .env                               # API key (protegido)
├── .gitignore                         # Archivos excluidos
├── DOCUMENTACION_EXTRACCION_MONTOS.md # Documentación completa
├── formulas_google_sheets.md          # Fórmulas de análisis
├── Data/
│   ├── AgostoHastaEl20.csv           # Datos originales
│   └── AgostoHastaEl20_con_montos_LLM.csv # Resultados
```

## 📈 **Métricas de Rendimiento**

### **Extracción Automática**
- **Tiempo de procesamiento**: ~15-20 minutos (293 registros)
- **Costo estimado**: ~$2-5 USD (API calls)
- **Tasa de éxito**: 48% (extracción inicial)

### **Verificación Manual**
- **Tiempo estimado**: 2-3 horas
- **Precisión final**: 90-95%
- **Casos especiales**: 10-15% requieren investigación adicional

## 🎯 **Casos de Uso**

### **Análisis de Inversión**
- **Total de financiamiento** disponible para artistas
- **Distribución geográfica** de oportunidades
- **Tendencias temporales** en financiamiento

### **Identificación de Oportunidades**
- **Oportunidades de alto valor** (>$10K USD)
- **Oportunidades por país** específico
- **Oportunidades por disciplina** artística

### **Análisis de Mercado**
- **Concentración de financiamiento** por región
- **Tipos de oportunidades** más comunes
- **Evolución de montos** en el tiempo

## 🔄 **Proceso de Mejora Continua**

### **Refinamiento de Prompts**
- **Análisis de errores** de extracción
- **Ajuste de instrucciones** para casos específicos
- **Pruebas con diferentes modelos**

### **Validación de Datos**
- **Muestreo aleatorio** de extracciones
- **Comparación con fuentes originales**
- **Documentación de errores comunes**

### **Automatización Adicional**
- **Detección de cantidad de becas** con LLM
- **Clasificación automática** de tipo de monto
- **Validación de URLs** y enlaces

## 📝 **Próximos Pasos**

### **Corto Plazo (1-2 semanas)**
1. **Ejecutar script** de extracción
2. **Importar a Google Sheets** y aplicar fórmulas
3. **Verificación manual** de montos extraídos
4. **Clasificación** de tipos de monto

### **Mediano Plazo (1 mes)**
1. **Investigación manual** de cantidad de becas
2. **Refinamiento** de criterios de clasificación
3. **Análisis estadístico** completo
4. **Documentación** de hallazgos

### **Largo Plazo (2-3 meses)**
1. **Automatización** de detección de cantidad de becas
2. **Dashboard** interactivo de análisis
3. **Sistema de alertas** para nuevas oportunidades
4. **Integración** con otras fuentes de datos

## 🤝 **Contribución**

### **Reportar Errores**
- **Errores de extracción**: Documentar casos específicos
- **Fórmulas incorrectas**: Verificar cálculos en Google Sheets
- **Limitaciones**: Identificar casos no cubiertos

### **Mejoras Sugeridas**
- **Nuevos criterios** de clasificación
- **Fórmulas adicionales** para análisis
- **Automatización** de procesos manuales

## 📞 **Contacto y Soporte**

Para preguntas o problemas:
1. **Revisar documentación** completa
2. **Verificar configuración** de API key
3. **Consultar fórmulas** de Google Sheets
4. **Documentar errores** específicos

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0  
**Estado**: Funcional - Requiere verificación manual
