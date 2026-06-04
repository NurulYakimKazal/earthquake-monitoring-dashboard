import pandas as pd

def filter_earthquakes(df, mag_min, mag_max, max_depth, start_time, end_time):

    dff = df.copy()

    # Convert datetime once
    dff["datetime"] = pd.to_datetime(dff["datetime"], utc=True)
    start_time = pd.to_datetime(start_time, utc=True)
    end_time = pd.to_datetime(end_time, utc=True)

    # Numeric filters first
    dff = dff[
        (dff["magnitude"] >= mag_min) &
        (dff["magnitude"] <= mag_max) &
        (dff["depth"] <= max_depth)
    ]

    # Time filter
    dff = dff[
        (dff["datetime"] >= start_time) &
        (dff["datetime"] <= end_time)
    ]

    # Sort last
    dff = dff.sort_values("datetime", ascending=False)

    return dff