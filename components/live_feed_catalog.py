import streamlit as st
from components.spacer import spacer


def render_live_feed(feed):
    st.subheader("⚡ Live Activity Feed")

    spacer(1)

    st.caption(
        "The live activity feed only shows the latest 20 earthquake events.",
    )

    for _, row in feed.iterrows():
        if row["magnitude"] >= 6:
            st.error(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")
        elif row["magnitude"] >= 5:
            st.warning(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")
        else:
            st.write(f"{row['time_fmt']} | M{row['magnitude']:.1f} | {row['place']}")


def render_catalog(df):
    st.subheader("📍 Earthquake Catalog")

    spacer(1)

    st.caption(
        "Catalog only shows the raw data of the last 500 earthquake events.",
    )

    st.dataframe(df, width="stretch", height="stretch", hide_index=True)