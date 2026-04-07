# pages/live_matches.py
import streamlit as st
import pandas as pd
from utils.api_fetcher import fetch_live_matches, fetch_upcoming_matches, fetch_recent_matches, fetch_scorecard

def show_scorecard(match_id, match_desc):
    st.markdown(f"### Scorecard: {match_desc}")
    with st.spinner("Loading scorecard..."):
        data = fetch_scorecard(match_id)
        if not data:
            st.error("Could not load scorecard.")
            return

        scorecards = data.get("scoreCard", [])
        if not scorecards:
            st.info("Scorecard not available yet.")
            return

        for innings in scorecards:
            innings_id = innings.get("inningsId")
            bat_team = innings.get("batTeamDetails", {})
            bowl_team = innings.get("bowlTeamDetails", {})
            
            st.markdown(f"#### Innings {innings_id} - {bat_team.get('batTeamName', '')}")

            # Score summary
            score_details = innings.get("scoreDetails", {})
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Runs", score_details.get("runs", 0))
            with col2:
                st.metric("Wickets", score_details.get("wickets", 0))
            with col3:
                st.metric("Overs", score_details.get("overs", 0))
            with col4:
                st.metric("Run Rate", score_details.get("runRate", 0))

            # Batting scorecard
            st.markdown("**Batting**")
            batsmen = bat_team.get("batsmenData", {})
            batting_rows = []
            for key, batsman in batsmen.items():
                batting_rows.append({
                    "Batsman": batsman.get("batName", ""),
                    "Runs": batsman.get("runs", 0),
                    "Balls": batsman.get("balls", 0),
                    "4s": batsman.get("fours", 0),
                    "6s": batsman.get("sixes", 0),
                    "SR": batsman.get("strikeRate", 0),
                    "Dismissal": batsman.get("outDesc", "batting")
                })
            if batting_rows:
                st.dataframe(pd.DataFrame(batting_rows), use_container_width=True)

            # Bowling scorecard
            st.markdown("**Bowling**")
            bowlers = bowl_team.get("bowlersData", {})
            bowling_rows = []
            for key, bowler in bowlers.items():
                bowling_rows.append({
                    "Bowler": bowler.get("bowlName", ""),
                    "Overs": bowler.get("overs", 0),
                    "Maidens": bowler.get("maidens", 0),
                    "Runs": bowler.get("runs", 0),
                    "Wickets": bowler.get("wickets", 0),
                    "Economy": bowler.get("economy", 0),
                    "NB": bowler.get("no_balls", 0),
                    "WD": bowler.get("wides", 0)
                })
            if bowling_rows:
                st.dataframe(pd.DataFrame(bowling_rows), use_container_width=True)

            st.markdown("---")

def show_live_matches():
    st.title("Live Matches")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Live", "Upcoming", "Recent"])

    with tab1:
        st.subheader("Live Matches")
        if st.button("Refresh"):
            st.rerun()

        matches = fetch_live_matches()
        if matches:
            for i, match in enumerate(matches):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{match.get('description', 'N/A')}**")
                        st.write(f"Teams: {match.get('team1')} vs {match.get('team2')}")
                        st.write(f"Format: {match.get('match_format')}  |  Venue: {match.get('venue')}, {match.get('city')}")
                        st.write(f"Status: {match.get('status')}")
                    with col2:
                        if st.button("View Scorecard", key=f"sc_{i}"):
                            st.session_state[f"show_sc_{i}"] = not st.session_state.get(f"show_sc_{i}", False)

                    if st.session_state.get(f"show_sc_{i}", False):
                        show_scorecard(match.get("match_id"), match.get("description"))

                    st.markdown("---")
        else:
            st.info("No live matches at the moment.")

    with tab2:
        st.subheader("Upcoming Matches")
        matches = fetch_upcoming_matches()
        if matches:
            df = pd.DataFrame(matches)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No upcoming matches found.")

    with tab3:
        st.subheader("Recent Matches")
        matches = fetch_recent_matches()
        if matches:
            df = pd.DataFrame(matches)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent matches found.")