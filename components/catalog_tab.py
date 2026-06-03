import streamlit as st


def render_live_feed(df):
    st.subheader("⚡ Live Activity Feed")
    st.write("")

    feed = df.head(10)[["time_fmt", "magnitude", "place", "depth"]]

    for _, row in feed.iterrows():
        if row["magnitude"] >= 6:
            st.error(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")
        elif row["magnitude"] >= 5:
            st.warning(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")
        else:
            st.write(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")


def render_catalog(df):
    st.subheader("📍 Earthquake Catalog")
    st.write("")

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

    st.dataframe(display_df, width='stretch', hide_index=True)