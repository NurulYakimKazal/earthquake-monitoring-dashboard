import streamlit as st
import pandas as pd
from src.db.database import fetch_all


@st.cache_data(ttl=60)
def get_clean_earthquake_data():
    df = fetch_all()

    if df.empty:
        return df

    # numeric cleanup
    df["magnitude"] = pd.to_numeric(df["magnitude"], errors="coerce")
    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df = df.dropna(subset=["magnitude", "depth", "latitude", "longitude"])
    df["depth"] = df["depth"].abs()

    # time standardization
    df["datetime"] = pd.to_datetime(df["time"], unit="ms", utc=True)
    df["time_fmt"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # sort
    df = df.sort_values("datetime", ascending=False).reset_index(drop=True)

    # derived fields
    df["magnitude_fmt"] = df["magnitude"].round(2)
    df["depth_fmt"] = df["depth"].round(2)

    return df