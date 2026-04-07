# utils/api_fetcher.py
# This file handles all Cricbuzz API calls
# It fetches live data and stores it in MySQL

import requests
import os
from utils.db_connection import get_connection, close_connection

# Load API key from environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

API_KEY = os.environ.get("RAPIDAPI_KEY")
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

# ─────────────────────────────────────────
# 1. FETCH LIVE MATCHES
# ─────────────────────────────────────────
def fetch_live_matches():
    """Fetch all currently live matches from Cricbuzz API"""
    try:
        url = f"{BASE_URL}/matches/v1/live"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        matches = []
        for type_match in data.get("typeMatches", []):
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    match_info = match.get("matchInfo", {})
                    match_score = match.get("matchScore", {})
                    matches.append({
                        "match_id": match_info.get("matchId"),
                        "description": match_info.get("matchDesc"),
                        "match_format": match_info.get("matchFormat"),
                        "status": match_info.get("status"),
                        "team1": match_info.get("team1", {}).get("teamName"),
                        "team2": match_info.get("team2", {}).get("teamName"),
                        "venue": match_info.get("venueInfo", {}).get("ground"),
                        "city": match_info.get("venueInfo", {}).get("city"),
                        "score": match_score
                    })
        return matches
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching live matches: {e}")
        return []

# ─────────────────────────────────────────
# 2. FETCH UPCOMING MATCHES
# ─────────────────────────────────────────
def fetch_upcoming_matches():
    """Fetch all upcoming matches"""
    try:
        url = f"{BASE_URL}/matches/v1/upcoming"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        matches = []
        for type_match in data.get("typeMatches", []):
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    match_info = match.get("matchInfo", {})
                    matches.append({
                        "match_id": match_info.get("matchId"),
                        "description": match_info.get("matchDesc"),
                        "match_format": match_info.get("matchFormat"),
                        "status": match_info.get("status"),
                        "team1": match_info.get("team1", {}).get("teamName"),
                        "team2": match_info.get("team2", {}).get("teamName"),
                        "venue": match_info.get("venueInfo", {}).get("ground"),
                        "city": match_info.get("venueInfo", {}).get("city"),
                    })
        return matches
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching upcoming matches: {e}")
        return []

# ─────────────────────────────────────────
# 3. FETCH RECENT MATCHES
# ─────────────────────────────────────────
def fetch_recent_matches():
    """Fetch recently completed matches"""
    try:
        url = f"{BASE_URL}/matches/v1/recent"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        matches = []
        for type_match in data.get("typeMatches", []):
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    match_info = match.get("matchInfo", {})
                    matches.append({
                        "match_id": match_info.get("matchId"),
                        "description": match_info.get("matchDesc"),
                        "match_format": match_info.get("matchFormat"),
                        "status": match_info.get("status"),
                        "team1": match_info.get("team1", {}).get("teamName"),
                        "team2": match_info.get("team2", {}).get("teamName"),
                        "venue": match_info.get("venueInfo", {}).get("ground"),
                        "result": match_info.get("status"),
                    })
        return matches
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching recent matches: {e}")
        return []

# ─────────────────────────────────────────
# 4. FETCH MATCH SCORECARD
# ─────────────────────────────────────────
def fetch_scorecard(match_id):
    """Fetch detailed scorecard for a specific match"""
    try:
        url = f"{BASE_URL}/mcenter/v1/{match_id}/scard"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching scorecard: {e}")
        return {}

# ─────────────────────────────────────────
# 5. FETCH TOP BATTING STATS
# ─────────────────────────────────────────
def fetch_top_batting_stats(format_type="ODI"):
    """Fetch top batting statistics"""
    try:
        format_map = {"ODI": "2", "Test": "1", "T20I": "3"}
        format_id = format_map.get(format_type, "2")
        url = f"{BASE_URL}/stats/v1/rankings/batsmen"
        params = {"formatType": format_type.lower()}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("rank", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching batting stats: {e}")
        return []

# ─────────────────────────────────────────
# 6. FETCH TOP BOWLING STATS
# ─────────────────────────────────────────
def fetch_top_bowling_stats(format_type="ODI"):
    """Fetch top bowling statistics"""
    try:
        url = f"{BASE_URL}/stats/v1/rankings/bowlers"
        params = {"formatType": format_type.lower()}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("rank", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching bowling stats: {e}")
        return []