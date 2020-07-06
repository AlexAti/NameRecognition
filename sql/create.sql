CREATE SCHEMA WLF;

CREATE TABLE WLF.party (
    key_party VARCHAR(64) PRIMARY KEY,
    value_party VARCHAR(128),
    birth_date DATE,
    birth_country VARCHAR(16),
    identifier VARCHAR(64)
);

CREATE TABLE WLF.screening (
    key_screen VARCHAR(64) PRIMARY KEY,
    value_screen VARCHAR(128),
    birth_date DATE,
    birth_country VARCHAR(16),
    identifier VARCHAR(64)
);

CREATE TABLE WLF.score_factor (
    factor_key VARCHAR(64) PRIMARY KEY,
    value_factor FLOAT,
    birth_date_factor FLOAT,
    birth_country_factor FLOAT,
    identifier_factor FLOAT
);

CREATE TABLE WLF.threshold (
    threshold_key VARCHAR(64),
    value_threshold FLOAT,
    global_threshold FLOAT
);

CREATE TABLE WLF.hit (
    hit_id VARCHAR(64) PRIMARY KEY,
    alert_id VARCHAR(64),
    key_party VARCHAR(64),
    key_screen VARCHAR(64),
    score FLOAT,
    birth_contry_hit BOOLEAN,
    birth_date_hit BOOLEAN,
    identifier_hit BOOLEAN
);

CREATE TABLE WLF.alert (
    key_alert VARCHAR(64),
    key_party VARCHAR(64)
);