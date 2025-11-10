
CREATE TABLE player (
    player_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age SMALLINT,
    nationality VARCHAR(50),
    rank SMALLINT,
    hand VARCHAR(5),
    PRIMARY KEY (player_id)
);

CREATE TABLE tournament (
    tournament_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    tournament_name VARCHAR(50) UNIQUE NOT NULL,
    level VARCHAR(15),
    PRIMARY KEY (tournament_id)
);

CREATE TABLE match (
    match_id BIGINT GENERATED ALWAYS AS IDENTITY,
    player_a_id SMALLINT,
    player_b_id SMALLINT,
    tournament_id SMALLINT,
    round VARCHAR(20),
    date DATE,
    referee VARCHAR(100),
    country VARCHAR(50),
    court_type VARCHAR(50),
    court_size VARCHAR(10),
    recorder VARCHAR(50),
    PRIMARY KEY (match_id),
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
);

CREATE TABLE game (
    game_id BIGINT GENERATED ALWAYS AS IDENTITY,
    match_id BIGINT,
    game_number SMALLINT,
    winner_id SMALLINT,
    FOREIGN KEY (match_id) REFERENCES match(match_id),
    FOREIGN KEY (winner_id) REFERENCES player(player_id)
);

CREATE TABLE rally (
    rally_id BIGINT GENERATED ALWAYS AS IDENTITY,
    game_id BIGINT,
    match_id BIGINT,
    player_a_score SMALLINT,
    player_b_score SMALLINT,
    winner_id SMALLINT,
    win_method VARCHAR(100),
    final_position_x FLOAT,
    final_position_y FLOAT,
    reliable_timing VARCHAR(5),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (match_id) REFERENCES match(match_id),
    FOREIGN KEY (winner_id) REFERENCES player(player_id)
);

CREATE TABLE shot (
    shot_id BIGINT GENERATED ALWAYS AS IDENTITY,
    rally_id BIGINT,
    game_id BIGINT,
    match_id BIGINT,
    player_id SMALLINT,
    x-coordinate FLOAT,
    y-coordinate FLOAT,
    timestamp FLOAT,
    volley VARCHAR(5),
    boast VARCHAR(5),
    backwall VARCHAR(5),
    soft VARCHAR(5),
    PRIMARY KEY (shot_id),
    FOREIGN KEY (rally_id) REFERENCES rally(rally_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (match_id) REFERENCES match(match_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);
