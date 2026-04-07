# main.py
import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

from pages.home import show_home
from pages.live_matches import show_live_matches
from pages.player_stats import show_player_stats
from pages.sql_analytics import show_sql_analytics
from pages.crud_operations import show_crud_operations

st.sidebar.title("Cricbuzz LiveStats")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["Home", "Live Matches", "Player Stats", "SQL Analytics", "CRUD Operations"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built with: Python, SQL, Streamlit, Cricbuzz API")

if page == "Home":
    show_home()
elif page == "Live Matches":
    show_live_matches()
elif page == "Player Stats":
    show_player_stats()
elif page == "SQL Analytics":
    show_sql_analytics()
elif page == "CRUD Operations":
    show_crud_operations()