import random
from backend.field import Field
from backend import settings as s


#Start of the game: Flip a coin to decide which team starts.

class Main:

    def __init__(self, team1, team2):
        self.play_field = None
        self.timer = 0
        self.kickoff = True
        self.team1 = team1
        self.team2 = team2

    def create_field(self):
        if random.randint(1, 2) == 1:
            play_field = Field(self.team1, self.team2)
        else:
            play_field = Field(self.team2, self.team1)
        self.play_field = play_field
        return play_field

    def play_match(self):
        # Start the game
        self.create_field()

        game_progress = []

        ##Main Loop
        while self.timer < s.max_time:
            game_progress.append(self.step())
            self.timer += 1

        # Return final match.
        return game_progress
        # print("Match over. Final {}".format(self.get_results()))

    def step(self):
        if self.timer < s.max_time:
            # Check for Halftime
            if self.timer == s.max_time / 2:
                self.play_field.halftime()
                self.play_field.kick_off()
            else:
                out = self.play_field.out_of_bounds_check()
                if out or self.kickoff:
                    # The ball has been kicked off the field
                    self.play_field.kick_off()
                    self.kickoff = False
                elif self.play_field.speed < 0 or random.randint(1, 100) <= s.PASS_ODDS:
                    # The ball will be passed.
                    self.play_field.pass_ball()
                elif self.play_field.goal_distance() < 1600 and random.randint(1, 100) <= s.SHOOT_CLOSE_ODDS:
                    # The ball is close to the goal, and it should be shot at the goal.
                    self.kickoff = self.play_field.shoot()
                elif random.randint(1, 1000) <= s.SHOOT_FAR_ODDS:
                    # The ball is far from the goal, but it could still be shot at the goal.
                    self.kickoff = self.play_field.shoot()
                else:
                    # Player moves with the ball.
                    self.play_field.move_ball()
            return self.play_field.get_status()

#
# m = Main(s.english_team, s.dutch_team)
# game = m.play_match()
# for g in game:
#     print("Ball at: {}, Owner: {} from {}, Score: {}: {} - {}: {}".format(int(g['ball']), g['owner'], g['owner-team'],
#                                                                           g['team1'], g['score1'],
#                                                                           g['team2'], g['score2']))
