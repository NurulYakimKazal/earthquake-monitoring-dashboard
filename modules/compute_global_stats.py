def compute_global_stats(df):
    return {
        "latest_data": df.iloc[0],
        "earliest": df["datetime"].min(),
        "latest_time": df["datetime"].max()
    }