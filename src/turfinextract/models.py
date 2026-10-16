from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Evidence:
    value: str
    source_text: str
    start: int
    end: int
    confidence: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FinancialRecord:
    product_name: Optional[Evidence] = None
    financing_amount: Optional[Evidence] = None
    profit_rate: Optional[Evidence] = None
    maturity: Optional[Evidence] = None
    fee: Optional[Evidence] = None
    target_audience: Optional[Evidence] = None
    campaign_period: Optional[Evidence] = None

    def to_dict(self) -> dict:
        return {
            "product_name": self.product_name.to_dict() if self.product_name else None,
            "financing_amount": self.financing_amount.to_dict() if self.financing_amount else None,
            "profit_rate": self.profit_rate.to_dict() if self.profit_rate else None,
            "maturity": self.maturity.to_dict() if self.maturity else None,
            "fee": self.fee.to_dict() if self.fee else None,
            "target_audience": self.target_audience.to_dict() if self.target_audience else None,
            "campaign_period": self.campaign_period.to_dict() if self.campaign_period else None,
        }
