import requests
import logging
from datetime import datetime, timedelta, timezone
from src.db.database import get_connection
from src.db.database import create_tables
from src.db.database import insert_earthquake


USGS_QUERY_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def run_backfill():

    create_tables()

    start_time = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    params = {
        "format": "geojson",
        "starttime": start_time,
        "orderby": "time-asc",
        "limit": 20000
    }

    response = requests.get(USGS_QUERY_URL, params=params, timeout=20)
    response.raise_for_status()

    features = response.json()["features"]

    conn = get_connection()
    inserted = 0

    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        if props["mag"] is None:
            continue

        eq = {
            "id": feature["id"],
            "magnitude": float(props["mag"]),
            "place": props["place"],
            "time": props["time"],
            "longitude": float(coords[0]),
            "latitude": float(coords[1]),
            "depth": float(coords[2]),
        }

        if insert_earthquake(conn, eq):
            inserted += 1

    conn.commit()
    conn.close()

    logger = logging.getLogger(__name__)

    logger.info(
        f"Backfill inserted {inserted} records"
    )