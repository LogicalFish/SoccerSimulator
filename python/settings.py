from python.import_team import import_teams
from python.team import Team

FIELD_LENGTH = 10600 #(cm)
FIELD_WIDTH = 6800 #(cm)

english_team = Team("England")
dutch_team = Team("The Netherlands")

import_teams()

english_team.populate_team()
dutch_team.populate_team()
# for player in english_team.field_team:
#     print("{} ({}):\tAttack: {},\tDefense: {}".format(player, player.position, player.stat_att, player.stat_def))

max_time = 90*60



#Initialize Players
