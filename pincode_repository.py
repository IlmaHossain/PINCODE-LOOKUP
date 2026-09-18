import sqlite3
from pathlib import Path

from models import LocationResponse

DB_PATH = Path(__file__).parent / "assets" / "pincode.db"

if not DB_PATH.exists():
    raise RuntimeError(
        f"{DB_PATH} not found - run `uv run python scripts/build_pincode_db.py` first."
    )

_SELECT_COLS = "postal_code, place_name, division, district, upazila, latitude, longitude"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_location(row: sqlite3.Row) -> LocationResponse:
    return LocationResponse(
        pincode=row["postal_code"],
        city=row["place_name"],
        state=row["division"],
        district=row["district"],
        upazila=row["upazila"],
        latitude=row["latitude"],
        longitude=row["longitude"],
    )


def get_by_pincode(code: str) -> LocationResponse | None:
    conn = _connect()
    try:
        row = conn.execute(
            f"SELECT {_SELECT_COLS} FROM pincodes WHERE postal_code = ?", (code,)
        ).fetchone()
    finally:
        conn.close()
    return _row_to_location(row) if row else None

def get_by_district(district: str) -> list[LocationResponse]:
    conn = _connect()
    try:
        rows = conn.execute(
            f"SELECT {_SELECT_COLS} FROM pincodes WHERE district = ? COLLATE NOCASE", (district,)
        ).fetchall()
    finally:
        conn.close()
    return [_row_to_location(row) for row in rows]

def get_many(codes: list[str]) -> list[LocationResponse]:
    if not codes:
        return []
    conn = _connect()
    try:
        placeholders = ",".join("?" for _ in codes)
        rows = conn.execute(
            f"SELECT {_SELECT_COLS} FROM pincodes WHERE postal_code IN ({placeholders})",
            codes,
        ).fetchall()
    finally:
        conn.close()
    by_code = {row["postal_code"]: _row_to_location(row) for row in rows}
    return [by_code[c] for c in codes if c in by_code]
