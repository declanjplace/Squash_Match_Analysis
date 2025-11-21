from get_data import download_all_data
import psycopg2 as psy
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

NAME_SPLITTER = '-_-'

# Database connecting functions


def get_db_connection(database_name: str) -> connection:
    """Returns a live connection from a database."""
    return psy.connect(f"dbname={database_name}", cursor_factory=RealDictCursor)

# ID retrieving functions


def get_player_id(player_name: str, conn: connection) -> int:
    """
    Connects to the database to retrieve the associated player id
    """
    cursor = conn.cursor()
    cursor.execute(
        f"""
        WITH full_names AS (
            SELECT player_id, 
                concat(first_name + last_name) AS full_name
            FROM player
        )
        SELECT player_id FROM full_names
        WHERE full_name = '{player_name}'
        ;
        """
    )
    player_id = cursor.fetchall()
    if len(player_id) == 0:
        raise Exception(f"{player_name} is not in the database")
    elif len(player_id) != 1:
        raise Exception(
            f"There are multiple players with the name: {player_name}")
    cursor.close()
    return player_id[0]


def get_tournament_id(tournament_name: str, conn: connection) -> int:
    """
    Connects to the database to retrieve the associated tournament id
    """
    cursor = conn.cursor()
    cursor. execute(
        f"""
            SELECT tournament_id 
            FROM tournament 
            WHERE tournament_name = '{tournament_name}'
            ;
        """
    )
    tournament_id = cursor.fetchall()
    if len(tournament_id) == 0:
        raise Exception(f"{tournament_name} is not in the database")
    elif len(tournament_id) != 1:
        raise Exception(
            f"There are multiple tournaments with the name: {tournament_name}")
    cursor.close()
    return tournament_id[0]


def get_match_id(match: dict, conn: connection):
    """
    Connects to the database to get the match id 
    """
    tournament_id = get_tournament_id(match[0]['tournament'], conn)
    player_a_name = match['matches'][0]['teams'][0]['firstName']
    player_a_name += match['matches'][0]['teams'][0]['lastName']
    player_b_name = match['matches'][0]['teams'][1]['firstName'][0]
    player_b_name += match['matches'][0]['teams'][1]['lastName'][0]
    tournament_round_number = match[0]['round']
    identifier = tournament_id + tournament_round_number + player_a_name + player_b_name
    cursor = conn.cursor()
    cursor.execute(
        f"""
            WITH get_match_id AS (
            SELECT match_id, 
                concat(CONVERT(tournament_id, CHAR), round,
                    CONVERT(player_a_id, CHAR), CONVERT(player_b_id, CHAR)
                ) AS match_string_identifier 
            FROM match 
            )
            SELECT match_id 
            FROM get_match_id
            WHERE match_string_identifier = '{identifier}'
        ;"""
    )
    match_id = cursor.fetchall()
    if len(match_id) == 0:
        raise Exception(f"{match_id} is not in the database")
    elif len(match_id) != 1:
        raise Exception(
            f"There are multiple tournaments with the name: {match_id}")
    cursor.close()
    return match_id[0]
# formatting/cleaning functions

def get_rally_winner_name(match: dict, game: dict) -> str:
    """
    Get the rallies full name
    """
    teams = match['matches'][0]['teams']
    game_winner_number = game['winner']
    if game_winner_number == 0:
        return teams[0]['firstName'] + teams[0]['lastName']
    return teams[1]['firstName'] + teams[1]['lastName']

def get_game_winner_name(match: dict, game: dict) -> str:
    """
    Gets the game winner full name
    """
    teams = match['matches'][0]['teams']
    game_winner_number = game['winner']
    if game_winner_number == 0:
        return teams[0]['firstName'] + teams[0]['lastName']
    return teams[1]['firstName'] + teams[1]['lastName']


def clean_shot(shot: dict):
    """
    When given a shot's (dict) data checks validity of each key 
    """
    pass


def format_date(date: str) -> str:
    """
    Formats date for SQL dates
    """
    date_splits = date.spilt('/')
    return f"{date_splits[2]}-{date_splits[1]}-{date_splits[0]}"

# Player functions



def get_all_players(match_data: list[dict]) -> list[str]:
    """
    Gets all the players and needed data for insertion to database
    """
    player_list = []
    for match in match_data:
        for player in match['matches'][0]['teams']:
            full_name = player[0]['firstName'] + \
                NAME_SPLITTER + player[0]['lastName']
            if full_name not in player_list:
                player_list.append(full_name)
    return player_list


def upload_players(raw_match_data: list[dict], conn: connection, database_name: str):
    """
    Uploads players to the database
    """
    cursor = conn.cursor()
    players = get_all_players(raw_match_data)
    for player in players:
        first_name = player.split(NAME_SPLITTER)[0]
        last_name = player.split(NAME_SPLITTER)[1]
        cursor.execute(
            f"""INSERT INTO player (first_name, last_name) 
            VALUES ('{first_name}', '{last_name}');"""
        )
        conn.commit()
    cursor.close()
    print(f"Players have been uploaded into {database_name}")

# Tournaments functions


def get_all_tournaments(raw_match_data: list[dict]) -> list[str]:
    """
    Gets all the tournament names
    """
    tournaments = []
    for match in raw_match_data:
        tournament = match['matches'][0]['tournament']
        if tournament not in tournaments:
            tournaments.append(tournament)
    return tournaments


def upload_tournaments(raw_match_data: list[dict], conn: connection, database_name: str):
    """
    Uploads tournaments to a specified database
    """
    cursor = conn.cursor()
    tournaments = get_all_tournaments(raw_match_data)
    for tournament in tournaments:
        cursor.execute(
            f"""INSERT INTO player (first_name, last_name) 
            VALUES ('{tournament}');"""
        )
    cursor.close()
    print(f"tournaments have been uploaded to {database_name}")

# Match functions


def format_match(match: dict, conn: connection) -> dict:
    """
    Formats match data to be entered into the database
    """
    player_a = match['matches'][0]['teams'][0]['firstName']
    player_a += match['matches'][0]['teams'][0]['lastName']
    player_b = match['matches'][0]['teams'][1]['firstName']
    player_b += match['matches'][0]['teams'][1]['lastName']
    formatted_match = {
        "player_a_id": get_player_id(player_a, conn),
        "player_b_id": get_player_id(player_b, conn),
        "tournament_id": get_tournament_id(match['tournament'], conn),
        "round": match['round'],
        "date": format_match(match['date']),
        "referee": match['referee'],
        "country": match['country'],
        "court_type": match['court_type'],
        "court_size": match['court_size'],
        "recorder": match['recorder']
    }
    return formatted_match


def format_matches(raw_matches: list[dict], conn: connection) -> list[dict]:
    """
    Gets all the matches in the format to be inserted into the database
    """
    matches = []
    for match in raw_matches:
        matches.append(format_match(match, conn))
    return matches


def upload_matches(database_name: str, raw_matches: list[dict], conn: connection):
    """
    Uploads all matches to the database
    """
    matches = format_matches(raw_matches, conn)
    cursor = conn.cursor()
    for match in matches:
        cursor.execute(
            f"""
                INSERT INTO match (
                    player_a_id, player_b_id, 
                    tournament_id, round, date, referee,
                    country, court_type, court_size, recorder
                ) 
                VALUES (
                    '{match['player_a_id']}', '{match['player_b_id']}', 
                    '{match['tournament_id']}', '{match['round']}', 
                    '{match['date']}', {match['referee']}, 
                    '{match['country']}', '{match['court_type']}',
                    '{match['court_size']}', '{match['recorder']}'
                );
            """
        )
        conn.commit()
    cursor.close()
    print(f"Matches have been uploaded to {database_name}")

# Game functions


def format_game(match: dict, conn: connection) -> list[dict]:
    """
    Takes a match an retrieves each game with respective data
    """
    games = []
    for game in match['matches'][0]['games']:
        winner_name = get_game_winner_name(match, game)
        games.append({
            "match_id": get_match_id(match, conn),
            "game_number": game['gameNumber'],
            "winner_id": get_player_id(winner_name, conn)
        })
    return games


def get_games(match_data: list[dict], conn: connection) -> list[dict]:
    """
    Gets all the games 
    """
    games = []
    for match in match_data:
        games.extend(format_game(match, conn))
    return games
    


def upload_games(match_data: list[dict], conn: connection, database_name: str):
    """
    Uploads all games to the database
    """
    games = get_games(match_data, conn)
    cursor = conn.cursor()
    for game in games:
        cursor.execute(
            f"""
            INSERT INTO game VALUES (
                match_id, game_number, winner_id
            )
            VALUES (
                '{game["match_id"]}', '{game['game_number']}', '{game['winner_id']}'
            );
            """
        )
        conn.commit()
    cursor.close()
    print(f"Games have been uploaded to {database_name}")


# Rally functions

def format_rally(match: list[dict], conn: connection) -> list[dict]:
    """
    Takes all the rallies in a list of games game and formats them into a list
    """

    for game in match:
        rally_winner = get_rally_winner_name(match, game)
        


def get_rallies(match_data: list[dict], conn: connection) -> list[dict]:
    """
    Gets all rallies
    """
    rallies = []
    for match in match_data:
        for game in match[0]['games']:
            for rally in game['rallies']:
                rallies.extend(format_rally(rally, conn))

def upload_rallies(match_data: list[dict], conn: connection, database_name: str):
    """
    Uploads all rallies to the database
    """
    rallies = get_rallies(match_data, conn)

# Shot functions


def upload_shots(match_data: list[dict], conn: connection, database_name: str):
    """
    Uploads all shots to the database
    """
    pass

# All together now


def upload_to_database(database_name: str):
    """
    Uploads all the data formatted a database
    """
    conn = get_db_connection(database_name)
    raw_match_data = download_all_data()
    upload_players(raw_match_data, conn, database_name)
    upload_tournaments(raw_match_data, conn, database_name)
    upload_games(raw_match_data, conn, database_name)
    upload_rallies(raw_match_data, conn, database_name)
    upload_shots(raw_match_data, conn, database_name)
    conn.close()