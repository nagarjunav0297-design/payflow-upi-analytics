-- PayFlow step 4 (preview): sample analysis queries.
-- Run these after loading data, just to sanity-check the model.
-- These also double as evidence of SQL skill for interviews.

-- 1. Monthly volume and value trend
SELECT d.[year], d.[month], d.month_name,
       COUNT(*) AS txn_count,
       SUM(f.amount) AS total_value,
       CAST(SUM(f.is_success) AS FLOAT) / COUNT(*) AS success_rate
FROM fact_transactions f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.[year], d.[month], d.month_name
ORDER BY d.[year], d.[month];

-- 2. Success rate by sender bank -> receiver bank pair
SELECT sb.bank_name AS sender_bank, rb.bank_name AS receiver_bank,
       COUNT(*) AS txn_count,
       CAST(SUM(f.is_success) AS FLOAT) / COUNT(*) AS success_rate
FROM fact_transactions f
JOIN dim_bank sb ON f.sender_bank_id = sb.bank_id
JOIN dim_bank rb ON f.receiver_bank_id = rb.bank_id
GROUP BY sb.bank_name, rb.bank_name
ORDER BY success_rate ASC;

-- 3. Failure rate by hour of day and device (for the heatmap page)
SELECT f.hour_of_day, dv.device_type,
       COUNT(*) AS txn_count,
       CAST(SUM(1 - f.is_success) AS FLOAT) / COUNT(*) AS failure_rate
FROM fact_transactions f
JOIN dim_device dv ON f.device_id = dv.device_id
GROUP BY f.hour_of_day, dv.device_type
ORDER BY f.hour_of_day;

-- 4. Average ticket size and volume by age group and category (segments page)
SELECT ag.age_group, mc.category_name,
       COUNT(*) AS txn_count,
       AVG(f.amount) AS avg_ticket
FROM fact_transactions f
JOIN dim_age_group ag ON f.sender_age_group_id = ag.age_group_id
JOIN dim_merchant_category mc ON f.category_id = mc.category_id
GROUP BY ag.age_group, mc.category_name
ORDER BY ag.age_group, txn_count DESC;

-- 5. Fraud rate by amount band (risk page)
SELECT
  CASE
    WHEN f.amount < 500 THEN '1. Under 500'
    WHEN f.amount < 2000 THEN '2. 500-2000'
    WHEN f.amount < 5000 THEN '3. 2000-5000'
    ELSE '4. 5000+'
  END AS amount_band,
  COUNT(*) AS txn_count,
  SUM(CAST(f.fraud_flag AS INT)) AS fraud_count,
  CAST(SUM(CAST(f.fraud_flag AS INT)) AS FLOAT) / COUNT(*) AS fraud_rate
FROM fact_transactions f
GROUP BY
  CASE
    WHEN f.amount < 500 THEN '1. Under 500'
    WHEN f.amount < 2000 THEN '2. 500-2000'
    WHEN f.amount < 5000 THEN '3. 2000-5000'
    ELSE '4. 5000+'
  END
ORDER BY amount_band;
