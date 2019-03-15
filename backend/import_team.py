#pip3 install openpyxl#pip3 install openpyxl
import openpyxl
import os

from backend import settings as s
from backend.team import Player

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def import_teams(filename="media/DevMatchData.xlsx"):
    """
    Method for importing teams from a specific .xlsx file.
    :param filename: The filename (in the SoccerSimulator root directory)
    """
    book = openpyxl.load_workbook(BASE_DIR + '/' + filename)
    sheet = book.active

    for row in sheet.iter_rows(min_row=3):
        name = row[7].value
        team = row[4].value
        pos = row[1].value
        stat_att = row[2].value
        stat_def = row[3].value

        new_player = Player(name, pos, stat_att, stat_def)

        if team == 1:
            s.english_team.team.append(new_player)
        elif team == 2:
            s.dutch_team.team.append(new_player)
