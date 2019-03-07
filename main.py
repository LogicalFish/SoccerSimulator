import random
from field import Field
import settings as s


#TODO RUN method
#Start Game: Flip Coin. Losing Team shoots backwards
random.randint(1, 2)
play_field = Field(s.dutch_team, s.english_team)
#Get Random Number between 1 and 2.
timer = 1
shots = {s.dutch_team: 0, s.english_team: 0}
far_shots = {s.dutch_team: 0, s.english_team: 0}
outs = 0

play_field.kick_off()
while timer < s.max_time:
    if timer == s.max_time/2:
        play_field.halftime()
        print("HALFTIME!")
        play_field.kick_off()
        timer += 1

    timer += 1
    print("Time: {}.".format(timer), play_field)

    out = play_field.out_check()
    pass_odds = 18
    if out:
        print("OUT!")
        outs+=1
        play_field.kick_off()
    elif play_field.speed < 0 or random.randint(1,100) <= pass_odds:
        print("PASS!")
        play_field.pass_ball()
    elif play_field.goal_distance() < 1600 and random.randint(1, 100) <= 60:
        print("TEST: {}".format(play_field.goal_distance()))
        print("SHOOT!")
        shots[play_field.ball_owner] += 1
        play_field.shoot()
    elif random.randint(1, 1000) <= 2:
        print("FAR SHOOT!")
        far_shots[play_field.ball_owner] += 1
        play_field.shoot()
    else:
        play_field.move_ball()


print("Match over.")
print("--\nDutch Shots taken: {}".format(shots[s.dutch_team]))
print("Dutch Far shots: {}".format(far_shots[s.dutch_team]))
print("Dutch Total shots: {}".format(shots[s.dutch_team]+far_shots[s.dutch_team]))
print("--\nEnglish Shots taken: {}".format(shots[s.english_team]))
print("English Far shots: {}".format(far_shots[s.english_team]))
print("English Total shots: {}".format(shots[s.english_team]+far_shots[s.english_team]))
print("--\nOuts: {}".format(outs))
