import random


class Team:

    def __init__(self, name):
        self.name = name
        self.goal_pos = -1
        self.team = []
        self.field_team = []

    def __str__(self):
        return self.name

    def set_goal(self, goal_pos):
        self.goal_pos = goal_pos

    def get_dir(self, bal_pos):
        x = bal_pos - self.goal_pos #If positive, goal = 0
        signbit = -1 if x < 0 else 1
        return signbit

    def add_player(self, player):
        self.team.append(player)

    def get_player(self, name):
        for player in self.team:
            if player.name == name:
                return player

    def get_position_list(self, position, field=True):
        result = []
        if field:
            team = self.field_team
        else:
            team = self.team
        for player in team:
            if player.position == position:
                result.append(player)
        return result

    def populate_team(self, count={"G":1,"D":4,"M":3,"A":3}):
        for position in count.keys():
            eligible_players = self.get_position_list(position, False)
            selection = random.sample(eligible_players, count[position])
            for s in selection:
                self.field_team.append(s)


class Player:

    def __init__(self, name, position, stat_att, stat_def):
        self.name = name
        self.position = position
        self.stat_att = stat_att
        self.stat_def = stat_def

    def __str__(self):
        return self.name

    def stat_overall(self):
        return max(self.stat_att, self.stat_def)
