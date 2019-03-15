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

MAX_TIME = 90 * 60

#Time (in seconds) each step of the match takes
STEP_SIZE = 2

#Odds for passing the ball each step (out of a 100)
PASS_ODDS = 18
#The distance to the goal (in cm) at which point a player might decide to make an attempt to shoot.
SHOOT_DISTANCE = 1600
#Odds for shooting the ball each step close to the goal (out of a 100)
SHOOT_CLOSE_ODDS = 5
#Odds for shooting the ball each step far from the goal (out of a 1000)
SHOOT_FAR_ODDS = 2

#Speed stats of an average player (cm per step)
PLAYER_SPEED = 200
MAX_SPEED = 500
#How fast a player can accelerate/decellerate (cm per step).
#If Decay is higher, a player will slow down on average.
#If Accel is higher, a player will speed up on average.
SPEED_DECAY = -40
SPEED_ACCEL = 25
#Minimum speed modifier. Determines minimum speed of a player within enemy territory
MIN_SPEED_MOD = 0.25

#Minimum and maximum distance (in cm) that a ball is kicked during a kickoff.
KICK_OFF_MIN = 1000
KICK_OFF_MAX = 2000

#Minimum and maximum distance (in cm) that a ball is kicked when passed.
PASS_MIN = 500
PASS_MAX = 2500

#The minimum chance that a ball shot towards the goal actually reaches the goal.
MINIMUM_GOAL_CHANCE = 5