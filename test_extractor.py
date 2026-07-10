import argparse
import json

from .extractor import FinancialInformationExtractor


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structured information from Turkish financial texts.")
    parser.add_argument("text", help="Turkish banking or campaign text")
    args = parser.parse_args()

    record = FinancialInformationExtractor().extract(args.text)
    print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
