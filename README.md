# Radartes Oportunidades – Pipeline de Limpieza

Este repositorio contiene un flujo de trabajo mínimo para preparar la base de datos de oportunidades publicadas en **Radartes.org** (archivo CSV incluido) y dejarla lista para análisis posterior.

## Archivos principales

* `146 Oportunidades ... .csv` – dataset crudo exportado.
* `clean_radartes_dataset.py` – script de limpieza y normalización.
* `clean_radartes.csv` – (autogenerado) versión limpia del dataset.
* `inversion_por_disciplina_pais.csv` – (autogenerado) tabla resumida de inversión en USD por disciplina y país.

## Requisitos

```bash
pip install pandas
```

## Uso

```bash
python clean_radartes_dataset.py --input "146 Oportunidades b267157879d54cfc8f7106039d4ab221.csv" --output clean_radartes.csv
```

El script: 

1. Normaliza la disciplina de cada oportunidad a las categorías:
   - Música
   - Escénicas
   - Cine
   - Diseño
   - Visuales
   - Literatura
   - Otras (multidisciplina, investigación, etc.)
2. Extrae montos y divisas desde el campo `Og_Resumida` mediante expresiones regulares.
3. Resuelve ambigüedad del símbolo `$` usando la moneda habitual del país.
4. Convierte todos los montos a **USD** (tasas aproximadas 2024 Q4).
5. Marca como `Significativa` la oportunidad si el monto estimado ≥ USD 1 000.
6. Genera una tabla resumida (`inversion_por_disciplina_pais.csv`) con la inversión total por disciplina y país.

> Nota: las tasas de cambio son estimativas y pueden ajustarse en `clean_radartes_dataset.py`. 