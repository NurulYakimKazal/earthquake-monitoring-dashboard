import pandas as pd
from pathlib import Path
from src.db.database import get_connection

ARCHIVE_PATH = Path("archive/earthquakes.parquet")


def archive_old_data(cutoff_time: int):
    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM earthquakes WHERE time < ?",
        conn,
        params=(cutoff_time,)
    )

    if df.empty:
        conn.close()
        return 0

    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if ARCHIVE_PATH.exists():
        old = pd.read_parquet(ARCHIVE_PATH)
        df = pd.concat([old, df], ignore_index=True)

    df.to_parquet(ARCHIVE_PATH, index=False)

    conn.execute(
        "DELETE FROM earthquakes WHERE time < ?",
        (cutoff_time,)
    )

    conn.commit()
    conn.close()

    return len(df)