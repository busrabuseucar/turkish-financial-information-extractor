# Turkish Financial Information Extractor

A compact, auditable NLP project that extracts structured information from Turkish banking, financing, and campaign texts.

The project focuses on a practical problem: financial product information is frequently published as unstructured prose, while comparison and decision-support systems require normalized fields.

## Why this project exists

A naive language-model prompt can produce plausible JSON, but it can also invent values. This project takes a stricter approach:

- Every extracted value is linked to its source span.
- Missing information remains `null` instead of being guessed.
- Numeric, percentage, maturity, and date values are normalized.
- Confidence scores are returned with each field.
- The code is modular and testable.

## Extracted fields

- Product name
- Financing amount
- Profit rate
- Maturity
- Fee
- Target audience
- Campaign period

## Architecture

```text
Turkish financial text
        ↓
Pattern and context detection
        ↓
Field-specific normalization
        ↓
Evidence span + confidence score
        ↓
Auditable JSON record
```

## Example

Input:

```text
Bereket Konut Finansmanı kampanyası kapsamında yeni müşterilere 2.500.000 TL'ye kadar, 120 ay vadeli ve %3,19 kâr payı oranlı finansman sunulmaktadır. Tahsis ücreti 5.000 TL'dir. Kampanya 31.12.2026 tarihine kadar geçerlidir.
```

Output excerpt:

```json
{
  "financing_amount": {
    "value": "2500000",
    "source_text": "2.500.000 TL",
    "confidence": 0.90
  },
  "profit_rate": {
    "value": "%3.19",
    "source_text": "%3,19",
    "confidence": 0.94
  },
  "maturity": {
    "value": "120 month",
    "source_text": "120 ay",
    "confidence": 0.91
  }
}
```


## What is included in v0.2

- Evidence-linked rule-based extraction
- 30-example labeled benchmark set
- Field-level evaluation script with Precision, Recall, and F1
- FastAPI service with `/health` and `/extract` endpoints
- Streamlit demo with JSON export and evidence table
- Unit and API tests

## Run the benchmark

```bash
python scripts/evaluate.py --data data/benchmark.jsonl
```

The benchmark is intentionally small and transparent. It is a project validation set, not a claim of production-grade model performance.

## Run the REST API

```bash
uvicorn app.api:app --reload
```

Open the automatically generated API documentation at `http://127.0.0.1:8000/docs`.

## Run the Streamlit demo

```bash
streamlit run app/streamlit_app.py
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/turkish-financial-information-extractor.git
cd turkish-financial-information-extractor
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -e .
pip install -r requirements.txt
```

## Usage

```bash
turfinextract "120 ay vadeli, %3,19 kâr payı oranlı ve 2.500.000 TL'ye kadar finansman"
```

Or from Python:

```python
from turfinextract import FinancialInformationExtractor

text = "120 ay vadeli ve %3,19 kâr payı oranlı finansman"
record = FinancialInformationExtractor().extract(text)
print(record.to_dict())
```

## Tests

```bash
pytest
```

## Current limitations

- The first version uses interpretable rules instead of a trained transformer model.
- Ambiguous product names and long cross-sentence dependencies may require a model-based layer.
- Confidence scores are heuristic and should later be calibrated on a labeled dataset.

## Roadmap

- Add a labeled Turkish financial-product dataset.
- Compare rule-based, transformer, and LLM-assisted extraction.
- Add field-level Precision, Recall, and F1 metrics.
- Add URL, retrieval date, and document-version metadata.
- Add a lightweight REST API and dashboard.
- Add optional local-LLM validation without sending data to external services.

## Ethics and reliability

This project does not generate financial advice. It structures publicly available product information and keeps evidence attached to every extracted value. Users should verify critical details from the original source.

## License

MIT
