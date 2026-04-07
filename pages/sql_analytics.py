# pages/sql_analytics.py
import streamlit as st
import pandas as pd
from utils.db_connection import get_connection, close_connection

def run_query(query):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            close_connection(conn, cursor)
            return pd.DataFrame(results)
        except Exception as e:
            st.error(f"Query error: {e}")
            close_connection(conn)
            return pd.DataFrame()
    return pd.DataFrame()

def show_sql_analytics():
    st.title("SQL Analytics")
    st.markdown("---")

    queries = {
        "Q1 - Players from India": """
            SELECT full_name, playing_role, batting_style, bowling_style 
            FROM players WHERE country = 'India'
        """,
        "Q2 - Matches in last 30 days": """
            SELECT match_description, t1.team_name as team1, t2.team_name as team2,
            v.venue_name, v.city, match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE match_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY match_date DESC
        """,
        "Q3 - Top 10 ODI Run Scorers": """
            SELECT p.full_name, cs.total_runs, cs.batting_average, cs.centuries
            FROM career_stats cs
            JOIN players p ON cs.player_id = p.player_id
            WHERE cs.format = 'ODI'
            ORDER BY cs.total_runs DESC LIMIT 10
        """,
        "Q4 - Venues with capacity > 50000": """
            SELECT venue_name, city, country, capacity
            FROM venues WHERE capacity > 50000
            ORDER BY capacity DESC
        """,
        "Q5 - Team wins count": """
            SELECT t.team_name, COUNT(*) as total_wins
            FROM matches m JOIN teams t ON m.winner_id = t.team_id
            GROUP BY t.team_name ORDER BY total_wins DESC
        """,
        "Q6 - Players per role": """
            SELECT playing_role, COUNT(*) as player_count
            FROM players GROUP BY playing_role
        """,
        "Q7 - Highest score per format": """
            SELECT format, MAX(highest_score) as highest_score
            FROM career_stats GROUP BY format
        """,
        "Q8 - Series starting in 2024": """
            SELECT series_name, host_country, match_type, start_date, total_matches
            FROM series WHERE YEAR(start_date) = 2024
        """,
        "Q9 - All-rounders 1000+ runs and 50+ wickets": """
            SELECT p.full_name, cs.total_runs, cs.total_wickets, cs.format
            FROM career_stats cs JOIN players p ON cs.player_id = p.player_id
            JOIN players pl ON cs.player_id = pl.player_id
            WHERE pl.playing_role = 'All-rounder'
            AND cs.total_runs > 1000 AND cs.total_wickets > 50
        """,
        "Q10 - Last 20 completed matches": """
            SELECT m.match_description, t1.team_name as team1, t2.team_name as team2,
            tw.team_name as winner, m.victory_margin, m.victory_type, v.venue_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams tw ON m.winner_id = tw.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.status = 'completed'
            ORDER BY m.match_date DESC LIMIT 20
        """,
        "Q11 - Player performance across formats": """
            SELECT p.full_name,
            SUM(CASE WHEN cs.format='Test' THEN cs.total_runs ELSE 0 END) as test_runs,
            SUM(CASE WHEN cs.format='ODI' THEN cs.total_runs ELSE 0 END) as odi_runs,
            SUM(CASE WHEN cs.format='T20I' THEN cs.total_runs ELSE 0 END) as t20_runs,
            AVG(cs.batting_average) as overall_avg
            FROM career_stats cs JOIN players p ON cs.player_id = p.player_id
            GROUP BY p.full_name HAVING COUNT(DISTINCT cs.format) >= 2
        """,
        "Q12 - Home vs Away wins": """
            SELECT t.team_name,
            SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) as home_wins,
            SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) as away_wins
            FROM matches m
            JOIN teams t ON m.winner_id = t.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY t.team_name
        """,
        "Q13 - Partnerships 100+ runs": """
            SELECT p1.full_name as batsman1, p2.full_name as batsman2,
            ps1.runs_scored + ps2.runs_scored as partnership_runs, ps1.innings
            FROM player_stats ps1
            JOIN player_stats ps2 ON ps1.match_id = ps2.match_id
            AND ps1.innings = ps2.innings
            AND ps2.batting_position = ps1.batting_position + 1
            JOIN players p1 ON ps1.player_id = p1.player_id
            JOIN players p2 ON ps2.player_id = p2.player_id
            WHERE ps1.runs_scored + ps2.runs_scored >= 100
        """,
        "Q14 - Bowler economy at venues": """
            SELECT p.full_name, v.venue_name,
            AVG(ps.economy_rate) as avg_economy,
            SUM(ps.wickets_taken) as total_wickets,
            COUNT(ps.match_id) as matches_played
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE ps.overs_bowled >= 4
            GROUP BY p.full_name, v.venue_name
            HAVING matches_played >= 1
        """,
        "Q15 - Performance in close matches": """
            SELECT p.full_name,
            AVG(ps.runs_scored) as avg_runs,
            COUNT(ps.match_id) as close_matches
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE (m.victory_type = 'runs' AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED) < 50)
            OR (m.victory_type = 'wickets' AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED) < 5)
            GROUP BY p.full_name
        """,
        "Q16 - Batting performance by year": """
            SELECT p.full_name, YEAR(m.match_date) as year,
            AVG(ps.runs_scored) as avg_runs,
            AVG(ps.strike_rate) as avg_sr
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.match_date >= '2020-01-01'
            GROUP BY p.full_name, YEAR(m.match_date)
            HAVING COUNT(ps.match_id) >= 1
        """,
        "Q17 - Toss advantage analysis": """
            SELECT toss_decision,
            COUNT(*) as total_matches,
            SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) as toss_winner_won,
            ROUND(SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_percentage
            FROM matches WHERE status = 'completed' AND toss_decision IS NOT NULL
            GROUP BY toss_decision
        """,
        "Q18 - Most economical bowlers": """
            SELECT p.full_name, AVG(ps.economy_rate) as economy,
            SUM(ps.wickets_taken) as total_wickets,
            COUNT(ps.match_id) as matches
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.match_type IN ('ODI','T20I') AND ps.overs_bowled > 0
            GROUP BY p.full_name
            HAVING matches >= 1 AND AVG(ps.overs_bowled) >= 1
            ORDER BY economy ASC
        """,
        "Q19 - Most consistent batsmen": """
            SELECT p.full_name,
            AVG(ps.runs_scored) as avg_runs,
            STDDEV(ps.runs_scored) as consistency_score
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE ps.balls_faced >= 10 AND m.match_date >= '2022-01-01'
            GROUP BY p.full_name
            HAVING COUNT(ps.stat_id) >= 1
            ORDER BY consistency_score ASC
        """,
        "Q20 - Format-wise match count and average": """
            SELECT p.full_name,
            SUM(CASE WHEN m.match_type='Test' THEN 1 ELSE 0 END) as test_matches,
            SUM(CASE WHEN m.match_type='ODI' THEN 1 ELSE 0 END) as odi_matches,
            SUM(CASE WHEN m.match_type IN ('T20I','T20') THEN 1 ELSE 0 END) as t20_matches,
            AVG(ps.runs_scored) as overall_avg
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            GROUP BY p.full_name
            HAVING COUNT(ps.stat_id) >= 1
        """,
        "Q21 - Comprehensive player ranking": """
            SELECT p.full_name,
            ROUND((cs.total_runs * 0.01) + (COALESCE(cs.batting_average,0) * 0.5) + (COALESCE(cs.batting_sr,0) * 0.3), 2) as batting_points,
            ROUND((cs.total_wickets * 2), 2) as bowling_points,
            ROUND((cs.total_catches * 3), 2) as fielding_points,
            cs.format
            FROM career_stats cs JOIN players p ON cs.player_id = p.player_id
            ORDER BY batting_points DESC
        """,
        "Q22 - Head to head analysis": """
            SELECT t1.team_name as team1, t2.team_name as team2,
            COUNT(*) as total_matches,
            SUM(CASE WHEN m.winner_id = m.team1_id THEN 1 ELSE 0 END) as team1_wins,
            SUM(CASE WHEN m.winner_id = m.team2_id THEN 1 ELSE 0 END) as team2_wins
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            WHERE m.status = 'completed'
            GROUP BY t1.team_name, t2.team_name
            HAVING total_matches >= 1
        """,
        "Q23 - Player form analysis": """
            SELECT p.full_name,
            AVG(ps.runs_scored) as avg_runs,
            MAX(ps.runs_scored) as highest,
            SUM(CASE WHEN ps.runs_scored >= 50 THEN 1 ELSE 0 END) as fifties_plus,
            STDDEV(ps.runs_scored) as consistency,
            CASE
                WHEN AVG(ps.runs_scored) >= 60 THEN 'Excellent Form'
                WHEN AVG(ps.runs_scored) >= 40 THEN 'Good Form'
                WHEN AVG(ps.runs_scored) >= 20 THEN 'Average Form'
                ELSE 'Poor Form'
            END as form_status
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            GROUP BY p.full_name
        """,
        "Q24 - Best batting partnerships": """
            SELECT p1.full_name as batsman1, p2.full_name as batsman2,
            AVG(ps1.runs_scored + ps2.runs_scored) as avg_partnership,
            MAX(ps1.runs_scored + ps2.runs_scored) as highest_partnership,
            COUNT(*) as total_partnerships
            FROM player_stats ps1
            JOIN player_stats ps2 ON ps1.match_id = ps2.match_id
            AND ps1.innings = ps2.innings
            AND ps2.batting_position = ps1.batting_position + 1
            JOIN players p1 ON ps1.player_id = p1.player_id
            JOIN players p2 ON ps2.player_id = p2.player_id
            GROUP BY p1.full_name, p2.full_name
            HAVING total_partnerships >= 1
            ORDER BY avg_partnership DESC
        """,
        "Q25 - Player career trajectory": """
            SELECT p.full_name,
            YEAR(m.match_date) as year,
            AVG(ps.runs_scored) as avg_runs,
            AVG(ps.strike_rate) as avg_sr,
            CASE
                WHEN AVG(ps.runs_scored) > LAG(AVG(ps.runs_scored)) OVER (PARTITION BY p.full_name ORDER BY YEAR(m.match_date))
                THEN 'Improving'
                WHEN AVG(ps.runs_scored) < LAG(AVG(ps.runs_scored)) OVER (PARTITION BY p.full_name ORDER BY YEAR(m.match_date))
                THEN 'Declining'
                ELSE 'Stable'
            END as trajectory
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN matches m ON ps.match_id = m.match_id
            GROUP BY p.full_name, YEAR(m.match_date)
            ORDER BY p.full_name, year
        """
    }

    selected_query = st.selectbox("Select a Query to Run", list(queries.keys()))

    if st.button("Run Query"):
        with st.spinner("Running query..."):
            df = run_query(queries[selected_query])
            if not df.empty:
                st.success(f"Query returned {len(df)} rows")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Query returned no results.")

    st.markdown("---")
    st.subheader("Custom Query")
    custom_query = st.text_area("Write your own SQL query here:")
    if st.button("Run Custom Query"):
        if custom_query:
            df = run_query(custom_query)
            if not df.empty:
                st.dataframe(df, use_container_width=True)