# pages/crud_operations.py
import streamlit as st
import pandas as pd
from utils.db_connection import get_connection, close_connection

def show_crud_operations():
    st.title("CRUD Operations")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["View Players", "Add Player", "Update Player", "Delete Player"])

    with tab1:
        st.subheader("All Players")
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM players")
            players = cursor.fetchall()
            close_connection(conn, cursor)
            if players:
                df = pd.DataFrame(players)
                st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Add New Player")
        full_name = st.text_input("Full Name")
        country = st.text_input("Country")
        dob = st.date_input("Date of Birth")
        playing_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        batting_style = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
        bowling_style = st.text_input("Bowling Style")
        team_id = st.number_input("Team ID", min_value=1, step=1)

        if st.button("Add Player"):
            if full_name and country:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO players (full_name, country, date_of_birth, playing_role, batting_style, bowling_style, team_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (full_name, country, dob, playing_role, batting_style, bowling_style, team_id))
                    conn.commit()
                    close_connection(conn, cursor)
                    st.success(f"Player {full_name} added successfully!")
            else:
                st.error("Please fill in at least Full Name and Country.")

    with tab3:
        st.subheader("Update Player")
        player_id = st.number_input("Enter Player ID to Update", min_value=1, step=1)
        new_name = st.text_input("New Full Name")
        new_country = st.text_input("New Country")

        if st.button("Update Player"):
            if player_id and new_name:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE players SET full_name=%s, country=%s WHERE player_id=%s
                    """, (new_name, new_country, player_id))
                    conn.commit()
                    close_connection(conn, cursor)
                    st.success("Player updated successfully!")

    with tab4:
        st.subheader("Delete Player")
        st.warning("This action cannot be undone.")
        del_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)

        if st.button("Delete Player"):
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM players WHERE player_id=%s", (del_id,))
                conn.commit()
                close_connection(conn, cursor)
                st.success("Player deleted successfully!")