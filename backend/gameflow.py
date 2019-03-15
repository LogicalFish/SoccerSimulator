import random
from backend.field import Field
from backend import settings as s


class GameFlow:

    def __init__(self, team1, team2):
        self.play_field = None
        self.timer = 0
        self.kickoff = True
        self.team1 = team1
        self.team2 = team2

    def create_field(self):
        """
        Readies the field. Initializes the playing field based on a coinflip to see who starts where.
        :return: the readied field object.
        """
        if random.randint(1, 2) == 1:
            play_field = Field(self.team1, self.team2)
        else:
            play_field = Field(self.team2, self.team1)
        self.play_field = play_field
        return play_field

    def step(self):
        """
        Method for determining what happens during a single 'step' of a match.
        :return: The current state of the field after this step. See field > get_status
        """
        if self.timer < s.MAX_TIME:
            # Check for Halftime
            if self.timer == s.MAX_TIME / 2:
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
                elif self.play_field.goal_distance() < s.SHOOT_DISTANCE and random.randint(1, 100) < s.SHOOT_CLOSE_ODDS:
                    # The ball is close to the goal, and it should be shot at the goal.
                    self.kickoff = self.play_field.shoot()
                elif random.randint(1, 1000) <= s.SHOOT_FAR_ODDS:
                    # The ball is far from the goal, but it could still be shot at the goal.
                    self.kickoff = self.play_field.shoot()
                else:
                    # Player moves with the ball.
                    self.play_field.move_ball()
            return self.play_field.get_status()

    def play_match(self):
        """
        Main Method for playing the match. Plays the match, step by step, and returns a list
        containing the game state after each step.
        :return: A list of the game states after each step.
        """
        # Start the game
        self.create_field()

        game_progress = []

        # MAIN LOOP
        while self.timer < s.MAX_TIME:
            game_progress.append(self.step())
            self.timer += s.STEP_SIZE

        # Return final match.
        return game_progress

    @staticmethod
    def compose_highlights(game_progress):
        """
        Method for finding the highlights of a match
        :param game_progress: The step-by-step state of the game.
        :return: A list of all the goals scored in the match, including time and scoring player.
        """
        highlight_list = []
        previous_step = None
        for i, step in enumerate(game_progress):
            if previous_step:
                for score in ("score1", "score2"):
                    if previous_step[score] < step[score]:
                        status = {'type': "GOAL!",
                                  'team': previous_step['owner-team'],
                                  'player': previous_step['owner'],
                                  'time': int((i-s.STEP_SIZE) / (60/s.STEP_SIZE))}
                        highlight_list.append(status)

            if 0 > step['ball'] or step['ball'] > s.FIELD_LENGTH:
                status = {'type': "OUT!",
                          'team': step['owner-team'],
                          'player': step['owner'],
                          'time': int((i - s.STEP_SIZE) / (60 / s.STEP_SIZE))}
                highlight_list.append(status)

            previous_step = step
        return highlight_list
