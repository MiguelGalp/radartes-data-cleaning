import pandas as pd
import re
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

# ---------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------------------------
# 1. Rutas de Entrada / Salida ------------------------------------------------
DEFAULT_INPUT = Path("146 Oportunidades b267157879d54cfc8f7106039d4ab221.csv")
DEFAULT_OUTPUT = Path("clean_radartes.csv")

# 2. Mapas Auxiliares ---------------------------------------------------------
DISCIPLINE_KEYWORDS = {
    "Música": [
        "música", "musica", "song", "canción", "piano", "compos", "orquesta",
        "sinfónica", "sinfónica", "cant", "sound", "audio"
    ],
    "Escénicas": [
        "danza", "teatro", "circ", "escénic", "perform", "marionet", "coreograf",
        "escenografía", "ópera", "opera", "dramaturg"
    ],
    "Cine": [
        "cine", "film", "movie", "docu", "video", "filmmaker", "animación",
        "filmmaking", "audiovisual"
    ],
    "Diseño": [
        "diseño", "design", "gráfic", "grafica", "arquitect", "interior",
        "packaging", "moda"
    ],
    "Visuales": [
        "visual", "pintur", "escultur", "fotograf", "grabado", "ilustr",
        "arte", "digital", "instalación", "installation", "drawing", "drawing"
    ],
    "Literatura": [
        "poesía", "poesia", "literatur", "escrit", "novel", "relato", "cuento",
        "narrativ", "crónica", "comic", "cómic"
    ],
    "Otras": []  # fallback
}

COUNTRY_CURRENCY = {
    "Argentina": "ARS",
    "España": "EUR",
    "Múltiples Países": "USD",
    "EEUU": "USD",
    "Estados Unidos": "USD",
    "Estados Unidos de América": "USD",
    "Francia": "EUR",
    "Italia": "EUR",
    "Portugal": "EUR",
    "Brasil": "BRL",
    "Chile": "CLP",
    "México": "MXN",
    "Colombia": "COP",
    "Reino Unido": "GBP",
    "Serbia": "RSD",
    "Dinamarca": "DKK",
    "China": "CNY",
    "Japón": "JPY",
    "Turquía": "TRY",
    "Alemania": "EUR",
    "Panamá": "USD",
    "Costa Rica": "CRC",
    "Canadá": "CAD",
    "Ecuador": "USD",
    "Perú": "PEN",
    "Uruguay": "UYU"
}

CURRENCY_WORDS_MAP = {
    # español / inglés plural / singular
    "dólares": "USD",
    "dolares": "USD",
    "dólar": "USD",
    "dolar": "USD",
    "usd": "USD",
    "euros": "EUR",
    "euro": "EUR",
    "pesos": None,  # se resolverá por país
    "peso": None,
    "reales": "BRL",
    "real": "BRL",
    "soles": "PEN",
    "sol": "PEN",
    "libras": "GBP",
    "libra": "GBP",
    "yenes": "JPY",
    "yen": "JPY",
    "yuanes": "CNY",
    "yuan": "CNY"
}

WORD_PATTERN = r"(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)[\s\xa0]*(?P<word>" + "|".join(CURRENCY_WORDS_MAP.keys()) + ")"

EXCHANGE_RATES_USD = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.25,
    "ARS": 0.0011,
    "MXN": 0.057,
    "CLP": 0.0011,
    "COP": 0.00026,
    "BRL": 0.2,
    "PEN": 0.27,
    "RSD": 0.0091,
    "DKK": 0.14,
    "CNY": 0.14,
    "JPY": 0.0067,
    "TRY": 0.031,
    "CAD": 0.74,
    "CRC": 0.0019,
    "UYU": 0.026
}

# RegEx patrones para búsqueda de montos (símbolo, divisa y número)
CURRENCY_SYMBOLS_PATTERN_LEAD = r"(?P<symbol>US\$|\$|€|£|R\$)\s?(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)(?![\d])"
CURRENCY_SYMBOLS_PATTERN_TRAIL = r"(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)(?![\d])\s?(?P<symbol>US\$|\$|€|£|R\$)"
CURRENCY_CODE_BEFORE_PATTERN = r"(?P<code>USD|EUR|GBP|BRL|ARS|MXN|CLP|COP|PEN|CAD|JPY)\s?(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)(?![\d])"
CURRENCY_CODE_AFTER_PATTERN = r"(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)(?![\d])\s?(?P<code>USD|EUR|GBP|BRL|ARS|MXN|CLP|COP|PEN|CAD|JPY)"

SCALE_MAP = {
    "mil": 1_000,
    "miles": 1_000,
    "mil.": 1_000,
    "millón": 1_000_000,
    "millones": 1_000_000,
    "million": 1_000_000,
    "millones.": 1_000_000
}

SCALE_PATTERN = r"(?P<amount>[\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)[\s]*(?P<scale>" + "|".join(SCALE_MAP.keys()) + ")"

# ---------------------------------------------------------------------------
# FUNCIONES PRINCIPALES
# ---------------------------------------------------------------------------

def infer_discipline(text: str) -> str:
    """Determina la disciplina principal a partir de un string."""
    text_low = str(text).lower()
    for disc, kw_list in DISCIPLINE_KEYWORDS.items():
        for kw in kw_list:
            if kw in text_low:
                return disc
    return "Otras"


def parse_amount(text: str) -> Tuple[Optional[float], Optional[str]]:
    """Intenta extraer un monto y su divisa desde texto."""
    if not isinstance(text, str):
        return None, None

    # 1. Símbolo antes del número $1000, € 2.500, etc.
    m = re.search(CURRENCY_SYMBOLS_PATTERN_LEAD, text)
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        sym = m.group("symbol")
        code = {
            "$": "USD",  # ambigua -> resolver después
            "US$": "USD",
            "€": "EUR",
            "£": "GBP",
            "R$": "BRL"
        }[sym]
        return amt, code

    # 1b. Símbolo después del número 1000 $, 2.500 €
    m = re.search(CURRENCY_SYMBOLS_PATTERN_TRAIL, text)
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        sym = m.group("symbol")
        code = {
            "$": "USD",
            "US$": "USD",
            "€": "EUR",
            "£": "GBP",
            "R$": "BRL"
        }[sym]
        return amt, code

    # 2. Códigos ISO antes / después
    m = re.search(CURRENCY_CODE_BEFORE_PATTERN, text, re.IGNORECASE)
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        return amt, m.group("code").upper()

    m = re.search(CURRENCY_CODE_AFTER_PATTERN, text, re.IGNORECASE)
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        return amt, m.group("code").upper()

    # 3. Palabras clave (pesos, euros, dólares, etc.)
    m = re.search(WORD_PATTERN, text.lower())
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        word = m.group("word")
        code = CURRENCY_WORDS_MAP[word]
        # ajustar por escala inmediatamente anterior (ej.: 1,5 millones de pesos)
        before = text.lower()[:m.start()].strip()[-60:]
        m_scale = re.search(SCALE_PATTERN, before)
        if m_scale:
            scale_factor = SCALE_MAP[m_scale.group("scale")]
            amt *= scale_factor
        return amt, code

    # 4. Patrón combinación número-escala-divisa (ej.: 30 mil euros)
    de_opt = r"(?:\sde(?:\sla)?)?"
    currency_opts = "|".join(CURRENCY_WORDS_MAP.keys())
    m = re.search(SCALE_PATTERN + de_opt + r"\s*(?P<word>" + currency_opts + ")", text.lower())
    if m:
        amt = _safe_float(m.group("amount"))
        if amt is None:
            return None, None
        scale_factor = SCALE_MAP[m.group("scale")]
        amt *= scale_factor
        code = CURRENCY_WORDS_MAP[m.group("word")]
        return amt, code

    # No se encontró
    return None, None


def convert_to_usd(amount: float, code: str) -> Optional[float]:
    if amount is None or code is None:
        return None
    rate = EXCHANGE_RATES_USD.get(code)
    if rate is None:
        return None
    # Si el monto es en moneda local, multiplicamos por ratio
    # NOTA: si rate representa USD por unidad de moneda local, es la inversa.
    return amount * rate


def resolve_currency_ambiguity(code: str, country: str) -> str:
    """Cuando el símbolo $ es ambiguo, resolvemos según país."""
    if code != "USD":
        return code
    if country in COUNTRY_CURRENCY and COUNTRY_CURRENCY[country] != "USD":
        return COUNTRY_CURRENCY[country]
    return "USD"


def clean_dataset(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # ---------------------------------------------------------------------
    # 1. Normalizar Disciplina --------------------------------------------
    # Si columna Disciplina tiene valores, usamos; si no, inferimos de Resumen
    df["Disciplina Limpia"] = df["Disciplina"].fillna("")
    df.loc[df["Disciplina Limpia"].str.strip() == "", "Disciplina Limpia"] = (
        df.loc[df["Disciplina Limpia"].str.strip() == "", "Resumen generado por la IA"].apply(infer_discipline)
    )
    # Para las que sí tienen texto, clasificamos mediante keywords tomando primera coincidencia
    df["Disciplina Limpia"] = df["Disciplina Limpia"].apply(infer_discipline)

    # ---------------------------------------------------------------------
    # 2. Extraer monto y convertir ----------------------------------------
    df[["Monto", "Moneda"]] = df["Og_Resumida"].apply(lambda x: pd.Series(parse_amount(x)))
    # Resolver ambigüedad con $ (USD vs moneda local del país)
    def fix_currency(code, country):
        # Si no se encontró divisa, asumimos la del país
        if code is None or pd.isna(code):
            return COUNTRY_CURRENCY.get(country, None)
        # Si es $ ambiguo (USD) resolvemos
        return resolve_currency_ambiguity(code, country)

    df["Moneda"] = [fix_currency(c, p) for c, p in zip(df["Moneda"], df["País"])]

    df["Monto_USD"] = [convert_to_usd(a, c) for a, c in zip(df["Monto"], df["Moneda"])]

    # ---------------------------------------------------------------------
    # 3. Campo inscripción vacía => Sin cargo -----------------------------
    df["Inscripcion"].fillna("Sin cargo", inplace=True)

    # ---------------------------------------------------------------------
    # 4. Relevancia: significant >= 400 USD -------------------------------
    df["Significativa"] = df["Monto_USD"] >= 400

    # ------------------------------------------------------------------
    # 5. Estadísticas resumidas ----------------------------------------
    resumen = (
        df[df["Monto_USD"].notnull()]
        .groupby(["Disciplina Limpia", "País"], as_index=False)["Monto_USD"]
        .sum()
        .rename(columns={"Monto_USD": "Inversion_USD"})
    )

    resumen.to_csv("inversion_por_disciplina_pais.csv", index=False)

    # ---------------------------------------------------------------------
    # Guardar limpio -------------------------------------------------------
    df.to_csv(output_path, index=False)
    return df


# ---------------------------------------------------------------------------
# UTILIDADES ----------------------------------------------------------------


def _safe_float(num_str: str) -> Optional[float]:
    """Convierte string con separadores de miles/coma a float robustamente."""
    if not isinstance(num_str, str):
        return None
    s = re.sub(r"[^0-9.,]", "", num_str)
    # Reemplazar ',' por '.' para unificar; luego decidir cuál es decimal
    s = s.replace(',', '.')
    parts = s.split('.')
    if len(parts) > 2:
        # todos los puntos son separadores de miles; eliminarlos
        s = ''.join(parts)
    elif len(parts) == 2:
        # Si la parte final tiene 3 dígitos, probablemente es separador de miles
        if len(parts[-1]) == 3:
            s = ''.join(parts)
        else:
            s = '.'.join(parts)
    # len(parts)==1 queda igual
    
    try:
        return float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# SCRIPT --------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Limpia y normaliza la base de oportunidades Radartes.")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT), help="Ruta al CSV de entrada.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Ruta al CSV limpio de salida.")
    args = parser.parse_args()

    df_clean = clean_dataset(Path(args.input), Path(args.output))
    print(f"Archivo limpio guardado en {args.output}. Total de filas: {len(df_clean)}") 