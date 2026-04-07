# pages/home.py
import streamlit as st

def show_home():
    st.title("Cricbuzz LiveStats")
    st.subheader("Real-Time Cricket Insights and SQL-Based Analytics")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pages", "5")
    with col2:
        st.metric("SQL Queries", "25")
    with col3:
        st.metric("Database", "MySQL")
    with col4:
        st.metric("API", "Cricbuzz")

    st.markdown("---")

    st.subheader("About This Project")
    st.write("""
    Cricbuzz LiveStats is a comprehensive cricket analytics dashboard that integrates 
    live data from the Cricbuzz API with a MySQL database to deliver real-time insights,
    player statistics, and SQL-driven analysis.
    """)

    st.subheader("How to Navigate")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Live Matches - View ongoing matches with live scores")
        st.info("Player Stats - Top batting and bowling rankings")
    with col2:
        st.success("SQL Analytics - Run 25 SQL queries on cricket data")
        st.success("CRUD Operations - Add, edit, delete player records")

    st.markdown("---")
    st.subheader("Tech Stack")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Python**\nCore language")
    with col2:
        st.markdown("**Streamlit**\nWeb dashboard")
    with col3:
        st.markdown("**MySQL**\nDatabase")
    with col4:
        st.markdown("**Cricbuzz API**\nLive data")
    with col5:
        st.markdown("**Pandas**\nData processing")