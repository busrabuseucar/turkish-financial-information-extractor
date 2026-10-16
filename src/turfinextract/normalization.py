"""Strict normalization for the supported Turkish notation."""
import re
from datetime import date
from decimal import Decimal

_MONTHS = {name: i for i, name in enumerate(
    ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran',
     'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık'], 1)}


def normalize_number(raw: str) -> str:
    value = re.sub(r'(?i)TL|₺|\s', '', raw)
    if not re.fullmatch(r'(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d+)?|\d+\.\d{1,2}', value):
        raise ValueError('Unsupported monetary notation')
    if ',' in value:
        value = value.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(?:\.\d{3})+', value):
        value = value.replace('.', '')
    rendered = format(Decimal(value), 'f')
    return rendered.rstrip('0').rstrip('.') if '.' in rendered else rendered


def normalize_percentage(raw: str) -> str:
    value = re.sub(r'[%\s]', '', raw).replace(',', '.')
    if not re.fullmatch(r'\d+(?:\.\d+)?', value):
        raise ValueError('Invalid percentage')
    # Preserve quoted decimal precision, e.g. %3,10 -> %3.10.
    return '%' + value


def normalize_maturity(raw: str) -> str:
    m = re.fullmatch(r'\s*(\d+)\s*(ay|yıl|gün)\s*', raw, re.I)
    if not m or int(m[1]) == 0:
        raise ValueError('Invalid maturity')
    return f"{int(m[1])} " + {'ay': 'month', 'yıl': 'year', 'gün': 'day'}[m[2].lower()]


def normalize_date(raw: str) -> str:
    text = raw.strip().replace('İ', 'i').lower()
    numeric = re.fullmatch(r'(\d{1,2})[./-](\d{1,2})[./-](\d{4})', text)
    if numeric:
        day, month, year = map(int, numeric.groups())
    else:
        named = re.fullmatch(r'(\d{1,2})\s+(\w+)\s+(\d{4})', text)
        if not named or named[2] not in _MONTHS:
            raise ValueError('Unsupported date')
        day, month, year = int(named[1]), _MONTHS[named[2]], int(named[3])
    return date(year, month, day).isoformat()
