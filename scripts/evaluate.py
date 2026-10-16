"""Evaluate the recovered synthetic development fixture, never a held-out claim."""
import argparse
import hashlib
import json
from pathlib import Path
from turfinextract import FinancialInformationExtractor

FIELDS = ['product_name', 'financing_amount', 'profit_rate', 'maturity',
          'fee', 'target_audience', 'campaign_period']


def evaluate(path: Path) -> dict:
    raw = path.read_bytes()
    items = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    if not items:
        raise ValueError('Evaluation dataset is empty')
    extractor = FinancialInformationExtractor()
    counts = {field: dict(tp=0, fp=0, fn=0) for field in FIELDS}
    mismatches = []
    for item in items:
        predicted = extractor.extract(item['text']).to_dict()
        expected = item['expected']
        for field in FIELDS:
            actual = predicted[field]['value'] if predicted[field] else None
            gold = expected.get(field)
            # Exact values, including original case; no silent label rewriting.
            if actual == gold:
                if gold is not None:
                    counts[field]['tp'] += 1
            else:
                if actual is not None:
                    counts[field]['fp'] += 1
                if gold is not None:
                    counts[field]['fn'] += 1
                mismatches.append(dict(id=item['id'], field=field, expected=gold, actual=actual))
    def metrics(c):
        precision = c['tp'] / (c['tp'] + c['fp']) if c['tp'] + c['fp'] else 0
        recall = c['tp'] / (c['tp'] + c['fn']) if c['tp'] + c['fn'] else 0
        return dict(**c, precision=round(precision, 4), recall=round(recall, 4),
                    f1=round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0)
    totals = {key: sum(c[key] for c in counts.values()) for key in ['tp', 'fp', 'fn']}
    return dict(scope='synthetic development fixture; not held-out evaluation',
                examples=len(items), dataset_sha256=hashlib.sha256(raw).hexdigest(),
                matching='exact field values; original case preserved',
                micro=metrics(totals), per_field={f: metrics(c) for f, c in counts.items()}, mismatches=mismatches)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1] / 'data/benchmark.jsonl')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(args.data)
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')


if __name__ == '__main__':
    main()
