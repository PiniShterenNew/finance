import pandas as pd
from .db import get_conn

def get_feature_frame(symbol: str) -> pd.DataFrame:
    conn = get_conn()
    candles = pd.read_sql(
        "SELECT ts, open, high, low, close, volume FROM candles WHERE symbol = ? ORDER BY ts",
        conn,
        params=(symbol,),
    )
    fundamentals = pd.read_sql(
        "SELECT ts, galaxy_score, active_addr_pct, news_sent FROM fundamentals WHERE symbol = ? ORDER BY ts",
        conn,
        params=(symbol,),
    )
    conn.close()

    fundamentals = fundamentals.set_index("ts")
    candles = candles.set_index("ts")
    df = candles.join(fundamentals, how="left").fillna(method="ffill")
    return df.reset_index()
