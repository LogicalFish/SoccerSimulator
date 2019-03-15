from backend.import_team  import import_teams
from backend.team import Team

#Field Dimensions of the Estádio D. Afonso Henriques
#Source: https://www.transfermarkt.nl/vitoria-guimaraes-sc/stadion/verein/2420
FIELD_LENGTH = 10600 #(cm)
FIELD_WIDTH = 6800 #(cm)

english_team = Team("England")
dutch_team = Team("The Netherlands")

import_teams()

# english_team.populate_team()
# dutch_team.populate_team()

max_time = 90*60

#Odds for passing the ball each second (out of a 100)
PASS_ODDS = 18
#Odds for shooting the ball each second close to the goal (out of a 100)
SHOOT_CLOSE_ODDS = 5
#Odds for shooting the ball each second far from the goal (out of a 1000)
SHOOT_FAR_ODDS = 2

#Starting Speed of an average player (cm per second)
PLAYER_SPEED = 200