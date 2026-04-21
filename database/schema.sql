-- ============================================
-- CRICBUZZ LIVESTATS - DATABASE SCHEMA
-- ============================================

USE cricbuzz_db;

-- 1. TEAMS TABLE
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(10),
    country VARCHAR(100),
    team_type ENUM('international', 'domestic') DEFAULT 'international',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. VENUES TABLE
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(200) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. PLAYERS TABLE
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    date_of_birth DATE,
    playing_role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper'),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(100),
    team_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- 4. SERIES TABLE
CREATE TABLE series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    start_date DATE,
    end_date DATE,
    total_matches INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. MATCHES TABLE
CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    series_id INT,
    match_description VARCHAR(300),
    team1_id INT,
    team2_id INT,
    venue_id INT,
    match_date DATE,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    status ENUM('upcoming', 'live', 'completed') DEFAULT 'upcoming',
    toss_winner_id INT,
    toss_decision ENUM('bat', 'bowl'),
    winner_id INT,
    victory_margin VARCHAR(100),
    victory_type ENUM('runs', 'wickets', 'draw', 'tie', 'no result'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id)
);

-- 6. PLAYER STATS TABLE
CREATE TABLE player_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    format ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    innings INT DEFAULT 1,
    batting_position INT,
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate DECIMAL(6,2),
    overs_bowled DECIMAL(4,1),
    runs_conceded INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    economy_rate DECIMAL(5,2),
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- 7. CAREER STATS TABLE
CREATE TABLE career_stats (
    career_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    format ENUM('Test', 'ODI', 'T20I', 'T20', 'Other'),
    matches_played INT DEFAULT 0,
    total_runs INT DEFAULT 0,
    highest_score INT DEFAULT 0,
    batting_average DECIMAL(6,2),
    batting_sr DECIMAL(6,2),
    centuries INT DEFAULT 0,
    fifties INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    bowling_average DECIMAL(6,2),
    economy_rate DECIMAL(5,2),
    best_bowling VARCHAR(10),
    total_catches INT DEFAULT 0,
    total_stumpings INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);