-- Create player_info table
CREATE TABLE IF NOT EXISTS player_info (
  player_id INTEGER PRIMARY KEY,
  player_name TEXT
);

-- Create score_info table
CREATE TABLE IF NOT EXISTS score_info (
  player_id INTEGER,
  score1 INTEGER,
  level_achieved TEXT,
  FOREIGN KEY (player_id) REFERENCES player_info(player_id)
);