# Data profile

Rows: 250,000  |  Columns: 17

## Schema and nulls
| column | dtype | nulls | null % | unique |
|---|---|---|---|---|
| transaction_id | object | 0 | 0.00% | 250,000 |
| timestamp | object | 0 | 0.00% | 248,610 |
| transaction_type | object | 0 | 0.00% | 4 |
| merchant_category | object | 0 | 0.00% | 10 |
| amount | int64 | 0 | 0.00% | 10,355 |
| transaction_status | object | 0 | 0.00% | 2 |
| sender_age_group | object | 0 | 0.00% | 5 |
| receiver_age_group | object | 0 | 0.00% | 5 |
| sender_state | object | 0 | 0.00% | 10 |
| sender_bank | object | 0 | 0.00% | 8 |
| receiver_bank | object | 0 | 0.00% | 8 |
| device_type | object | 0 | 0.00% | 3 |
| network_type | object | 0 | 0.00% | 4 |
| fraud_flag | int64 | 0 | 0.00% | 2 |
| hour_of_day | int64 | 0 | 0.00% | 24 |
| day_of_week | object | 0 | 0.00% | 7 |
| is_weekend | int64 | 0 | 0.00% | 2 |

## Duplicates
Fully duplicated rows: 0
Duplicate values in `transaction_id`: 0

## Time coverage
`timestamp`: 2024-01-01 00:05:10 to 2024-12-30 23:55:40 (unparseable: 0)

## Categorical distributions (<= 20 unique values)

**transaction_type**
- P2P: 44.98%
- P2M: 35.06%
- Bill Payment: 14.95%
- Recharge: 5.01%

**merchant_category**
- Grocery: 19.99%
- Food: 14.99%
- Shopping: 11.95%
- Fuel: 10.03%
- Other: 9.93%
- Utilities: 8.94%
- Transport: 8.04%
- Entertainment: 8.04%
- Healthcare: 5.07%
- Education: 3.04%

**transaction_status**
- SUCCESS: 95.05%
- FAILED: 4.95%

**sender_age_group**
- 26-35: 34.97%
- 36-45: 25.15%
- 18-25: 24.94%
- 46-55: 9.94%
- 56+: 5.00%

**receiver_age_group**
- 26-35: 35.15%
- 18-25: 25.04%
- 36-45: 24.86%
- 46-55: 9.93%
- 56+: 5.02%

**sender_state**
- Maharashtra: 14.97%
- Uttar Pradesh: 12.05%
- Karnataka: 11.90%
- Tamil Nadu: 10.15%
- Delhi: 9.95%
- Telangana: 8.97%
- Gujarat: 8.02%
- Andhra Pradesh: 8.00%
- Rajasthan: 7.99%
- West Bengal: 7.99%

**sender_bank**
- SBI: 25.08%
- HDFC: 14.99%
- ICICI: 11.91%
- IndusInd: 10.07%
- Axis: 10.02%
- PNB: 9.98%
- Yes Bank: 9.94%
- Kotak: 8.01%

**receiver_bank**
- SBI: 24.95%
- HDFC: 15.06%
- ICICI: 11.98%
- IndusInd: 10.03%
- Yes Bank: 10.00%
- Axis: 10.00%
- PNB: 9.92%
- Kotak: 8.06%

**device_type**
- Android: 75.11%
- iOS: 19.85%
- Web: 5.04%

**network_type**
- 4G: 59.93%
- 5G: 25.03%
- WiFi: 10.05%
- 3G: 4.99%

**fraud_flag**
- 0: 99.81%
- 1: 0.19%

**day_of_week**
- Monday: 14.60%
- Sunday: 14.40%
- Wednesday: 14.28%
- Tuesday: 14.22%
- Friday: 14.20%
- Thursday: 14.17%
- Saturday: 14.13%

**is_weekend**
- 0: 71.47%
- 1: 28.53%

## Numeric summary
|             |   count |    mean |     std |   min |   50% |     95% |     99% |   max |
|:------------|--------:|--------:|--------:|------:|------:|--------:|--------:|------:|
| amount      |  250000 | 1311.76 | 1848.06 |    10 |   629 | 4687.05 | 9003.01 | 42099 |
| fraud_flag  |  250000 |    0    |    0.04 |     0 |     0 |    0    |    0    |     1 |
| hour_of_day |  250000 |   14.68 |    5.19 |     0 |    15 |   22    |   23    |    23 |
| is_weekend  |  250000 |    0.29 |    0.45 |     0 |     0 |    1    |    1    |     1 |

`amount` <= 0: 0 rows

## What this file can support
- User identifier (needed for retention/cohorts): NOT FOUND
- Failure reason (needed for failure-reason analysis): NOT FOUND
- Timestamp (needed for trends/time intelligence): YES -> timestamp
- Status (success/failed): YES -> transaction_status
- Fraud label: YES -> fraud_flag