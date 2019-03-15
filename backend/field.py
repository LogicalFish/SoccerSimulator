import random
from backend import settings as s


class Field:
    """
    Class representing the playing field, with methods to move the ball around.
    Attributes:
            teams: Tuple of the two teams. First element is the starting team.
            ball_pos: Current position of the ball on the field.
            ball_owner: Player that is in possession of the ball.
            scores: Dictionary tracking the scores of each team.

    """

    def __init__(self, team_start, team_other):
        """
        Initialization method.
        :param team_start: The team that starts the match during the kick-off
        :param team_other: The other team.
        """
        self.teams = (team_start, team_other)
        self.teams[0].goal_pos = 0
        self.teams[1].goal_pos = s.FIELD_LENGTH
        self.ball_pos = s.FIELD_LENGTH/2
        self.ball_owner = random.choice(self.teams[0].get_position_list("A"))
        self.scores = {self.teams[0]: 0, self.teams[1]: 0}
        self.speed = s.PLAYER_SPEED

    def __str__(self):
        """
        :return: String with current status of the field.
        """
        result = "Current Ball Position = {}. Currently on Ball: {}. Score = {}-{}."
        result = result.format((self.ball_pos*100 / s.FIELD_LENGTH),
                               self.ball_owner,
                               self.scores[self.teams[0]],
                               self.scores[self.teams[1]]
                               )
        return result

    def get_team(self):
        """
        :return: The team that currently has the ball.
        """
        for team in self.teams:
            if self.ball_owner in team.field_team:
                return team
        raise ValueError

    def get_status(self):
        """
        :return: The current state of the match
        """
        return {'ball': self.ball_pos,
                'owner': self.ball_owner,
                'owner-team': self.get_team(),
                'team1': self.teams[0],
                'score1': self.scores[self.teams[0]],
                'team2': self.teams[1],
                'score2': self.scores[self.teams[1]],
                }

    def halftime(self):
        """
        Helper method for switching the teams around during halftime and resetting the ball.
        """
        self.ball_pos = s.FIELD_LENGTH/2

        self.teams[0].goal_pos = s.FIELD_LENGTH
        self.teams[1].goal_pos = 0

        self.ball_owner = random.choice(self.teams[1].get_position_list("A"))

    @staticmethod
    def get_zone(goal_distance):
        """
        Static helper method that specifies which soccer players can be found where in the field.
        :param goal_distance: the distance of the ball to the goal.
        :return: A if the ball is close to the opponent's goal, M if it is in the middle, D if the ball is close to their own goal.
        """
        if goal_distance >= s.FIELD_LENGTH * (2 / 3):
            return "D"
        elif s.FIELD_LENGTH * (2 / 3) > goal_distance >= s.FIELD_LENGTH / 3:
            return "M"
        elif s.FIELD_LENGTH / 3 > goal_distance:
            return "A"

    def ball_switch(self):
        """
        Helper method for switching the ball to the other team.
        :return: the team that now owns the ball
        """
        for team in self.teams:
            if self.ball_owner not in team.field_team:
                self.ball_owner = random.choice(team.get_position_list(self.get_zone(s.FIELD_LENGTH - self.goal_distance())))
                self.speed = s.PLAYER_SPEED
                return team

    def goal_distance(self):
        """
        Helper method for calculating the ball's distance to the goal.
        :return: the distance of the ball to the opposing team's goal.
        """
        if self.get_team().goal_pos == 0:
            return s.FIELD_LENGTH - self.ball_pos
        else:
            return self.ball_pos

    def move_ball(self):
        """
        Method for moving the ball (and player) to a new position.
        The new position is based on the following factors:
            A. How long the player has owned the ball.
            B. How far the player is from the opposing team's goal.
            C. A random factor.
        :return:
        """
        movement = random.randint(self.speed - 40, min(self.speed + 25, 500))
        modifier = max(0.25, self.goal_distance()/s.FIELD_LENGTH)
        self.ball_pos += movement * self.get_team().get_dir(self.ball_pos) * modifier
        self.speed = movement

    def kick_off(self):
        """
        Method for a kick-off, where the ball is kicked backwards towards the own team.
        """
        movement = 1000
        if self.ball_pos == 0:
            direction = 1
        elif self.ball_pos == s.FIELD_LENGTH:
            direction = -1
        elif self.ball_pos == s.FIELD_LENGTH/2:
            direction = self.get_team().get_dir(self.ball_pos)*-1
        self.ball_pos += movement * direction

    def pass_ball(self):
        """
        Method for passing the ball to another player on the same team.
        There's a chance the pass fails, based on the statistics of the player owning the ball.
        If the pass succeeds, the ball moves forward to a new player.
        If the pass succeeds, the enemy gains control of the ball.
        """
        chance_success = self.ball_owner.stat_overall()

        zero_point = s.FIELD_LENGTH*.75 - self.get_team().goal_pos/2
        modifier = (self.ball_pos-zero_point) / (self.get_team().goal_pos-zero_point)

        movement = 1500*modifier
        direction = self.get_team().get_dir(self.ball_pos)
        self.ball_pos += movement * direction
        if random.randint(1, 100) <= chance_success:
            self.ball_owner = random.choice(self.get_team().get_position_list(self.get_zone(self.goal_distance())))
            self.speed = s.PLAYER_SPEED
        else:
            self.ball_switch()  # Failure =, hand over ball.

    def shoot(self):
        """
        A method for shooting the ball at the goal.
        The odds of success are calculated based on:
            A. distance from the goal
            B. Attack stat of the shooting player.
        In addition, the opposing team has a chance to block, based on their defensive stats.
        Regardless, the enemy team is given the ball.
        """

        distance_modifier = max(0, (s.FIELD_LENGTH/2 - self.goal_distance()) / (s.FIELD_LENGTH/2))

        chance_success = max(5, self.ball_owner.stat_att * distance_modifier)
        self.ball_pos += self.goal_distance()/2 * self.get_team().get_dir(self.ball_pos)

        chance_catch = self.get_opposing_defense().stat_def
        shoot_roll = random.randint(1, 100)
        catch_roll = random.randint(1, 100)
        result = False

        if shoot_roll <= chance_success and chance_success - shoot_roll > chance_catch - catch_roll:
            self.scores[self.get_team()] += 1
            self.ball_pos = s.FIELD_LENGTH/2
            result = True
        self.ball_switch()
        return result

    def get_opposing_defense(self):
        """
        Helper method for getting a person to block a possible offense.
        :return: A Goalkeeper or Defending player.
        """
        for team in self.teams:
            if self.ball_owner not in team.field_team:
                defense_list = team.get_position_list("G")
                defense_list += team.get_position_list("D")
                return random.choice(defense_list)

    def out_of_bounds_check(self):
        """
        A method for determining if the ball is out of bounds.
        :return: True if the ball is out of bounds, False if it is not.
        """
        if 0 > self.ball_pos or self.ball_pos > s.FIELD_LENGTH:
            if self.ball_pos < 0:
                self.ball_pos = 0
            elif self.ball_pos > s.FIELD_LENGTH:
                self.ball_pos = s.FIELD_LENGTH
            self.ball_switch()
            return True
        return False
