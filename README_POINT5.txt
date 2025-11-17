# Kifagri Point-5 Add‑Ons
How to use:
1) Copy files over your project (matching paths).
2) `alembic upgrade head` (inside backend/) to create tables (requires PostGIS installed).
3) Run API: `uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8080`
4) Test with Postman collection included.
