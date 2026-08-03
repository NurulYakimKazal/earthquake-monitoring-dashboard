def prepare_live_feed_data(df):
    feed = df.head(15)[["time_fmt", "magnitude", "place", "depth"]]
    return feed


def prepare_catalog_data(df):
    display_df = df[
        ["datetime", "magnitude", "place", "depth", "latitude", "longitude"]
    ].copy()

    display_df["magnitude"] = display_df["magnitude"].map(lambda x: f"{x:.2f}")
    display_df["depth"] = display_df["depth"].map(lambda x: f"{x:.2f}")

    display_df.rename(
        columns={
            "datetime": "Date Time (UTC)",
            "magnitude": "Magnitude",
            "place": "Location",
            "depth": "Depth (km)",
            "latitude": "Latitude",
            "longitude": "Longitude",
        },
        inplace=True,
    )

    return display_df