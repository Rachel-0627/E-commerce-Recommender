# Backend

FastAPI backend for the e-commerce recommendation and AI explanation MVP.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /api/users/{user_id}`
- `GET /api/products`
- `GET /api/recommendations?user_id=u_001&scene=home&limit=5`
