-- PayFlow step 3: create the star schema in SQL Server.
-- Run this against a new database, e.g.:  CREATE DATABASE PayFlow;
-- Then run this whole script against PayFlow.

CREATE TABLE dim_date (
    date_key      INT PRIMARY KEY,
    [date]        DATE NOT NULL,
    [year]        INT NOT NULL,
    [month]       INT NOT NULL,
    month_name    VARCHAR(10) NOT NULL,
    quarter       INT NOT NULL,
    day_of_week   VARCHAR(10) NOT NULL,
    is_weekend    BIT NOT NULL
);

CREATE TABLE dim_bank (
    bank_id     INT PRIMARY KEY,
    bank_name   VARCHAR(50) NOT NULL
);

CREATE TABLE dim_age_group (
    age_group_id INT PRIMARY KEY,
    age_group    VARCHAR(10) NOT NULL
);

CREATE TABLE dim_state (
    state_id    INT PRIMARY KEY,
    state_name  VARCHAR(50) NOT NULL
);

CREATE TABLE dim_merchant_category (
    category_id     INT PRIMARY KEY,
    category_name   VARCHAR(50) NOT NULL
);

CREATE TABLE dim_transaction_type (
    txn_type_id     INT PRIMARY KEY,
    txn_type_name   VARCHAR(30) NOT NULL
);

CREATE TABLE dim_device (
    device_id     INT PRIMARY KEY,
    device_type   VARCHAR(20) NOT NULL
);

CREATE TABLE dim_network (
    network_id    INT PRIMARY KEY,
    network_type  VARCHAR(10) NOT NULL
);

CREATE TABLE fact_transactions (
    transaction_id        VARCHAR(30) PRIMARY KEY,
    date_key              INT NOT NULL REFERENCES dim_date(date_key),
    hour_of_day            TINYINT NOT NULL,
    sender_bank_id         INT NOT NULL REFERENCES dim_bank(bank_id),
    receiver_bank_id       INT NOT NULL REFERENCES dim_bank(bank_id),
    sender_age_group_id    INT NOT NULL REFERENCES dim_age_group(age_group_id),
    receiver_age_group_id  INT NOT NULL REFERENCES dim_age_group(age_group_id),
    sender_state_id        INT NOT NULL REFERENCES dim_state(state_id),
    category_id            INT NOT NULL REFERENCES dim_merchant_category(category_id),
    txn_type_id            INT NOT NULL REFERENCES dim_transaction_type(txn_type_id),
    device_id              INT NOT NULL REFERENCES dim_device(device_id),
    network_id             INT NOT NULL REFERENCES dim_network(network_id),
    amount                 DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    transaction_status     VARCHAR(10) NOT NULL,
    is_success             BIT NOT NULL,
    fraud_flag             BIT NOT NULL
);

-- Helpful indexes for the queries and Power BI joins in the next steps
CREATE INDEX ix_fact_date ON fact_transactions(date_key);
CREATE INDEX ix_fact_banks ON fact_transactions(sender_bank_id, receiver_bank_id);
CREATE INDEX ix_fact_category ON fact_transactions(category_id);
