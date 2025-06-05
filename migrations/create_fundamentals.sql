CREATE TABLE IF NOT EXISTS fundamentals (
    symbol TEXT,
    ts INTEGER,
    galaxy_score REAL,
    active_addr_pct REAL,
    news_sent REAL,
    PRIMARY KEY(symbol, ts)
);
