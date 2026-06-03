import streamlit as st

from src.etl.fetch_usgs import run_etl
from src.db.database import create_tables
from modules.data_processing import get_clean_earthquake_data
from modules.earthquake_filtering import filter_earthquakes
from modules.init_db_and_sync import init_db_and_sync
from modules.add_features import add_features
from modules.compute_global_stats import compute_global_stats
from modules.init_ui_state import init_ui_state
from components.sidebar import sidebar
from components.kpis import render_summary
from components.map_tab import render_earthquake_map
from components.analytics_tab import render_trends
from components.catalog_tab import render_live_feed, render_catalog


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Earthquake Dashboard", layout="wide")

st.title("🌍 Earthquake Monitoring Dashboard")

st.write("")
st.write("")
st.write("")

st.markdown(
    """
    **Data Source:** [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/)  
    Real-time global earthquake events provided by the United States Geological Survey (USGS).
    """
)

st.write("")
st.write("")
st.write("")


# -----------------------------
# INIT DB
# -----------------------------
init_db_and_sync(create_tables, run_etl)

# -----------------------------
# LOAD DATA
# -----------------------------
df = get_clean_earthquake_data()

if df is None:
    st.warning("No earthquake data available.")
    st.stop()

df = add_features(df)

stats = compute_global_stats(df)

latest_data = stats["latest_data"]
earliest = stats["earliest"]
latest_time = stats["latest_time"]

init_ui_state()


# ----------------------------------------
# GENERATE SIDEBAR FILTERS (GLOBAL)
# ----------------------------------------
sidebar_result = sidebar()

view_mode = sidebar_result['view_mode']
max_depth = sidebar_result['max_depth']
mag_min = sidebar_result['mag_min']
mag_max = sidebar_result['mag_max']


# ----------------------------------------
# FILTERS DATAFRAME
# ----------------------------------------
result = filter_earthquakes(df, mag_min, mag_max, max_depth)

dff = result["filtered"]
latest = result["latest"]
is_empty = result["empty"]

if is_empty:
    st.warning("No earthquakes match the selected filters.")
    st.stop()


# -----------------------------
# HEADER SUMMARY
# -----------------------------
render_summary(latest_data, earliest, latest_time, dff)

st.write("")

# -----------------------------
# TABS
# -----------------------------
tab_map, tab_analytics, tab_catalog = st.tabs(
    ["🌍 Map", "📈 Analytics", "📍 Catalog"]
)


# -----------------------------
# MAP
# -----------------------------
with tab_map:
    st.write("")
    render_earthquake_map(dff, view_mode, latest)

# -----------------------------
# ANALYTICS
# -----------------------------
with tab_analytics:
    st.write("")
    render_trends(dff)

# -----------------------------
# CATALOG
# -----------------------------
with tab_catalog:
    st.write("")

    column1, column2 = st.columns([2, 3], border=True)
    with column1:
        render_live_feed(df)


    with column2:
        render_catalog(df)


st.divider()

st.caption(
    "Earthquake Monitoring Dashboard • Data provided by USGS Earthquake Catalog API"
)