import random
from python import settings as s

#Source: https://www.transfermarkt.nl/vitoria-guimaraes-sc/stadion/verein/2420

SPEED = 300

class Field:

    def __init__(self, team_start, team_other):
        self.teams = [team_start, team_other]
        self.teams[0].set_goal(0)
        self.teams[1].set_goal(s.FIELD_LENGTH)
        self.ball_pos = s.FIELD_LENGTH/2
        self.ball_owner = random.choice(self.teams[0].get_position_list("A"))
        self.scores = {self.teams[0]: 0, self.teams[1]: 0}
        self.speed = SPEED

    def __str__(self):
        result = "Current Ball Position = {}. Currently on Ball: {}. Score = {}-{}."
        result = result.format((self.ball_pos*100 / s.FIELD_LENGTH), self.ball_owner, self.scores[self.teams[0]],self.scores[self.teams[1]])
        return result

    def get_team(self):
        for team in self.teams:
            if self.ball_owner in team.field_team:
                return team
        raise ValueError

    def halftime(self):
        #Switch Goals
        self.ball_pos = s.FIELD_LENGTH/2

        self.teams[0].set_goal(s.FIELD_LENGTH)
        self.teams[1].set_goal(0)

        self.ball_owner = random.choice(self.teams[1].get_position_list("A"))

    def ball_switch(self):
        for team in self.teams:
            if self.ball_owner not in team.field_team:
                self.ball_owner = random.choice(team.get_position_list(self.get_zone(s.FIELD_LENGTH - self.goal_distance())))
                self.speed = SPEED
                return team

    def goal_distance(self):
        if self.get_team().goal_pos == 0:
            return s.FIELD_LENGTH - self.ball_pos
        else:
            return self.ball_pos

    @staticmethod
    def get_zone(goal_distance):
        if s.FIELD_LENGTH > goal_distance > s.FIELD_LENGTH * (2 / 3):
            return "D"
        elif s.FIELD_LENGTH * (2/3) > goal_distance > s.FIELD_LENGTH / 3:
            return "M"
        elif s.FIELD_LENGTH / 3 > goal_distance > 0:
            return "A"
        else:
            return "?"

    def move_ball(self):
        movement = random.randint(self.speed - 40, min(self.speed + 25, 500))
        modifier = self.goal_distance()/s.FIELD_LENGTH
        self.ball_pos += movement * self.get_team().get_dir(self.ball_pos) * modifier
        self.speed = movement

    def kick_off(self):
        movement = 1000
        if self.ball_pos == 0:
            direction = 1
        elif self.ball_pos == s.FIELD_LENGTH:
            direction = -1
        elif self.ball_pos == s.FIELD_LENGTH/2:
            direction = self.get_team().get_dir(self.ball_pos)*-1
        self.ball_pos += movement * direction

    # Pass
    # Calculate odds of success based on team success.
    # Roll Dice
    # Move ball based on distance from goal. If failure, enemy team now has ball.
    def pass_ball(self):
        chance_success = self.ball_owner.stat_overall()
        #calculate movement
        zero_point = s.FIELD_LENGTH*.75 - self.get_team().goal_pos/2
        modifier = (self.ball_pos-zero_point) / (self.get_team().goal_pos-zero_point)

        movement = 1500*modifier
        direction = self.get_team().get_dir(self.ball_pos)
        self.ball_pos += movement * direction
        if random.randint(1, 100) <= chance_success:
            self.ball_owner = random.choice(self.get_team().get_position_list(self.get_zone(self.goal_distance())))
            self.speed = SPEED
        else:
            self.ball_switch()  # Failure =, hand over ball.

    # Shoot
    # Calculate odds of success based on length
    # Roll dice
    # Move Ball ahead. If failure, enemy team now has ball.
    def shoot(self):

        distance_modifier = max(0, (s.FIELD_LENGTH/2 - self.goal_distance()) / (s.FIELD_LENGTH/2))

        chance_success = max(5, self.ball_owner.stat_att * distance_modifier)
        self.ball_pos += self.goal_distance()/2 * self.get_team().get_dir(self.ball_pos)

        chance_catch = self.get_opposing_defense().stat_def
        shoot_roll = random.randint(1, 100)
        catch_roll = random.randint(1, 100)

        if shoot_roll <= chance_success and chance_success - shoot_roll > chance_catch - catch_roll:
            self.scores[self.get_team()] += 1
            self.ball_pos = s.FIELD_LENGTH/2
        self.ball_switch()

        if shoot_roll <= chance_success:
            return True
        return False

    def get_opposing_defense(self):
        for team in self.teams:
            if self.ball_owner not in team.field_team:
                defense_list = team.get_position_list("G")
                defense_list += team.get_position_list("D")
                return random.choice(defense_list)

    def out_check(self):
        if 0 > self.ball_pos or self.ball_pos > s.FIELD_LENGTH:
            if self.ball_pos < 0:
                self.ball_pos = 0
            elif self.ball_pos > s.FIELD_LENGTH:
                self.ball_pos = s.FIELD_LENGTH
            self.ball_switch()
            return True
        return False
