import logging
from src.etl.fetch_historical_usgs import run_backfill


if __name__ == "__main__":
    try:
        run_backfill()
    except Exception as e:
        logging.exception(f"Backfill failed: {e}")
        raise