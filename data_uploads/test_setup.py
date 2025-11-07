import pytest
from upload_data import get_all_players, NAME_SPLITTER
from unittest.mock import patch

test_data = [{'matches': [{
    "teams": [[{'hand': 'Right',
                'firstName': 'Eain',
                'rank': '',
                'nationality': '',
                'age': '',
                'lastName': 'Yow Ng'}],
              [{'rank': '',
                'age': '',
                'lastName': 'Farag',
                'nationality': 'Egyptian ',
                'firstName': 'Ali',
                'hand': 'Right'}]]
}]},
    {'matches': [{
        "teams": [[{'hand': 'Right',
                    'firstName': 'test',
                    'rank': '',
                    'nationality': '',
                    'age': '',
                    'lastName': 'one'}],
                  [{'rank': '',
                    'age': '',
                    'lastName': 'two',
                    'nationality': 'Egyptian ',
                    'firstName': 'test',
                    'hand': 'Right'}]]
    }]}]


@patch("setup_players.download_all_data", return_value=test_data)
def test_get_all_players(download_all_data_mock):
    assert get_all_players() == [
        "Eain" + NAME_SPLITTER + "Yow Ng",
        "Ali" + NAME_SPLITTER + "Farag",
        "test" + NAME_SPLITTER + "one",
        "test" + NAME_SPLITTER + "two"
    ]
