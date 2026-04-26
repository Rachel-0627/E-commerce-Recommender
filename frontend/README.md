# Frontend

Static frontend for the e-commerce recommendation and AI explanation MVP.

## Run

Start the backend first:

```bash
cd ../backend
python3 -m uvicorn app.main:app --reload
```

Then start the frontend:

```bash
python3 -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

## Features

- Two-step flow: direction page -> product recommendation page
- Back navigation from product page to direction page
- Direct entry to general product recommendations without choosing a direction
- User selector
- Recommendation scene selector
- Product cards with images
- Product detail dialog
- Recommendation score
- Recommendation source
- Reason tags
- AI explanation text
- Explanation provider label
- Explanation feedback buttons
- User behavior tracking for click, view, favorite, add to cart, and dislike
- Runtime analytics dashboard with impressions, CTR, add-to-cart rate, explanation feedback rate, and top products
- Trend source management section with source/category filters and product mapping visibility
- Manual correction of unmapped trend records by selecting a product and saving the mapping
- Direct editing of trend score and sales score, plus deletion of a trend record
- Manual creation of a new trend record from the frontend
- Batch import entry that accepts JSON/CSV files or pasted export content
- Import preview with row-level validation, auto-mapping visibility, and error reporting before the real import
- Trend import preview now includes template recognition, detected headers, field mapping presets, and unused fields
- Product source import section with source/category filters
- Product source batch import that accepts JSON/CSV files or pasted export content
- Product import preview with generated product IDs, source metadata, and row-level error reporting
- Product sync section for maintaining repeatable sync sources, triggering single-source syncs, and running all enabled sources
- Import history section that records previews/imports for products and trends, including adapter, filename, counts, and errors
- Product management section for filtering, creating, and updating product records directly from the frontend
- User profile management section for filtering, creating, and updating user profiles directly from the frontend
- Direction management section for filtering, creating, updating direction metadata, and maintaining each direction's linked product IDs
- Direction product layering inside the product page, with roles such as 入门款 / 核心商品 / 搭配款 reflected from the maintained direction-product mapping
