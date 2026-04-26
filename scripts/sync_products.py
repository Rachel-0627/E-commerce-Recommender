from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.sample_data import PRODUCT_SYNC_SOURCES  # noqa: E402
from app.services.database import init_db, seed_product_sync_sources  # noqa: E402
from app.services.product_sync import run_all_product_sync_sources, run_product_sync_source  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run configured product sync sources.")
    parser.add_argument("--source-id", default=None, help="Run a single product sync source by id")
    parser.add_argument("--all", action="store_true", help="Run all sync sources, including disabled ones")
    args = parser.parse_args()

    init_db()
    seed_product_sync_sources(PRODUCT_SYNC_SOURCES)

    if args.source_id:
        result = run_product_sync_source(args.source_id)
        print(
            f"[{result.status}] {result.source_id} "
            f"imported={result.imported_count} total={result.total_count} "
            f"adapter={result.adapter or 'auto'} message={result.message or ''}"
        )
        return

    response = run_all_product_sync_sources(enabled_only=not args.all)
    print(
        f"Ran {response.total_sources} sync sources "
        f"(success={response.success_count}, error={response.error_count})"
    )
    for item in response.items:
        print(
            f"- [{item.status}] {item.source_id} "
            f"imported={item.imported_count} total={item.total_count} "
            f"adapter={item.adapter or 'auto'}"
        )


if __name__ == "__main__":
    main()
