-- ============================================================
-- Cricbuzz LiveStats - Database Schema
-- Compatible with SQLite, PostgreSQL, and MySQL
-- ============================================================

CREATE TABLE IF NOT EXISTS teams (
    team_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT    NOT NULL,
    country   TEXT    NOT NULL,
    short_name TEXT
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT    NOT NULL,
    city       TEXT    NOT NULL,
    country    TEXT    NOT NULL,
    capacity   INTEGER
);

CREATE TABLE IF NOT EXISTS series (
    series_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name   TEXT    NOT NULL,
    host_country  TEXT,
    match_type    TEXT,
    start_date    TEXT,
    end_date      TEXT,
    total_matches INTEGER
);

CREATE TABLE IF NOT EXISTS players (
    player_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name    TEXT    NOT NULL,
    country      TEXT    NOT NULL,
    playing_role TEXT,
    batting_style TEXT,
    bowling_style TEXT,
    date_of_birth TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id         INTEGER REFERENCES series(series_id),
    match_description TEXT,
    team1_id          INTEGER REFERENCES teams(team_id),
    team2_id          INTEGER REFERENCES teams(team_id),
    venue_id          INTEGER REFERENCES venues(venue_id),
    match_date        TEXT,
    match_format      TEXT,
    status            TEXT    DEFAULT 'Completed',
    winning_team_id   INTEGER REFERENCES teams(team_id),
    victory_margin    INTEGER,
    victory_type      TEXT,
    toss_winner_id    INTEGER REFERENCES teams(team_id),
    toss_decision     TEXT
);

CREATE TABLE IF NOT EXISTS batting_performances (
    perf_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER REFERENCES matches(match_id),
    player_id       INTEGER REFERENCES players(player_id),
    innings_number  INTEGER DEFAULT 1,
    runs_scored     INTEGER DEFAULT 0,
    balls_faced     INTEGER DEFAULT 0,
    batting_position INTEGER,
    fours           INTEGER DEFAULT 0,
    sixes           INTEGER DEFAULT 0,
    strike_rate     REAL,
    is_not_out      INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bowling_performances (
    perf_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id       INTEGER REFERENCES matches(match_id),
    player_id      INTEGER REFERENCES players(player_id),
    innings_number INTEGER DEFAULT 1,
    overs_bowled   REAL    DEFAULT 0,
    wickets_taken  INTEGER DEFAULT 0,
    runs_conceded  INTEGER DEFAULT 0,
    economy_rate   REAL,
    maiden_overs   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fielding_performances (
    perf_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id   INTEGER REFERENCES matches(match_id),
    player_id  INTEGER REFERENCES players(player_id),
    catches    INTEGER DEFAULT 0,
    stumpings  INTEGER DEFAULT 0,
    run_outs   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS player_career_stats (
    stat_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id        INTEGER REFERENCES players(player_id),
    format           TEXT,
    matches_played   INTEGER DEFAULT 0,
    innings          INTEGER DEFAULT 0,
    runs_scored      INTEGER DEFAULT 0,
    highest_score    INTEGER DEFAULT 0,
    batting_average  REAL,
    strike_rate      REAL,
    centuries        INTEGER DEFAULT 0,
    half_centuries   INTEGER DEFAULT 0,
    wickets_taken    INTEGER DEFAULT 0,
    bowling_average  REAL,
    economy_rate     REAL,
    catches          INTEGER DEFAULT 0,
    stumpings        INTEGER DEFAULT 0,
    UNIQUE(player_id, format)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_matches_date        ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format      ON matches(match_format);
CREATE INDEX IF NOT EXISTS idx_batting_match       ON batting_performances(match_id);
CREATE INDEX IF NOT EXISTS idx_batting_player      ON batting_performances(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_match       ON bowling_performances(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player      ON bowling_performances(player_id);
CREATE INDEX IF NOT EXISTS idx_career_player       ON player_career_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_career_format       ON player_career_stats(format);
