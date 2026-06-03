import pandas as pd


def filter_earthquakes(df: pd.DataFrame, mag_min: float, mag_max: float, max_depth: float):
    dff = df[
        (df["magnitude"] >= mag_min) &
        (df["magnitude"] <= mag_max) &
        (df["depth"] <= max_depth)
    ].copy()

    dff = dff.sort_values("datetime", ascending=False)

    latest = dff.head(1)

    return {
        "filtered": dff,
        "latest": latest,
        "empty": dff.empty
    }