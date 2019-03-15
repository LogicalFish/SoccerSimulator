from django import forms

pos_dict = {"G": "Goalkeeper","D": "Defender", "M": "Midfielder", "A": "Attacker"}


class TeamSelection(forms.Form):

    def __init__(self, team, *args, **kwargs):
        self.team = team
        super(TeamSelection, self).__init__(*args, **kwargs)

        for position in pos_dict.keys():
            player_list = team.get_position_list(position, False)
            name_list = []
            for player in player_list:
                name_list.append((player.name, player.name))
            identifier = position + "-" + team.name
            self.fields[identifier] = forms.CharField(label="{}:".format(pos_dict[position]), widget=forms.CheckboxSelectMultiple(choices=name_list))

