import pandas as pd
import re
import requests
import hashlib
import time
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

from clean_radartes_dataset import _safe_float, convert_to_usd, EXCHANGE_RATES_USD, COUNTRY_CURRENCY

CACHE_DIR = Path('.web_cache')
CACHE_DIR.mkdir(exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; RadartesBot/1.0; +https://radartes.org)'
}
TIMEOUT = 15
SLEEP_BETWEEN = 0.7  # seconds

# --- patrones de búsqueda de montos (basado en script principal) ---------
CURRENCY_SYMBOLS = r"US\$|\$|€|£|R\$"
ISO_CODES = r"USD|EUR|GBP|BRL|ARS|MXN|CLP|COP|PEN|CAD|JPY"
WORD_CURRENCY = r"dólares?|dolares?|euros?|peso?s?|reales?|soles?|libras?|yenes?|yuanes?"

AMOUNT_PATTERN = rf"(?P<symbol>{CURRENCY_SYMBOLS})?\s*(?P<amt>[\d]{{1,3}}(?:[.,]\d{{3}})*(?:[.,]\d+)?)\s*(?P<after_sym>{CURRENCY_SYMBOLS})?|(?P<code>{ISO_CODES})\s*(?P<amt2>[\d]{{1,3}}(?:[.,]\d{{3}})*(?:[.,]\d+)?)|(?P<amt3>[\d]{{1,3}}(?:[.,]\d{{3}})*(?:[.,]\d+)?)\s*(?P<word>{WORD_CURRENCY})"
AMOUNT_REGEX = re.compile(AMOUNT_PATTERN, re.IGNORECASE)

AWARD_KEYWORDS = re.compile(r"premio|award|grant|prize|ayuda|subvenci[oó]n|beca", re.IGNORECASE)
FEE_KEYWORDS = re.compile(r"inscripci[oó]n|registration|entry fee|cuota|pago|tarifa|fee", re.IGNORECASE)
SCALE_MAP = {
    'mil': 1_000,
    'miles': 1_000,
    'millón': 1_000_000,
    'millones': 1_000_000,
    'million': 1_000_000,
}
SCALE_RE = re.compile(r"\s+(mil(?:es)?|mill[oó]n(?:es)?|million)\b", re.IGNORECASE)


def cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.md5(url.encode()).hexdigest() + '.txt')


def fetch_url(url: str) -> str:
    path = cache_path(url)
    if path.exists():
        return path.read_text(errors='ignore')
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.ok and 'text/html' in r.headers.get('Content-Type', ''):
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text(' ', strip=True)
            path.write_text(text)
            time.sleep(SLEEP_BETWEEN)
            return text
    except requests.RequestException:
        pass
    return ''


def iter_amounts(text: str):
    for m in AMOUNT_REGEX.finditer(text):
        span_start = m.start()
        raw_amt = None
        code = None
        if m.group('amt'):
            raw_amt = m.group('amt')
            sym = m.group('symbol') or m.group('after_sym')
            if sym:
                code = {'$': 'USD', 'US$': 'USD', '€': 'EUR', '£': 'GBP', 'R$': 'BRL'}.get(sym, 'USD')
        elif m.group('amt2'):
            raw_amt = m.group('amt2')
            code = m.group('code')
        elif m.group('amt3'):
            raw_amt = m.group('amt3')
            word = m.group('word')
            code = {
                'dolar': 'USD', 'dólar': 'USD', 'dolares': 'USD', 'dólares': 'USD',
                'euro': 'EUR', 'euros': 'EUR',
                'peso': None, 'pesos': None,
                'real': 'BRL', 'reales': 'BRL',
                'soles': 'PEN', 'sol': 'PEN',
                'libras': 'GBP', 'libra': 'GBP',
                'yenes': 'JPY', 'yen': 'JPY',
                'yuanes': 'CNY', 'yuan': 'CNY',
            }.get(word.lower(), None)
        amount = _safe_float(raw_amt)
        if amount is None:
            continue
        # Escalas tipo "30 mil" (palabra inmediatamente después)
        after = text[m.end():m.end()+15].lower()
        mscale = SCALE_RE.match(after)
        if mscale:
            scale_factor = SCALE_MAP.get(mscale.group(1).lower(), 1)
            amount *= scale_factor
        # Si no hay divisa explícita, descartar
        if code is None:
            continue
        yield amount, code, span_start


def classify(span: int, text: str) -> str:
    window = text[max(0, span-80): span+80].lower()
    if FEE_KEYWORDS.search(window):
        return 'fee'
    if AWARD_KEYWORDS.search(window):
        return 'award'
    return 'other'


def process_row(row):
    url = get_url_from_row(row)
    if not isinstance(url, str) or not url.startswith('http'):
        return None, None
    html_text = fetch_url(url)
    if not html_text:
        return None, None
    award_usd = None
    fee_usd = None
    country = row.get('País', '')
    best_award = 0.0
    best_fee = None
    for amount, code, span in iter_amounts(html_text):
        typ = classify(span, html_text)
        # resolver moneda si None
        if code is None:
            code = COUNTRY_CURRENCY.get(country, None)
        usd = convert_to_usd(amount, code) if code else None
        if usd is None:
            continue
        if typ == 'award':
            if usd > best_award:
                best_award = usd
        elif typ == 'fee':
            if best_fee is None or usd < best_fee:
                best_fee = usd
    if best_award > 0:
        award_usd = best_award
    if best_fee is not None:
        fee_usd = best_fee
    return award_usd, fee_usd


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Enriquece CSV con montos web')
    parser.add_argument('--csv', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--limit', type=int, default=None, help='Procesar sólo las primeras N filas (head)')
    parser.add_argument('--tail', type=int, default=None, help='Procesar sólo las últimas N filas')
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    if args.limit is not None:
        df = df.head(args.limit)
    if args.tail is not None:
        df = df.tail(args.tail)
    awards = []
    fees = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        award, fee = process_row(row)
        awards.append(award)
        fees.append(fee)
    df['Premio_USD'] = awards
    df['Inscripcion_USD_web'] = fees
    df['Significativa_400'] = df['Premio_USD'] >= 400
    df.to_csv(args.out, index=False)
    print('Guardado', args.out)


# ------------------------ URL helper ----------------------------


def get_url_from_row(row):
    for col in row.index:
        if 'base url' in col.lower() or col.lower() == 'url':
            val = row[col]
            if isinstance(val, str) and str(val).startswith('http'):
                return str(val).strip()
    return None


if __name__ == '__main__':
    main() 