"""
PayFlow step 3b: load the star_schema_csv files into SQL Server.

Run this AFTER 02_create_tables.sql has created the 9 empty tables.

Install requirements first (one time):
    pip install pandas sqlalchemy pyodbc

Usage:
    python 04_load_to_sql.py
(run it from inside your PayFlow folder, so it can find star_schema_csv)
"""
import os
import pandas as pd
from sqlalchemy import create_engine

# ---- connection settings ----------------------------------------------
SERVER = "localhost"          # change to "localhost\\SQLEXPRESS" if that's your instance
DATABASE = "PayFlow"
DRIVER = "ODBC Driver 17 for SQL Server"   # try "ODBC Driver 18 for SQL Server" if this fails

CONN_STR = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER.replace(' ', '+')}"
    f"&trusted_connection=yes"
    f"&TrustServerCertificate=yes"
)

# Load order matters: dimensions first, fact table last (foreign keys)
LOAD_ORDER = [
    "dim_date",
    "dim_bank",
    "dim_age_group",
    "dim_state",
    "dim_merchant_category",
    "dim_transaction_type",
    "dim_device",
    "dim_network",
    "fact_transactions",
]

CSV_DIR = "star_schema_csv"


def main():
    if not os.path.isdir(CSV_DIR):
        raise SystemExit(
            f"Can't find the '{CSV_DIR}' folder. Run this script from inside "
            "your PayFlow folder, and make sure step 2 has been run."
        )

    engine = create_engine(CONN_STR)

    with engine.connect() as conn:
        print(f"Connected to {SERVER}/{DATABASE}")

    for table in LOAD_ORDER:
        csv_path = os.path.join(CSV_DIR, f"{table}.csv")
        if not os.path.exists(csv_path):
            print(f"  SKIP {table}: {csv_path} not found")
            continue

        df = pd.read_csv(csv_path)
        df.to_sql(table, engine, if_exists="append", index=False, chunksize=5000)
        print(f"  loaded {table}: {len(df):,} rows")

    print("\nDone. Run a SELECT COUNT(*) on each table in VS Code to double-check.")


if __name__ == "__main__":
    main()
