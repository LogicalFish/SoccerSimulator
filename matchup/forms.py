from django import forms


class TeamSelection(forms.Form):

    # error_css_class = "alert alert-danger"

    def __init__(self, team, *args, **kwargs):
        self.team = team
        super(TeamSelection, self).__init__(*args, **kwargs)

        self.create_position_form(team)

    def create_position_form(self, team):
        player_list = team.sort_team_by_position()

        for position in player_list.keys():
            name_list = []
            for player in player_list[position]:
                name_list.append((player.name, player.name))
            identifier = position + "-" + team.name
            self.fields[identifier] = forms.MultipleChoiceField(label="{}:".format(position), widget=forms.CheckboxSelectMultiple, choices=name_list)

    def clean(self):
        cleaned_data = super().clean()
        name_list = []
        for option in cleaned_data.keys():
            name_list += cleaned_data.get(option)
        player_list = self.team.get_players_by_name(name_list)
        sorted_list = self.team.sort_team_by_position(player_list)

        errormsg = ""
        if len(player_list) != 11:
            errormsg += "Team must have 11 players.\n"
        if "Goalkeeper" in sorted_list.keys() and len(sorted_list["Goalkeeper"]) > 1:
            errormsg += "Team must have only 1 Goalkeeper.\n"
        if errormsg:
            raise forms.ValidationError(errormsg)

