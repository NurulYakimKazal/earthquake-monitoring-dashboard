import requests
from datetime import datetime, timezone
import pandas as pd
import logging

from src.db.database import (
    create_tables,
    get_connection,
    get_latest_time,
    insert_earthquake,
)

from src.archived.archive import archive_old_data


USGS_QUERY_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


# -----------------------------
# Build safe start time
# -----------------------------
def build_starttime(latest_time_ms: int) -> str:
    """
    Convert epoch ms → ISO-8601 UTC.
    Adds overlap window to avoid missing events.
    """

    if latest_time_ms == 0:
        return "2025-01-01T00:00:00Z"

    overlap_ms = 5 * 60 * 1000
    safe_time = max(0, latest_time_ms - overlap_ms)

    dt = datetime.fromtimestamp(
        safe_time / 1000,
        tz=timezone.utc
    )

    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# -----------------------------
# Fetch from USGS
# -----------------------------
def fetch_usgs_data(latest_time_ms: int):
    params = {
        "format": "geojson",
        "starttime": build_starttime(latest_time_ms),
        "orderby": "time-asc",
    }

    try:
        response = requests.get(
            USGS_QUERY_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise TimeoutError("USGS API timeout")

    return response.json()["features"]


# -----------------------------
# ETL PIPELINE
# -----------------------------
def run_etl():
    create_tables()

    latest_time = get_latest_time()

    features = fetch_usgs_data(latest_time)

    with get_connection() as conn:

        inserted = 0

        for feature in features:
            try:
                props = feature["properties"]
                coords = feature["geometry"]["coordinates"]

                mag = props["mag"]

                # -----------------------------
                # clean invalid records
                # -----------------------------
                if mag is None:
                    continue

                now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

                if props["time"] > now_ms:
                    continue

                eq = {
                    "id": feature["id"],
                    "magnitude": float(mag),
                    "place": props["place"],
                    "time": props["time"],
                    "longitude": float(coords[0]),
                    "latitude": float(coords[1]),
                    "depth": float(coords[2]),
                }

                # insert_earthquake must use INSERT OR IGNORE internally
                if insert_earthquake(conn, eq):
                    inserted += 1

            except (KeyError, TypeError, ValueError):
                continue

        conn.commit()

    logger = logging.getLogger(__name__)

    logger.info(
        f"Inserted {inserted} new earthquakes (watermark={latest_time})"
    )

    # -----------------------------
    # ARCHIVE LAYER (HOT → COLD)
    # -----------------------------
    retention_days = 180  # keep 6 months in SQLite

    cutoff_time = int(
        (pd.Timestamp.utcnow() - pd.Timedelta(days=retention_days))
        .timestamp() * 1000
    )

    archived = archive_old_data(cutoff_time)

    logger.info(f"Archived {archived} old records")


# -----------------------------
# CLI ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_etl()