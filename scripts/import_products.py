from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.database import init_db  # noqa: E402
from app.services.product_import import import_products_from_content, list_product_adapter_info  # noqa: E402


DEFAULT_INPUT = ROOT / "data" / "product_source_catalog.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Import product source data into SQLite.")
    parser.add_argument("input", nargs="?", default=str(DEFAULT_INPUT), help="Path to a JSON or CSV file")
    parser.add_argument("--adapter", default=None, help="Adapter name to force")
    parser.add_argument("--list-adapters", action="store_true", help="List available adapters and exit")
    args = parser.parse_args()

    if args.list_adapters:
        for adapter in list_product_adapter_info():
            print(f"{adapter['name']}: {adapter['description']}")
        return

    input_path = Path(args.input).expanduser().resolve()
    content = input_path.read_text(encoding="utf-8")

    init_db()
    result = import_products_from_content(
        content=content,
        filename=input_path.name,
        adapter_name=args.adapter,
    )
    print(
        f"Imported {result['imported_count']} products "
        f"(adapter={result['adapter']}, generated_ids={result['generated_product_id_count']})"
    )


if __name__ == "__main__":
    main()
