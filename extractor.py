import argparse
import json
from pathlib import Path

from turfinextract import FinancialInformationExtractor

FIELDS = [
    "product_name", "financing_amount", "profit_rate", "maturity",
    "fee", "target_audience", "campaign_period"
]


def evaluate(path: Path) -> dict:
    extractor = FinancialInformationExtractor()
    tp = fp = fn = 0
    per_field = {field: {"tp": 0, "fp": 0, "fn": 0} for field in FIELDS}

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        prediction = extractor.extract(item["text"]).to_dict()
        expected = item.get("expected", {})

        for field in FIELDS:
            pred_value = prediction[field]["value"] if prediction[field] else None
            gold_value = expected.get(field)
            if pred_value == gold_value and gold_value is not None:
                tp += 1; per_field[field]["tp"] += 1
            elif pred_value is not None and gold_value is None:
                fp += 1; per_field[field]["fp"] += 1
            elif pred_value is None and gold_value is not None:
                fn += 1; per_field[field]["fn"] += 1
            elif pred_value != gold_value:
                fp += 1; fn += 1
                per_field[field]["fp"] += 1; per_field[field]["fn"] += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "micro": {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)},
        "counts": {"tp": tp, "fp": fp, "fn": fn},
        "per_field": per_field,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/benchmark.jsonl")
    args = parser.parse_args()
    print(json.dumps(evaluate(Path(args.data)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
