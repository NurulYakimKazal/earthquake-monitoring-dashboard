import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import hdbscan


DEFAULT_KPIS_VALUES = {
    "Detected Clusters": 0,
    "Unclustered Points": "0.0%",
    "Max Cluster Size": 0
}


# =========================
# COMMON UTILITY
# =========================
def _prepare_coords(df: pd.DataFrame):
    """
    Convert lat/lon to radians for haversine clustering.
    """
    return np.radians(
        df[["latitude", "longitude"]].values
    )


# =========================
# DBSCAN CLUSTERING
# =========================
def run_dbscan(
    df: pd.DataFrame,
    eps_km: float = 30,
    min_samples: int = 5,
) -> pd.DataFrame:
    """
    DBSCAN clustering using haversine distance.
    """

    coords = _prepare_coords(df)

    earth_radius = 6371.0088
    eps = eps_km / earth_radius

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree",
    )

    df["cluster"] = model.fit_predict(coords)

    return df


# =========================
# HDBSCAN CLUSTERING
# =========================
def run_hdbscan(
    df: pd.DataFrame,
    min_cluster_size: int = 8,
    min_samples: int = 5,
) -> pd.DataFrame:
    """
    HDBSCAN clustering using haversine distance.
    """

    coords = _prepare_coords(df)

    model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="haversine",
    )

    df["cluster"] = model.fit_predict(coords)

    return df


# =========================
# CLUSTER SUMMARY
# =========================
def get_cluster_summary(df: pd.DataFrame):

    if df.empty or "cluster" not in df.columns:
        return DEFAULT_KPIS_VALUES

    clusters = df["cluster"]
    valid = clusters[clusters != -1]

    if valid.empty:
        return {
            "Detected Clusters": 0,
            "Unclustered Points": "100.0%",
            "Max Cluster Size": 0,
        }

    return {
        "Detected Clusters": int(valid.nunique()),
        "Unclustered Points": f"{float((clusters == -1).mean()):.1%}",
        "Max Cluster Size": int(valid.value_counts().max()),
    }


# =========================
# CLUSTERING PIPELINE
# =========================
def prepare_clustered_data(
    dff: pd.DataFrame,
    parameters: dict,
):
    """
    Prepare filtered data and run selected clustering algorithm.
    Returns a new dataframe with cluster labels.
    """

    # Protect session_state.filtered_df
    dff = (
        dff
        .dropna(subset=["latitude", "longitude"])
        .copy()
    )

    if dff.empty:
        dff["cluster"] = -1
        return dff

    n = len(dff)

    # Not enough points for clustering
    if n < 2:
        dff["cluster"] = -1
        return dff

    if parameters["algorithm"] == "DBSCAN":

        return run_dbscan(
            dff,
            eps_km=parameters["eps_km"],
            min_samples=min(
                parameters["min_samples"],
                n
            ),
        )

    return run_hdbscan(
        dff,
        min_cluster_size=min(
            parameters["min_cluster_size"],
            n
        ),
        min_samples=min(
            parameters["min_samples"],
            n
        ),
    )