# Data

This directory stores generated seed data for local recommendation experiments.

Generate the sample behavior log with:

```bash
python3 scripts/generate_sample_events.py
```

The generated `events.json` file is used by the backend ItemCF recommender as seed behavior data. Runtime events submitted from the frontend are merged with this seed data in memory.

Sample trend signals can be imported with:

```bash
python3 scripts/import_product_trends.py
```

The default input file is:

```text
data/product_trends.json
```

You can also import a CSV-style market export:

```bash
python3 scripts/import_product_trends.py data/product_trends_market_export.csv
```

When `product_id` is missing, the import script will try to auto-map rows to existing products by `keyword` and `category`.

Available source adapters:

```bash
python3 scripts/import_product_trends.py --list-adapters
```

## Product source samples

Example product source files:

- `data/product_source_catalog.json`
- `data/product_catalog_market_export.csv`
- `data/amazon_bestsellers_export.csv`
- `data/shopify_products_export.csv`
- `data/jd_catalog_export.csv`

Import them with:

```bash
python3 scripts/import_products.py
python3 scripts/import_products.py data/product_catalog_market_export.csv --adapter ecommerce_catalog
```

Example adapter-specific inputs:

```text
data/google_trends_export.csv
data/ecommerce_rank_export.csv
```

Runtime data is stored in:

```text
data/app.sqlite3
```

The SQLite database contains users, products, product trend signals, frontend events, recommendation logs, and explanation feedback. It is generated locally and ignored by git.
