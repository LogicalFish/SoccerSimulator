import random
import settings as s

#Source: https://www.transfermarkt.nl/vitoria-guimaraes-sc/stadion/verein/2420

SPEED = 300

class Field:

    def __init__(self, team_start, team_other):
        self.teams = [team_start, team_other]
        self.teams[0].set_goal(0)
        self.teams[1].set_goal(s.FIELD_LENGTH)
        self.ball_pos = s.FIELD_LENGTH/2
        self.ball_owner = self.teams[0]
        self.scores = {self.teams[0]: 0, self.teams[1]: 0}
        self.speed = SPEED

    def __str__(self):
        result = "Current Ball Position = {}. Currently on Ball: {}. Score = {}-{}."
        result = result.format((self.ball_pos*100 / s.FIELD_LENGTH), self.ball_owner, self.scores[self.teams[0]],self.scores[self.teams[1]])
        return result

    def halftime(self):
        #Switch Goals
        self.ball_pos = s.FIELD_LENGTH/2

        self.teams[0].set_goal(s.FIELD_LENGTH)
        self.teams[1].set_goal(0)

        self.ball_owner = self.teams[1]

    def ball_switch(self):
        for team in self.teams:
            if team != self.ball_owner:
                self.ball_owner = team
                self.speed = SPEED
                return team

    def move_ball(self):
        movement = random.randint(self.speed - 40, min(self.speed + 25, 500))
        modifier = self.goal_distance()/s.FIELD_LENGTH
        self.ball_pos += movement * self.ball_owner.get_dir(self.ball_pos) * modifier
        self.speed = movement

    def kick_off(self):
        movement = 1000
        if self.ball_pos == 0:
            direction = 1
        elif self.ball_pos == s.FIELD_LENGTH:
            direction = -1
        elif self.ball_pos == s.FIELD_LENGTH/2:
            direction = self.ball_owner.get_dir(self.ball_pos)*-1
        self.ball_pos += movement * direction


    # Pass
    # Calculate odds of success based on team success.
    # Roll Dice
    # Move ball based on distance from goal. If failure, enemy team now has ball.
    def pass_ball(self):
        chance_success = 84 #Todo: change based on position
        #calculate movement
        zero_point = s.FIELD_LENGTH*.75 - self.ball_owner.goal_pos/2
        modifier = (self.ball_pos-zero_point) / (self.ball_owner.goal_pos-zero_point)

        movement = 1500*modifier
        direction = self.ball_owner.get_dir(self.ball_pos)
        self.ball_pos += movement * direction
        if random.randint(1, 100) <= chance_success:
            self.speed = SPEED
        else:
            self.ball_switch()  # Failure =, hand over ball.

    def goal_distance(self):
        if self.ball_owner.goal_pos == 0:
            return s.FIELD_LENGTH - self.ball_pos
        else:
            return self.ball_pos

    # Shoot
    # Calculate odds of success based on length
    # Roll dice
    # Move Ball ahead. If failure, enemy team now has ball.
    def shoot(self):

        distance_modifier = max(0, (s.FIELD_LENGTH/2 - self.goal_distance()) / (s.FIELD_LENGTH/2))

        print("MOD: {0} = ({1} - {2}) / {1}".format(distance_modifier, s.FIELD_LENGTH/2, self.goal_distance()))

        chance_success = max(5, 80 * distance_modifier)
        self.ball_pos += self.goal_distance()/2 * self.ball_owner.get_dir(self.ball_pos)

        chance_block = 75
        shoot_roll = random.randint(1, 100)
        block_roll = random.randint(1, 100)

        if shoot_roll <= chance_success and block_roll > chance_block:
            self.scores[self.ball_owner] += 1
            self.ball_switch()
            self.ball_pos = self.ball_owner.goal_pos
        else:
            self.ball_switch()

    def out_check(self):
        if 0 > self.ball_pos or self.ball_pos > s.FIELD_LENGTH:
            if self.ball_pos < 0:
                self.ball_pos = 0
            elif self.ball_pos > s.FIELD_LENGTH:
                self.ball_pos = s.FIELD_LENGTH
            self.ball_switch()
            return True
        return False
