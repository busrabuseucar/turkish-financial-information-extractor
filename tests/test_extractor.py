import pytest
from turfinextract import FinancialInformationExtractor
from turfinextract.normalization import normalize_date, normalize_number

extract = FinancialInformationExtractor().extract


def test_sample_fields_and_exact_evidence():
    text = "Bereket Konut Finansmanı kampanyası kapsamında yeni müşterilere 2.500.000 TL'ye kadar, 120 ay vadeli ve %3,19 kâr payı oranlı finansman sunulmaktadır. Tahsis ücreti 5.000 TL'dir. Kampanya 31.12.2026 tarihine kadar geçerlidir."
    record = extract(text).to_dict()
    expected = dict(product_name='Bereket Konut Finansmanı', financing_amount='2500000', maturity='120 month', profit_rate='%3.19', fee='5000', target_audience='yeni müşterilere', campaign_period='2026-12-31')
    assert {key: value['value'] for key, value in record.items()} == expected
    for value in record.values():
        assert text[value['start']:value['end']] == value['source_text']
        assert 0 <= value['confidence'] <= 1


@pytest.mark.parametrize('text,amount,fee', [
    ("Tahsis ücreti 2.500 TL'dir.", None, '2500'),
    ("Ücret 1.000 ₺, finansman üst limiti 200.000 ₺'dir.", '200000', '1000'),
    ('90 gün vadeli ve 5.000 TL masrafsız mikro finansman.', '5000', '0'),
    ('1.000 TL tahsis ücreti.', None, '1000'),
    ('100.000 TL kredi ve 200.000 TL kredi.', None, None),
    ('100.000 TL kredi. Üst limit 100.000 TL.', '100000', None),
])
def test_money_context_and_ambiguity(text, amount, fee):
    r = extract(text)
    assert (r.financing_amount.value if r.financing_amount else None) == amount
    assert (r.fee.value if r.fee else None) == fee


@pytest.mark.parametrize('raw,expected', [('1.250,50 TL', '1250.5'), ('1250,50 ₺', '1250.5'), ('2.500.000 TL', '2500000'), ('0 TL', '0'), ('12.50 TL', '12.5')])
def test_numbers(raw, expected):
    assert normalize_number(raw) == expected


@pytest.mark.parametrize('raw', ['31.02.2026', '29 Şubat 2025', '01/13/2026'])
def test_invalid_calendar_dates(raw):
    with pytest.raises(ValueError):
        normalize_date(raw)
    assert extract('Kampanya ' + raw + ' tarihinde biter.').campaign_period is None


def test_leap_day_and_conflicting_dates():
    assert normalize_date('29 Şubat 2024') == '2024-02-29'
    assert extract('01.01.2026 - 31.12.2026 kampanyası').campaign_period is None


@pytest.mark.parametrize('text', ['', '   ', None, 'x' * 20001])
def test_invalid_input(text):
    with pytest.raises(ValueError):
        extract(text)


def test_unknown_text_and_zero_maturity():
    assert all(value is None for value in extract('Ürün yalnızca mobil kanaldan sunulmaktadır.').to_dict().values())
    assert extract('0 ay vadeli ürün').maturity is None


def test_rate_is_not_discount_and_precision_preserved():
    assert extract('%25 indirim uygulanır').profit_rate is None
    assert extract('%3,10 kâr payı').profit_rate.value == '%3.10'


def test_offsets_survive_leading_whitespace():
    text = '   120 ay vadeli ve 200.000 TL finansman'
    for evidence in extract(text).to_dict().values():
        if evidence:
            assert text[evidence['start']:evidence['end']] == evidence['source_text']

def test_target_clause_preserves_thousands_separator():
    text = '18 yaşını doldurmuş yeni müşteriler için 20.000 TL destek.'
    assert extract(text).target_audience.value == text[:-1]


def test_large_amount_has_no_decimal_context_rounding():
    value = '1234567890123456789012345678901234567890'
    assert normalize_number(value + ' TL') == value
