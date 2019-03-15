import random


class Team:
    """
    A class representing a team of players.
    Attributes:
        name: The name of the team
        goal_pos: The position of the team's goal. To be initialized later.
        team: The players in the team.
        field_team: The players of this team on the field.
    """

    def __init__(self, name):
        self.name = name
        self.goal_pos = -1
        self.team = []
        self.field_team = []

    def __str__(self):
        return self.name

    def get_dir(self, bal_pos):
        """
        Method for getting the direction this team wants the ball to go.
        :param bal_pos: The position of the ball.
        :return: -1 if the ball should go 'left, 1 if the ball should go 'right'
        """
        x = bal_pos - self.goal_pos #If positive, goal = 0
        signbit = -1 if x < 0 else 1
        return signbit

    def get_player(self, name):
        """
        UNUSED METHOD: Gets a Player object based on a name.
        :param name: The name of the player you are looking for.
        :return: The Player Object
        """
        for player in self.team:
            if player.name == name:
                return player

    def get_position_list(self, position, field=True):
        """
        Get the list of all players that play a specific position.
        :param position: A letter signifying the position. See Player object for more details
        :param field: Boolean signifying whether the returned players should be on the field or not.
        :return: A list of players
        """
        result = []
        if field:
            team = self.field_team
        else:
            team = self.team
        for player in team:
            if player.position == position:
                result.append(player)
        return result

    def populate_team(self, headcount={"G":1, "D":4, "M":3, "A":3}):
        """
        Select random members from the team to form a field_team.
        :param headcount: A dictionary stating how many players of each position should be on the team.
        """
        self.field_team.clear()
        for position in headcount.keys():
            eligible_players = self.get_position_list(position, False)
            selection = random.sample(eligible_players, headcount[position])
            for s in selection:
                self.field_team.append(s)


class Player:
    """
    A class representing a single Soccer Player.
    Attributes:
        Name: The Player's full name.
        Position: The Player's preferred position as a one-letter string.
            (G = Goalkeeper
            D = Defender
            M = Midfielder
            A = Attacker)
        stat_att: The attack stat
        stat_def: The defense stat
    """

    def __init__(self, name, position, stat_att, stat_def):
        self.name = name
        self.position = position
        self.stat_att = stat_att
        self.stat_def = stat_def

    def __str__(self):
        return self.name

    def stat_overall(self):
        """
        Method to return the highest stat of attack/defense
        :return: int reflecting the highest stat
        """
        return max(self.stat_att, self.stat_def)
