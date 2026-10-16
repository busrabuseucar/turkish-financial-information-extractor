"""Evidence-linked, deterministic extraction for a single financial product."""
import re
from .models import Evidence, FinancialRecord
from .normalization import normalize_date, normalize_maturity, normalize_number, normalize_percentage

MAX_TEXT_LENGTH = 20_000
MONEY = r'(?<![\w.,-])(?P<value>\d[\d.,]*\s*(?:TL\b|₺))'
FEE_WORD = r'(?:tahsis\s+ücreti|masraf\b|ücret(?:i)?\b)'
PERCENT = r'(?P<value>%\s*\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s*%)'


class FinancialInformationExtractor:
    """Return null when absent, invalid or ambiguous under the supported rules."""

    PRODUCT_PATTERNS = [
        re.compile(r'(?P<value>[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü-]*(?:\s+[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü-]*){0,4}\s+(?:Finansmanı|Kredisi|Hesabı|Kartı))'),
    ]
    RATE_PATTERNS = [
        re.compile(PERCENT + r'\s*(?:kâr\s+pay(?:ı|lı)|kar\s+pay(?:ı|lı)|faiz|oran)', re.I),
        re.compile(r'(?:kâr\s+payı|kar\s+payı|faiz|oran)[^.%\n]{0,20}' + PERCENT, re.I),
    ]
    MATURITY_PATTERNS = [re.compile(r'(?P<value>\d+\s*(?:ay|yıl|gün))\b', re.I)]
    TARGET_PATTERNS = [
        re.compile(r'(?P<value>(?:18|21) yaşını doldurmuş(?:[^.!?\n]|\.(?=\d)){0,100})', re.I),
        re.compile(r"(?P<value>emeklilere|öğrencilere|çiftçilere|KOBİ['’]lere|kobilere|yeni müşterilere|bireysel müşterilere)", re.I),
    ]
    DATE_PATTERNS = [
        re.compile(r'(?P<value>\d{1,2}[./-]\d{1,2}[./-]\d{4})'),
        re.compile(r'(?P<value>\d{1,2}\s+(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+\d{4})', re.I),
    ]

    @staticmethod
    def _evidence(text, match, normalizer, score):
        start, end = match.span('value')
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        raw = text[start:end]
        try:
            value = normalizer(raw)
        except ValueError:
            return None
        return Evidence(value, raw, start, end, score)

    @staticmethod
    def _unique(items):
        items = [item for item in items if item is not None]
        # Conflicting values require review; repeated mentions of one value do not.
        return items[0] if items and len({item.value for item in items}) == 1 else None

    def _extract(self, text, patterns, normalizer, confidence):
        return self._unique(self._evidence(text, match, normalizer, confidence)
                            for pattern in patterns for match in pattern.finditer(text))

    def _money(self, text):
        fees, amounts = [], []
        free = re.compile(r'(?P<value>masrafsız|ücretsiz)\b', re.I)
        for match in re.finditer(MONEY, text, re.I):
            # Restrict context to adjacent words in this clause. Never classify a
            # fee as financing just because it is the first currency value.
            before = text[max(0, match.start() - 45):match.start()]
            after = text[match.end():match.end() + 45]
            fee_context = re.search(FEE_WORD + r"(?:\s+(?:ise|olarak))?\s*[:=]?\s*$", before, re.I)
            fee_context = fee_context or re.match(r'\s*' + FEE_WORD, after, re.I)
            target = fees if fee_context else amounts
            target.append(self._evidence(text, match, normalize_number, 0.88 if fee_context else 0.90))
        fees.extend(self._evidence(text, match, lambda _: '0', 0.88)
                    for match in free.finditer(text))
        return self._unique(amounts), self._unique(fees)

    def extract(self, text: str) -> FinancialRecord:
        if not isinstance(text, str) or not text.strip():
            raise ValueError('text must be a non-empty string')
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(f'text must not exceed {MAX_TEXT_LENGTH} characters')
        amount, fee = self._money(text)
        return FinancialRecord(
            product_name=self._extract(text, self.PRODUCT_PATTERNS, str.strip, 0.82),
            financing_amount=amount,
            profit_rate=self._extract(text, self.RATE_PATTERNS, normalize_percentage, 0.94),
            maturity=self._extract(text, self.MATURITY_PATTERNS, normalize_maturity, 0.91),
            fee=fee,
            target_audience=self._extract(text, self.TARGET_PATTERNS, str.strip, 0.76),
            campaign_period=self._extract(text, self.DATE_PATTERNS, normalize_date, 0.87),
        )
