# Crypto Trade Dashboard Skeleton

This repository provides a minimal backend skeleton to collect basic market fundamentals and merge them with candle data.

## Features

- **Fundamental Processor** (`backend/fundamental_processor.py`)
  - Fetches GalaxyScore from LunarCrush, active address change from Glassnode, and news sentiment from CryptoPanic RSS.
  - Runs hourly using APScheduler.
  - Stores data in a SQLite database (`trade.db`).
- **Indicator Utilities** (`backend/indicators.py`)
  - `get_feature_frame(symbol)` loads candle data and merges the latest fundamentals.
- **Database Setup**
  - Schema for the `fundamentals` table is provided in `migrations/create_fundamentals.sql`.

## Quick Start

1. Install dependencies:
   ```bash
   pip install aiolunarcrush glassnode-rest textblob feedparser apscheduler pandas
   ```
2. Initialize the database:
   ```bash
   python backend/db.py
   ```
3. Run the fundamental processor:
   ```bash
   python backend/fundamental_processor.py
   ```

Set environment variables `LUNARCRUSH_API_KEY` and `GLASSNODE_API_KEY` for API access.
