from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from turfinextract import FinancialInformationExtractor

app = FastAPI(
    title="Turkish Financial Information Extractor API",
    version="0.2.0",
    description="Auditable extraction of structured fields from Turkish financial texts.",
)

extractor = FinancialInformationExtractor()


class ExtractionRequest(BaseModel):
    text: str = Field(..., min_length=1, examples=["120 ay vadeli, %3,19 kâr payı oranlı finansman"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/extract")
def extract(request: ExtractionRequest) -> dict:
    try:
        return extractor.extract(request.text).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
