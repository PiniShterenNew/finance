import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "trade.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS fundamentals (
    symbol TEXT,
    ts INTEGER,
    galaxy_score REAL,
    active_addr_pct REAL,
    news_sent REAL,
    PRIMARY KEY(symbol, ts)
);
"""

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized", DB_PATH)
