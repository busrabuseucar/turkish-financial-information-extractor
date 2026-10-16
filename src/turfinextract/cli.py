"""Command-line JSON output; errors go to stderr with exit code 2."""
import argparse
import json
from .extractor import FinancialInformationExtractor


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract evidence-linked fields from one Turkish financial text.')
    parser.add_argument('text', help='Turkish banking or campaign text (max 20,000 characters)')
    args = parser.parse_args()
    try:
        record = FinancialInformationExtractor().extract(args.text)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
