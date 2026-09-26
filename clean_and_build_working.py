"""
PayFlow step 2: clean the raw UPI CSV and build a star schema.

Usage:  python 01_clean_and_build_star_schema.py upi_transactions_2024.csv
Output: a folder "star_schema_csv" containing:
        dim_date.csv, dim_bank.csv, dim_age_group.csv, dim_state.csv,
        dim_merchant_category.csv, dim_transaction_type.csv,
        dim_device.csv, dim_network.csv, fact_transactions.csv
These are what you load into SQL Server in step 3.
"""
import sys
import os
import pandas as pd

RAW_PATH = sys.argv[1] if len(sys.argv) > 1 else None
OUT_DIR = "star_schema_csv"

if not RAW_PATH:
    sys.exit("Usage: python 01_clean_and_build_star_schema.py <path-to-csv>")

os.makedirs(OUT_DIR, exist_ok=True)


def save(df: pd.DataFrame, name: str) -> None:
    path = os.path.join(OUT_DIR, name)
    df.to_csv(path, index=False)
    print(f"  wrote {path}  ({len(df):,} rows)")


import re


def snake(col: str) -> str:
    col = re.sub(r"\(.*?\)", "", col)            # "amount (INR)" -> "amount"
    return re.sub(r"[^0-9a-zA-Z]+", "_", col).strip("_").lower()


print(f"Reading {RAW_PATH} ...")
df = pd.read_csv(RAW_PATH)
df.columns = [snake(c) for c in df.columns]
print("Columns found:", list(df.columns))
before = len(df)

# ---- 1. Clean --------------------------------------------------------
df = df.drop_duplicates(subset="transaction_id")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])
df = df[df["amount"] > 0]
for c in ["transaction_type", "merchant_category", "transaction_status",
          "sender_age_group", "receiver_age_group", "sender_state",
          "sender_bank", "receiver_bank", "device_type", "network_type",
          "day_of_week"]:
    df[c] = df[c].astype(str).str.strip()

print(f"Cleaning: {before:,} -> {len(df):,} rows "
      f"({before - len(df):,} removed: duplicates, bad timestamps, non-positive amounts)")

df["date"] = df["timestamp"].dt.date

# ---- 2. Dimension tables ---------------------------------------------
print("\nBuilding dimensions...")

dim_date = pd.DataFrame({"date": pd.to_datetime(sorted(df["date"].unique()))})
dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.strftime("%b")
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["day_of_week"] = dim_date["date"].dt.strftime("%A")
dim_date["is_weekend"] = dim_date["date"].dt.dayofweek.isin([5, 6]).astype(int)
dim_date = dim_date[["date_key", "date", "year", "month", "month_name",
                      "quarter", "day_of_week", "is_weekend"]]
save(dim_date, "dim_date.csv")

def make_dim(values, id_col, name_col):
    d = pd.DataFrame({name_col: sorted(pd.unique(values))})
    d.insert(0, id_col, range(1, len(d) + 1))
    return d

dim_bank = make_dim(pd.concat([df["sender_bank"], df["receiver_bank"]]),
                     "bank_id", "bank_name")
save(dim_bank, "dim_bank.csv")

dim_age_group = make_dim(pd.concat([df["sender_age_group"], df["receiver_age_group"]]),
                          "age_group_id", "age_group")
save(dim_age_group, "dim_age_group.csv")

dim_state = make_dim(df["sender_state"], "state_id", "state_name")
save(dim_state, "dim_state.csv")

dim_category = make_dim(df["merchant_category"], "category_id", "category_name")
save(dim_category, "dim_merchant_category.csv")

dim_txn_type = make_dim(df["transaction_type"], "txn_type_id", "txn_type_name")
save(dim_txn_type, "dim_transaction_type.csv")

dim_device = make_dim(df["device_type"], "device_id", "device_type")
save(dim_device, "dim_device.csv")

dim_network = make_dim(df["network_type"], "network_id", "network_type")
save(dim_network, "dim_network.csv")

# ---- 3. Fact table (map text values to surrogate keys) ---------------
print("\nBuilding fact table...")

bank_map = dict(zip(dim_bank["bank_name"], dim_bank["bank_id"]))
age_map = dict(zip(dim_age_group["age_group"], dim_age_group["age_group_id"]))
state_map = dict(zip(dim_state["state_name"], dim_state["state_id"]))
cat_map = dict(zip(dim_category["category_name"], dim_category["category_id"]))
type_map = dict(zip(dim_txn_type["txn_type_name"], dim_txn_type["txn_type_id"]))
device_map = dict(zip(dim_device["device_type"], dim_device["device_id"]))
network_map = dict(zip(dim_network["network_type"], dim_network["network_id"]))

fact = pd.DataFrame({
    "transaction_id": df["transaction_id"],
    "date_key": pd.to_datetime(df["date"]).dt.strftime("%Y%m%d").astype(int),
    "hour_of_day": df["hour_of_day"],
    "sender_bank_id": df["sender_bank"].map(bank_map),
    "receiver_bank_id": df["receiver_bank"].map(bank_map),
    "sender_age_group_id": df["sender_age_group"].map(age_map),
    "receiver_age_group_id": df["receiver_age_group"].map(age_map),
    "sender_state_id": df["sender_state"].map(state_map),
    "category_id": df["merchant_category"].map(cat_map),
    "txn_type_id": df["transaction_type"].map(type_map),
    "device_id": df["device_type"].map(device_map),
    "network_id": df["network_type"].map(network_map),
    "amount": df["amount"],
    "transaction_status": df["transaction_status"],
    "is_success": (df["transaction_status"].str.upper() == "SUCCESS").astype(int),
    "fraud_flag": df["fraud_flag"].astype(int),
})
save(fact, "fact_transactions.csv")

print("\nDone. Star schema CSVs are in the 'star_schema_csv' folder.")
print("Next: run 02_create_tables.sql in SQL Server, then load these CSVs "
      "using the Import Flat File wizard (or BULK INSERT).")
