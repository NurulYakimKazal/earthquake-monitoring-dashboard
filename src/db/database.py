import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "earthquake.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# -----------------------------
# SCHEMA INIT
# -----------------------------
def create_tables():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            magnitude REAL,
            place TEXT,
            time INTEGER,
            longitude REAL,
            latitude REAL,
            depth REAL
        )
        """)
        conn.commit()


# -----------------------------
# INSERT (IDEMPOTENT)
# -----------------------------
def insert_earthquake(conn, eq: dict) -> bool:
    """
    Inserts one earthquake.
    Returns True if inserted, False if ignored (duplicate).
    """

    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO earthquakes (
            id, magnitude, place, time,
            longitude, latitude, depth
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        eq["id"],
        eq["magnitude"],
        eq["place"],
        eq["time"],
        eq["longitude"],
        eq["latitude"],
        eq["depth"],
    ))

    # rowcount = 1 means inserted, 0 means ignored (duplicate)
    return cur.rowcount > 0


# -----------------------------
# GET LAST TIMESTAMP (WATERMARK)
# -----------------------------
def get_latest_time() -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(time) FROM earthquakes")
        result = cur.fetchone()[0]

        return result if result is not None else 0


def fetch_all():
    with get_connection() as conn:
        return pd.read_sql(
            "SELECT * FROM earthquakes ORDER BY time DESC",
            conn
        )