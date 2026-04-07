# pages/player_stats.py
import streamlit as st
import pandas as pd
from utils.api_fetcher import fetch_top_batting_stats, fetch_top_bowling_stats

def show_player_stats():
    st.title("Player Statistics")
    st.markdown("---")

    format_type = st.selectbox("Select Format", ["ODI", "Test", "T20I"])

    tab1, tab2 = st.tabs(["Batting Rankings", "Bowling Rankings"])

    with tab1:
        st.subheader(f"Top Batting Rankings - {format_type}")
        data = fetch_top_batting_stats(format_type)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No batting data available.")

    with tab2:
        st.subheader(f"Top Bowling Rankings - {format_type}")
        data = fetch_top_bowling_stats(format_type)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No bowling data available.")