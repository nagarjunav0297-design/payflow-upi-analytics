# PayFlow — UPI Payments Analytics
Power BI | SQL | Python | Excel

A Power BI dashboard analyzing 250,000 simulated UPI transactions, built to
demonstrate data modelling, SQL, and DAX skills for Data Analyst / Product Analyst roles.

## Data source

[UPI Transactions dataset](https://www.kaggle.com/datasets/skullagos5246/upi-transactions-2024-dataset)
on Kaggle — a **synthetic** dataset simulating realistic UPI transaction patterns across
merchant categories, banks, devices, and networks. Not real production data; see
Limitations below for what that means for the findings.

## Architecture

```
Raw CSV (Kaggle)
      │
      ▼
Python (pandas) ── cleaning, dedup, star-schema split
      │
      ▼
SQL Server ── 8 dimension tables + 1 fact table, indexed, FK-constrained
      │
      ▼
Power BI ── DAX measures, 4-page report
```

**Star schema:** `fact_transactions` (250K rows) links to `dim_date`, `dim_bank`
(shared by sender and receiver, via two relationships — one active, one inactive
and reached with `USERELATIONSHIP`), `dim_age_group`, `dim_state`,
`dim_merchant_category`, `dim_transaction_type`, `dim_device`, `dim_network`.

**Scripts** (run in order):
1. `upi_profile.py` — profiles the raw CSV (schema, nulls, distributions) before modeling
2. `01_clean_and_build_star_schema.py` — cleans and splits into star-schema CSVs
3. `02_create_tables.sql` — creates the SQL Server schema
4. `04_load_to_sql.py` — loads the CSVs into SQL Server
5. `03_analysis_queries.sql` — sample SQL used to validate the model

## Dashboard pages

**1. Executive Overview** — ₹327.94M total volume, 250K transactions, 95% success
rate, ₹1.31K average ticket size, with monthly volume trend and MoM growth.

**2. Payment Performance** — success rate by sender bank and receiver bank side by
side (both ~95%, using an inactive-relationship DAX measure via `USERELATIONSHIP`),
failure rate by network type and transaction type, and an hour-of-day × device
failure-rate heatmap.

**3. Customer Segments** — P2P is the dominant transaction type at 45% (ahead of P2M
at 35%), Shopping leads category volume at 23% (₹76.86M), Maharashtra leads state
volume (₹49M), and average ticket size is broadly flat across age groups.

**4. Fraud and Risk** — 480 fraud cases out of 250,000 transactions (0.19% overall
rate), broadly flat across device, network, and merchant category, with fraud rate
by amount band and hour of day.

## Key techniques demonstrated

- Star-schema modeling with surrogate keys and a dedicated marked Date table
- Dual relationships to one dimension table, resolved in DAX with `USERELATIONSHIP`
  (sender-bank vs. receiver-bank, sender-age vs. receiver-age)
- Time intelligence (`DATEADD`, MoM growth)
- Rare-event / imbalanced-data handling for a 0.19% fraud rate (rate + count shown
  together, not rate alone)
- Calculated columns vs. measures (e.g., amount-band bucketing)
- Data cleaning and validation in Python and SQL before any visualization

## Limitations

- **Synthetic data**: findings describe patterns in the simulated dataset, not real
  UPI behavior. Success/failure and fraud rates appear largely independent of bank,
  device, network, and time in this data — a production dataset would very likely
  show real variation (e.g., from bank-side outages or genuine fraud rings), which is
  worth validating against live data before acting on it.
- **No user identifier** in the source data, so retention, cohorts, and repeat-user
  analysis aren't possible here. That analysis is covered instead in [PROJECT 2 NAME],
  which uses a dataset with user-level history.
- **No failure-reason column**, so failure analysis is limited to rate by segment
  rather than root cause.

## What I'd add with real data

User-level retention and cohort curves, root-cause failure codes, and a check for
whether fraud and failure rates genuinely vary by bank or region (which would point
to specific operational or fraud-ring issues worth investigating).

## Tools

Python (pandas), Microsoft SQL Server, Power BI Desktop (DAX, Power Query)

## Screenshots

See `/screenshots` for all 4 pages.
