import random
from python.field import Field
from python import settings as s

#Start Game: Flip Coin. Losing Team shoots backwards
if random.randint(1, 2) == 1:
    play_field = Field(s.dutch_team, s.english_team)
else:
    play_field = Field(s.english_team, s.dutch_team)
timer = 1
shots = {s.dutch_team: 0, s.english_team: 0}
far_shots = {s.dutch_team: 0, s.english_team: 0}
on_targets = {s.dutch_team: 0, s.english_team: 0}
outs = 0



play_field.kick_off()
while timer < s.max_time:
    if timer == s.max_time/2:
        play_field.halftime()
        # print("HALFTIME!")
        play_field.kick_off()
        timer += 1

    timer += 1
    # print("Time: {}.".format(timer), play_field)

    out = play_field.out_check()
    pass_odds = 18
    if out:
        print("OUT!")
        outs += 1
        play_field.kick_off()
    elif play_field.speed < 0 or random.randint(1, 100) <= pass_odds:
        # print("PASS!")
        play_field.pass_ball()
    elif play_field.goal_distance() < 1600 and random.randint(1, 100) <= 20:
        # print("SHOOT!")
        shots[play_field.get_team()] += 1
        on_target = play_field.shoot()
        if on_target:
            on_targets[play_field.get_team()] += 1
    elif random.randint(1, 1000) <= 2:
        # print("FAR SHOOT!")
        far_shots[play_field.get_team()] += 1
        on_target = play_field.shoot()
        if on_target:
            on_targets[play_field.get_team()] += 1
    else:
        play_field.move_ball()

# print("---")
print("Match over. Final Scores: {}: {} - {}: {}.".format(
    s.dutch_team,
    play_field.scores[s.dutch_team],
    s.english_team,
    play_field.scores[s.english_team],))
# print("--")
# # print("Dutch Shots taken: {}".format(shots[s.dutch_team]))
# # print("Dutch Far shots: {}".format(far_shots[s.dutch_team]))
# print("Dutch Total shots: {}".format(shots[s.dutch_team]+far_shots[s.dutch_team]))
# print("Dutch On Target shots: {}".format(on_targets[s.english_team]))
# print("--")
# # print("English Shots taken: {}".format(shots[s.english_team]))
# # print("English Far shots: {}".format(far_shots[s.english_team]))
# print("English Total shots: {}".format(shots[s.english_team]+far_shots[s.english_team]))
# print("English On Target shots: {}".format(on_targets[s.dutch_team]))
# print("--\nOuts: {}".format(outs))
# dutch_score = 0
# dutch_att = 0
# dutch_def = 0
# english_score = 0
# english_att = 0
# english_def = 0
# for player in s.dutch_team.field_team:
#     dutch_score += player.stat_overall()
#     dutch_att += player.stat_att
#     dutch_def += player.stat_def
# for player in s.english_team.field_team:
#     english_score += player.stat_overall()
#     english_att += player.stat_att
#     english_def += player.stat_def
# print("Dutch average player strength:\t\t{}. Attack: {}. Defense: {}.".format(int(dutch_score/11),int(dutch_att/11),int(dutch_def/11)))
# print("English average player strength:\t{}. Attack: {}. Defense: {}.".format(int(english_score/11), int(english_att/11), int(english_def/11)))
