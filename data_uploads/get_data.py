"""Downloads all the match data from jsons_October_2023"""
import json
import os

PATHWAY_TO_DATA = r"C:\Users\Gaming PC\Documents\Coding\match_data"

def get_json_folders(dataset_name: str) -> list[str]:
    """Gets each folder name in the folder"""
    folders = os.listdir(PATHWAY_TO_DATA + '\\' + dataset_name)
    for folder in folders:
        if '_json' not in folder:
            folders.pop(folders.index(folder))
    return folders


def get_json_file_names(player_folder_name: str, dataset_name: str) -> list[str]:
    """Gets the file names of a players' matches into a list"""
    return os.listdir(f"{PATHWAY_TO_DATA + '\\' + dataset_name}\{player_folder_name}")


def get_match_data(player_jsons_251023: str, dataset_name: str) -> list[dict]:
    """Gets all the data of a players' matches into a list"""
    match_file_names = get_json_file_names(player_jsons_251023, dataset_name)
    matches = []
    for file_name in match_file_names:
        if '.json' in file_name:
            with open(f"{PATHWAY_TO_DATA + '\\' + dataset_name}\{player_jsons_251023}\{file_name}", 'r') as data:
                match = json.load(data)
                match['file_name'] = file_name
                matches.append(match)

    return matches


def download_all_data(dataset_name: str) -> list[dict]:
    """Downloads all the match data from specific dataset"""
    player_folders = get_json_folders(dataset_name)
    matches = []
    for player in player_folders:
        player_data = get_match_data(player, dataset_name)
        matches.extend(player_data)
    return matches