"""Walmart Forage Task 4: combine shipping CSVs into the supplied SQLite schema.

Place this file beside shipment_database.db and the data/ folder in the
official starter repository. Requires only Python's standard library.

The original starter database is preserved. A new database file named
shipment_database_populated.db is created containing the imported data.
"""

import csv
import shutil
import sqlite3
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SOURCE_DB = BASE_DIR / "shipment_database.db"
OUTPUT_DB = BASE_DIR / "shipment_database_populated.db"


def read_csv(filename, required_columns):
    """Read a CSV as dictionaries, validating columns before importing."""
    path = DATA_DIR / filename
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = set(required_columns) - columns
        if missing:
            raise ValueError(f"{filename}: missing columns {sorted(missing)}")
        return list(reader)


def require_schema(connection):
    """Check the expected tables/fields in the provided SQLite database."""
    expected = {
        "product": {"id", "name"},
        "shipment": {"product_id", "quantity", "origin", "destination"},
    }
    for table, required in expected.items():
        columns = {
            row[1] for row in connection.execute(f"PRAGMA table_info({table})")
        }
        missing = required - columns
        if missing:
            raise ValueError(f"Database table {table!r} lacks {sorted(missing)}")


def product_id(cursor, product_name, cache):
    """Create each product once and reuse its database ID."""
    if product_name not in cache:
        cursor.execute(
            "INSERT OR IGNORE INTO product (name) VALUES (?)", (product_name,)
        )
        cursor.execute("SELECT id FROM product WHERE name = ?", (product_name,))
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"Product lookup failed: {product_name}")
        cache[product_name] = result[0]
    return cache[product_name]


def add_shipment(cursor, product, quantity, origin, destination, cache):
    """Write one row per product in a shipment using a foreign-key ID."""
    cursor.execute(
        """INSERT INTO shipment (product_id, quantity, origin, destination)
           VALUES (?, ?, ?, ?)""",
        (product_id(cursor, product, cache), quantity, origin, destination),
    )


def prepare_rows():
    """Return normalized rows from CSV 0 and the joined CSVs 1 and 2."""
    sheet0 = read_csv(
        "shipping_data_0.csv",
        {"origin_warehouse", "destination_store", "product", "product_quantity"},
    )
    sheet1 = read_csv("shipping_data_1.csv", {"shipment_identifier", "product"})
    sheet2 = read_csv(
        "shipping_data_2.csv",
        {"shipment_identifier", "origin_warehouse", "destination_store"},
    )

    # File 0 is self-contained: its quantity is already a number.
    normalized = [
        (
            row["product"],
            int(row["product_quantity"]),
            row["origin_warehouse"],
            row["destination_store"],
        )
        for row in sheet0
    ]
    direct_count = len(normalized)

    # File 2 gives the location information for each shipment ID in file 1.
    routes = {
        row["shipment_identifier"]: (
            row["origin_warehouse"], row["destination_store"]
        )
        for row in sheet2
    }

    # File 1 has one physical product unit per row. Repeated (ID, product)
    # combinations are counted together into a quantity.
    counts = Counter(
        (row["shipment_identifier"], row["product"]) for row in sheet1
    )
    for (shipment_identifier, product), quantity in counts.items():
        if shipment_identifier not in routes:
            raise ValueError(f"No route for shipment {shipment_identifier}")
        origin, destination = routes[shipment_identifier]
        normalized.append((product, quantity, origin, destination))

    return normalized, direct_count, len(sheet1), len(sheet2)


def main():
    if not SOURCE_DB.is_file():
        raise FileNotFoundError(f"Starter database not found: {SOURCE_DB}")
    if OUTPUT_DB.exists():
        raise FileExistsError(
            f"{OUTPUT_DB.name} already exists. Rename or remove it to rerun."
        )

    records, direct_count, product_rows, route_rows = prepare_rows()
    shutil.copy2(SOURCE_DB, OUTPUT_DB)  # Do not modify the starter database.
    try:
        with sqlite3.connect(OUTPUT_DB) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            require_schema(connection)
            cursor = connection.cursor()
            cache = {}
            for product, quantity, origin, destination in records:
                add_shipment(cursor, product, quantity, origin, destination, cache)
            # Context manager commits all inserts or rolls them back on error.
    except Exception:
        OUTPUT_DB.unlink(missing_ok=True)
        raise

    print(f"Read {direct_count} records from shipping_data_0.csv")
    print(f"Grouped {product_rows} rows from shipping_data_1.csv")
    print(f"Matched routes from {route_rows} rows of shipping_data_2.csv")
    print(f"Inserted {len(records)} shipment-product rows")
    print(f"Output database: {OUTPUT_DB}")


if __name__ == "__main__":
    main()
