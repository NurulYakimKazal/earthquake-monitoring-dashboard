import streamlit as st

from src.etl.fetch_usgs import run_etl
from src.db.database import create_tables
from modules.data_processing import get_clean_earthquake_data
from modules.earthquake_filtering import filter_earthquakes
from modules.init_db_and_sync import init_db_and_sync
from modules.compute_global_stats import compute_global_stats
from modules.init_ui_state import init_ui_state
from components.sidebar import sidebar

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Earthquake Dashboard", layout="wide")

# -----------------------------
# INIT DB
# -----------------------------
init_db_and_sync(create_tables, run_etl)

# -----------------------------
# LOAD DATA
# -----------------------------
df = get_clean_earthquake_data()

st.session_state.unfiltered_df = df

if df is None:
    st.warning("No earthquake data available.")
    st.stop()

stats = compute_global_stats(df)

latest_data = stats["latest_data"]
earliest = stats["earliest"]
latest_time = stats["latest_time"]

init_ui_state(stats)

# ----------------------------------------
# GENERATE SIDEBAR FILTERS (GLOBAL)
# ----------------------------------------
sidebar_result = sidebar(stats)

max_depth = sidebar_result['max_depth']
mag_min = sidebar_result['mag_min']
mag_max = sidebar_result['mag_max']

start_time = sidebar_result['start_time']
end_time = sidebar_result['end_time']


# ----------------------------------------
# FILTERS DATAFRAME
# ----------------------------------------
dff = filter_earthquakes(
    df,
    mag_min,
    mag_max,
    max_depth,
    start_time,
    end_time
)

st.session_state.filtered_df = dff


pg = st.navigation(
    [
        st.Page(
            "pages/overview.py",
            title="Overview",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page(
            "pages/analytics.py",
            title="Analytics",
            icon=":material/query_stats:",
        ),
        st.Page(
            "pages/ml_clustering.py",
            title="ML Clustering",
            icon=":material/hub:",
        ),
        st.Page(
            "pages/catalog.py",
            title="Live Feed & Catalog",
            icon=":material/public:",
        )
    ]
)

pg.run()