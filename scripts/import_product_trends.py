import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.services.database import init_db  # noqa: E402
from app.services.trend_import import import_product_trends_from_content, list_adapter_info  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "product_trends.json"


def main() -> None:
    args = parse_args()
    if args.list_adapters:
        print_available_adapters()
        return

    input_path = Path(args.input).resolve() if args.input else DEFAULT_INPUT
    if not input_path.exists():
        raise FileNotFoundError(f"Trend file not found: {input_path}")

    init_db()
    content = input_path.read_text(encoding="utf-8-sig")
    result = import_product_trends_from_content(
        content=content,
        filename=input_path.name,
        adapter_name=args.adapter,
    )

    print(
        "Imported "
        f"{result['imported_count']} product trend records from {input_path} "
        f"using adapter '{result['adapter']}' "
        f"(auto-mapped: {result['mapped_count']}, generated trend ids: {result['generated_trend_id_count']})"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import product trend signals into SQLite.")
    parser.add_argument("input", nargs="?", default=None, help="Path to a JSON or CSV trend export file.")
    parser.add_argument(
        "--adapter",
        default=None,
        help="Explicitly choose a source adapter. Defaults to auto detection for CSV and generic for JSON.",
    )
    parser.add_argument(
        "--list-adapters",
        action="store_true",
        help="List available source adapters and exit.",
    )
    return parser.parse_args()


def print_available_adapters() -> None:
    for adapter in list_adapter_info():
        print(f"{adapter['name']}: {adapter['description']}")


if __name__ == "__main__":
    main()
