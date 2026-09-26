"""
PayFlow step 1: profile the raw UPI CSV before any modelling.

Usage:  python upi_profile.py path/to/upi_transactions_2024.csv
Output: prints a report and saves it to data_profile.md

The script does not assume exact column names. It normalises them to
snake_case and then checks what the file can support.
"""
import re
import sys
import pandas as pd


def snake(col: str) -> str:
    col = re.sub(r"\(.*?\)", "", col)            # "amount (INR)" -> "amount"
    return re.sub(r"[^0-9a-zA-Z]+", "_", col).strip("_").lower()


def find(cols, *keywords):
    return [c for c in cols if any(k in c for k in keywords)]


def main(path: str) -> None:
    raw = pd.read_csv(path)
    df = raw.copy()
    df.columns = [snake(c) for c in df.columns]
    out = []
    add = out.append

    add("# Data profile\n")
    add(f"Rows: {len(df):,}  |  Columns: {df.shape[1]}\n")

    add("## Schema and nulls")
    add("| column | dtype | nulls | null % | unique |")
    add("|---|---|---|---|---|")
    for c in df.columns:
        n = int(df[c].isna().sum())
        add(f"| {c} | {df[c].dtype} | {n:,} | {n / len(df):.2%} | {df[c].nunique():,} |")

    add("\n## Duplicates")
    add(f"Fully duplicated rows: {int(df.duplicated().sum()):,}")
    for c in find(df.columns, "transaction_id", "txn_id"):
        add(f"Duplicate values in `{c}`: {int(df[c].duplicated().sum()):,}")

    add("\n## Time coverage")
    time_cols = find(df.columns, "timestamp", "date", "time")
    time_cols = [c for c in time_cols if not pd.api.types.is_numeric_dtype(df[c])]
    for c in time_cols:
        parsed = pd.to_datetime(df[c], errors="coerce")
        if parsed.notna().mean() > 0.9:
            add(f"`{c}`: {parsed.min()} to {parsed.max()} "
                f"(unparseable: {int(parsed.isna().sum()):,})")
    if not time_cols:
        add("No text timestamp column found (check for numeric date parts).")

    add("\n## Categorical distributions (<= 20 unique values)")
    for c in df.columns:
        if df[c].nunique() <= 20:
            shares = df[c].value_counts(normalize=True, dropna=False).round(4)
            add(f"\n**{c}**")
            for k, v in shares.items():
                add(f"- {k}: {v:.2%}")

    add("\n## Numeric summary")
    num = df.select_dtypes("number")
    if not num.empty:
        add(num.describe(percentiles=[.5, .95, .99]).T.round(2).to_markdown())
    for c in find(num.columns, "amount"):
        add(f"\n`{c}` <= 0: {int((num[c] <= 0).sum()):,} rows")

    add("\n## What this file can support")
    checks = {
        "User identifier (needed for retention/cohorts)": find(df.columns, "user", "customer", "sender_id", "upi_id"),
        "Failure reason (needed for failure-reason analysis)": find(df.columns, "reason", "error", "failure"),
        "Timestamp (needed for trends/time intelligence)": find(df.columns, "timestamp", "date"),
        "Status (success/failed)": find(df.columns, "status"),
        "Fraud label": find(df.columns, "fraud"),
    }
    for label, hits in checks.items():
        add(f"- {label}: {'YES -> ' + ', '.join(hits) if hits else 'NOT FOUND'}")

    report = "\n".join(out)
    print(report)
    with open("data_profile.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\nSaved to data_profile.md")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python upi_profile.py <path-to-csv>")
    main(sys.argv[1])
