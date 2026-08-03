DEFAULT_VALUES = {
    "latest_data": {
        "magnitude": "N/A",
        "place": "N/A",
        "depth": "N/A",
        "datetime": "N/A",
    },
    "earliest": "N/A",
    "latest_time": "N/A",
}


def prepare_global_stats(df):

    if df.empty:
        return DEFAULT_VALUES

    latest_data = df.iloc[0]

    return {
        "latest_data": {
            "magnitude": f"{latest_data['magnitude']:.2f}",
            "place": latest_data["place"],
            "depth": f"{latest_data['depth']:.2f} Km",
            "datetime": latest_data["datetime"].strftime("%Y-%m-%d %H:%M:%S"),
        },
        "earliest": df["datetime"].min().strftime("%Y-%m-%d %H:%M:%S"),
        "latest_time": df["datetime"].max().strftime("%Y-%m-%d %H:%M:%S")
    }