
class Team:

    def __init__(self, name):
        self.name = name
        self.goal_pos = -1
        # self.players = []
        # self.substitutes = []

    def __str__(self):
        return self.name

    def set_goal(self, goal_pos):
        self.goal_pos = goal_pos

    def get_dir(self, bal_pos):
        x = bal_pos - self.goal_pos #If positive, goal = 0
        signbit = -1 if x < 0 else 1
        return signbit

    def add_player(self, player, substitute=False):
        if substitute or len(self.players) == 11:
            self.players.append(player)
        else:
            self.substitutes.append(player)


class Player:

    def __init__(self, name, position, stat_att, stat_def):
        self.name = name
        self.position = position
