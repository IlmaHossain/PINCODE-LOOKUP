# Data: GeoNames Bangladesh postal codes (CC BY 4.0) - https://www.geonames.org
"""Build assets/pincode.db from assets/BD.txt. Rerun after refreshing the source file."""
import csv
import sqlite3
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
SOURCE_PATH = ASSETS_DIR / "BD.txt"
DB_PATH = ASSETS_DIR / "pincode.db"

SCHEMA = """
CREATE TABLE pincodes (
    postal_code TEXT PRIMARY KEY,
    place_name  TEXT NOT NULL DEFAULT '',
    division    TEXT NOT NULL DEFAULT '',
    district    TEXT NOT NULL DEFAULT '',
    upazila     TEXT,
    latitude    REAL,
    longitude   REAL
);
CREATE INDEX idx_pincodes_district ON pincodes(district);
CREATE INDEX idx_pincodes_place_name ON pincodes(place_name);
"""


def main():
    DB_PATH.unlink(missing_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    rows = []
    with SOURCE_PATH.open(encoding="utf-8") as f:
        for line in csv.reader(f, delimiter="\t"):
            postal_code, place_name, division, _, district, _, upazila = line[1:8]
            latitude, longitude = line[9], line[10]

            if not (len(postal_code) == 4 and postal_code.isdigit()):
                print(f"warning: non-4-digit postal code skipped check: {postal_code!r}")

            rows.append((
                postal_code.strip(),
                place_name.strip(),
                division.strip(),
                district.strip(),
                upazila.strip() or None,
                float(latitude) if latitude.strip() else None,
                float(longitude) if longitude.strip() else None,
            ))

    conn.executemany(
        "INSERT INTO pincodes (postal_code, place_name, division, district, upazila, latitude, longitude) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM pincodes").fetchone()[0]
    conn.close()
    print(f"Built {DB_PATH} with {count} pincodes")


if __name__ == "__main__":
    main()
