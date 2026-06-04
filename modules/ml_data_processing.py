import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import DBSCAN
import hdbscan


# =========================
# COMMON UTILITY
# =========================
def _prepare_coords(df: pd.DataFrame):
    """
    Convert lat/lon to radians for haversine clustering.
    """
    return np.radians(df[["latitude", "longitude"]].values)


# =========================
# DBSCAN CLUSTERING (CACHED)
# =========================
@st.cache_data(show_spinner=True)
def run_dbscan(
    df: pd.DataFrame,
    eps_km: float = 30,
    min_samples: int = 5
) -> pd.DataFrame:
    """
    DBSCAN clustering using haversine distance.
    """

    if df.empty:
        df = df.copy()
        df["cluster"] = pd.Series(dtype="int")
        return df

    df = df.copy()
    coords = _prepare_coords(df)

    earth_radius = 6371.0088
    eps = eps_km / earth_radius

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree"
    )

    df["cluster"] = model.fit_predict(coords)
    return df


# =========================
# HDBSCAN CLUSTERING (CACHED)
# =========================
@st.cache_data(show_spinner=True)
def run_hdbscan(
    df: pd.DataFrame,
    min_cluster_size: int = 8,
    min_samples: int = 5
) -> pd.DataFrame:
    """
    HDBSCAN clustering using haversine distance.
    """

    if df.empty:
        df = df.copy()
        df["cluster"] = pd.Series(dtype="int")
        return df

    df = df.copy()
    coords = _prepare_coords(df)

    model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="haversine"
    )

    df["cluster"] = model.fit_predict(coords)
    return df


# =========================
# CLUSTER SUMMARY (UI)
# =========================
def get_cluster_summary(df: pd.DataFrame):
    """
    Returns quick stats for UI dashboard.
    """

    if df.empty or "cluster" not in df.columns:
        return {
            "num_clusters": 0,
            "noise_ratio": 0.0,
            "largest_cluster": 0
        }

    clusters = df["cluster"]

    # exclude noise
    valid = clusters[clusters != -1]

    num_clusters = valid.nunique()
    noise_ratio = float((clusters == -1).mean())
    largest_cluster = valid.value_counts().iloc[0] if not valid.empty else 0

    return {
        "num_clusters": int(num_clusters),
        "noise_ratio": noise_ratio,
        "largest_cluster": int(largest_cluster)
    }