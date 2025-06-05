import os
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiolunarcrush import LunarCrush
from glassnode_rest import GlassnodeClient
import feedparser
from textblob import TextBlob

from .db import get_conn, init_db

WATCHLIST = ["BTCUSDT", "ETHUSDT"]
LUNARCRUSH_API_KEY = os.getenv("LUNARCRUSH_API_KEY", "")
GLASSNODE_API_KEY = os.getenv("GLASSNODE_API_KEY", "")
CRYPTO_PANIC_RSS = os.getenv(
    "CRYPTO_PANIC_RSS",
    "https://cryptopanic.com/api/v1/posts/?kind=news&public=true"
)

async def fetch_galaxy_score(symbol: str) -> float:
    lc = LunarCrush(api_key=LUNARCRUSH_API_KEY)
    data = await lc.get_coins(symbol=symbol)
    if data and "galaxy_score" in data[0]:
        return float(data[0]["galaxy_score"])
    return 0.0

async def fetch_active_addr_pct(symbol: str) -> float:
    g = GlassnodeClient(GLASSNODE_API_KEY)
    try:
        data = g.get("addresses/active_count_change", a=symbol)
        return float(data[-1]["v"]) if data else 0.0
    except Exception:
        return 0.0

async def fetch_news_sentiment() -> float:
    feed = feedparser.parse(CRYPTO_PANIC_RSS)
    total = 0.0
    count = 0
    for entry in feed.entries:
        blob = TextBlob(entry.title)
        total += blob.sentiment.polarity
        count += 1
    return total / count if count else 0.0

async def update_fundamentals():
    ts = int(datetime.utcnow().timestamp() * 1000)
    conn = get_conn()
    news_sent = await fetch_news_sentiment()
    for symbol in WATCHLIST:
        galaxy = await fetch_galaxy_score(symbol)
        active = await fetch_active_addr_pct(symbol)
        with conn:
            conn.execute(
                "REPLACE INTO fundamentals (symbol, ts, galaxy_score, active_addr_pct, news_sent) VALUES (?, ?, ?, ?, ?)",
                (symbol, ts, galaxy, active, news_sent),
            )
    conn.close()
    print(f"Updated fundamentals @ {datetime.utcnow()} for {WATCHLIST}")

async def main():
    init_db()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_fundamentals, "interval", hours=1, next_run_time=datetime.utcnow())
    scheduler.start()
    print("Fundamental processor running. Press Ctrl+C to exit.")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
