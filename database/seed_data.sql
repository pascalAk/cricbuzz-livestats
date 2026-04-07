USE cricbuzz_db;

-- TEAMS
INSERT INTO teams (team_name, short_name, country, team_type) VALUES
('India', 'IND', 'India', 'international'),
('Australia', 'AUS', 'Australia', 'international'),
('England', 'ENG', 'England', 'international'),
('Pakistan', 'PAK', 'Pakistan', 'international'),
('South Africa', 'SA', 'South Africa', 'international'),
('New Zealand', 'NZ', 'New Zealand', 'international'),
('West Indies', 'WI', 'West Indies', 'international'),
('Sri Lanka', 'SL', 'Sri Lanka', 'international');

-- VENUES
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33108),
('Eden Gardens', 'Kolkata', 'India', 68000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Lords Cricket Ground', 'London', 'England', 30000),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
('Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000),
('MA Chidambaram Stadium', 'Chennai', 'India', 50000),
('Sydney Cricket Ground', 'Sydney', 'Australia', 48000);

-- PLAYERS
INSERT INTO players (full_name, country, date_of_birth, playing_role, batting_style, bowling_style, team_id) VALUES
('Virat Kohli', 'India', '1988-11-05', 'Batsman', 'Right-hand bat', 'Right-arm medium', 1),
('Rohit Sharma', 'India', '1987-04-30', 'Batsman', 'Right-hand bat', 'Right-arm off-break', 1),
('Jasprit Bumrah', 'India', '1993-12-06', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
('Ravindra Jadeja', 'India', '1988-12-06', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
('Steve Smith', 'Australia', '1989-06-02', 'Batsman', 'Right-hand bat', 'Right-arm leg-break', 2),
('Pat Cummins', 'Australia', '1993-05-08', 'Bowler', 'Right-hand bat', 'Right-arm fast', 2),
('Mitchell Starc', 'Australia', '1990-01-30', 'Bowler', 'Left-hand bat', 'Left-arm fast', 2),
('Joe Root', 'England', '1990-12-30', 'Batsman', 'Right-hand bat', 'Right-arm off-break', 3),
('Ben Stokes', 'England', '1991-06-04', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', 3),
('Babar Azam', 'Pakistan', '1994-10-15', 'Batsman', 'Right-hand bat', 'Right-arm off-break', 4),
('Shaheen Afridi', 'Pakistan', '1999-04-06', 'Bowler', 'Left-hand bat', 'Left-arm fast', 4),
('Kagiso Rabada', 'South Africa', '1995-05-25', 'Bowler', 'Right-hand bat', 'Right-arm fast', 5),
('Kane Williamson', 'New Zealand', '1990-08-08', 'Batsman', 'Right-hand bat', 'Right-arm off-break', 6),
('MS Dhoni', 'India', '1981-07-07', 'Wicket-keeper', 'Right-hand bat', 'Right-arm medium', 1),
('Shubman Gill', 'India', '1999-09-08', 'Batsman', 'Right-hand bat', 'Right-arm off-break', 1);

-- SERIES
INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
('ICC World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
('Border-Gavaskar Trophy 2024', 'Australia', 'Test', '2024-11-22', '2025-01-03', 5),
('IPL 2024', 'India', 'T20', '2024-03-22', '2024-05-26', 74),
('Ashes 2023', 'England', 'Test', '2023-06-16', '2023-07-31', 5),
('Asia Cup 2024', 'Sri Lanka', 'ODI', '2024-08-30', '2024-09-15', 13);

-- MATCHES
INSERT INTO matches (series_id, match_description, team1_id, team2_id, venue_id, match_date, match_type, status, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type) VALUES
(1, 'India vs Pakistan, ICC World Cup 2023', 1, 4, 7, '2023-10-14', 'ODI', 'completed', 1, 'bat', 1, '7 wickets', 'wickets'),
(1, 'India vs Australia, ICC World Cup 2023 Final', 1, 2, 2, '2023-11-19', 'ODI', 'completed', 2, 'bat', 2, '6 wickets', 'wickets'),
(2, 'Australia vs India, 1st Test', 2, 1, 3, '2024-11-22', 'Test', 'completed', 2, 'bat', 1, '295 runs', 'runs'),
(4, 'England vs Australia, 1st Ashes Test', 3, 2, 4, '2023-06-16', 'Test', 'completed', 3, 'bowl', 2, '2 wickets', 'wickets'),
(1, 'India vs New Zealand, ICC World Cup 2023', 1, 6, 1, '2023-10-22', 'ODI', 'completed', 1, 'bat', 1, '4 wickets', 'wickets');

-- CAREER STATS
INSERT INTO career_stats (player_id, format, matches_played, total_runs, highest_score, batting_average, batting_sr, centuries, fifties, total_wickets, bowling_average, economy_rate, best_bowling, total_catches) VALUES
(1, 'ODI', 292, 13906, 183, 57.32, 93.17, 46, 72, 4, 166.0, 5.27, '1/15', 125),
(1, 'Test', 113, 8848, 254, 49.15, 55.73, 29, 30, 0, NULL, NULL, NULL, 95),
(1, 'T20I', 115, 4038, 122, 52.44, 137.04, 1, 37, 0, NULL, NULL, NULL, 55),
(2, 'ODI', 264, 10709, 264, 48.93, 89.48, 31, 57, 8, 152.0, 5.11, '2/27', 145),
(2, 'Test', 67, 3547, 212, 40.77, 57.91, 9, 17, 0, NULL, NULL, NULL, 52),
(5, 'Test', 110, 9360, 239, 56.03, 55.26, 32, 38, 17, 71.0, 2.82, '3/18', 145),
(8, 'Test', 145, 12109, 254, 51.31, 55.24, 32, 61, 41, 101.0, 2.79, '5/8', 162),
(10, 'ODI', 104, 5151, 158, 59.78, 88.21, 18, 31, 2, 194.0, 5.26, '1/33', 35),
(3, 'ODI', 83, 101, 35, 5.94, 78.91, 0, 0, 151, 22.42, 4.56, '6/19', 22),
(11, 'ODI', 67, 245, 42, 9.07, 85.66, 0, 0, 122, 23.15, 5.01, '6/35', 12);

-- PLAYER STATS (match by match)
INSERT INTO player_stats (player_id, match_id, format, innings, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, overs_bowled, runs_conceded, wickets_taken, economy_rate, catches) VALUES
(1, 1, 'ODI', 1, 3, 122, 111, 12, 2, 109.90, 0, 0, 0, 0.00, 1),
(2, 1, 'ODI', 1, 1, 87, 91, 9, 1, 95.60, 0, 0, 0, 0.00, 0),
(4, 1, 'ODI', 1, 6, 45, 35, 3, 2, 128.57, 8.0, 43, 2, 5.37, 2),
(3, 1, 'ODI', 2, 9, 12, 18, 1, 0, 66.67, 9.4, 44, 2, 4.55, 1),
(1, 2, 'ODI', 1, 3, 54, 63, 5, 1, 85.71, 0, 0, 0, 0.00, 0),
(5, 2, 'ODI', 2, 4, 61, 73, 6, 0, 83.56, 0, 0, 0, 0.00, 2),
(6, 2, 'ODI', 2, 9, 24, 28, 2, 0, 85.71, 9.0, 51, 3, 5.66, 0),
(8, 4, 'Test', 1, 4, 110, 185, 14, 1, 59.45, 8.0, 42, 1, 5.25, 1),
(9, 4, 'Test', 1, 6, 155, 206, 21, 4, 75.24, 12.0, 61, 4, 5.08, 2),
(1, 5, 'ODI', 1, 3, 95, 105, 9, 2, 90.47, 0, 0, 0, 0.00, 2);