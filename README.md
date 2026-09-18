# Pincode LookUp

FastAPI service for looking up Bangladesh postal codes (city, division/state, district, upazila, coordinates).

## Run

```bash
uv sync
uv run uvicorn main:app --reload
```

## Data

Postal code data lives in `assets/pincode.db` (SQLite), built from `assets/BD.txt` via:

```bash
uv run python scripts/build_pincode_db.py
```

Source: [GeoNames.org](https://www.geonames.org/) Bangladesh postal code extract, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Covers 1,349 postal codes across all
divisions, districts and upazilas of Bangladesh.

## Endpoints

- `GET /pincode/{code}` — look up a single 4-digit pincode
- `GET /pincode/district/{district}` — list all pincodes in a district (case-insensitive, e.g. `dhaka`)
- `POST /pincode/bulk` — look up up to 20 pincodes at once
