from django.shortcuts import render
from . import forms
from backend import settings
from backend.main import Main

# Create your views here.


def home(request):
    # Set up forms
    form_english = forms.TeamSelection(team=settings.english_team)
    form_dutch = forms.TeamSelection(team=settings.dutch_team)
    errormsg = []
    # Received input
    if request.method == "POST":
        #Input is submitting players
        if request.POST.get("input"):
            form_english = forms.TeamSelection(settings.english_team, request.POST)
            form_dutch = forms.TeamSelection(settings.dutch_team, request.POST)
            #Check if forms are valid
            if form_dutch.is_valid() and form_english.is_valid():
                team_dict = {form_dutch: settings.dutch_team, form_english: settings.english_team}

                #Create a list of players for each team.
                for form in (form_dutch, form_english):
                    player_list = []
                    for option in form:
                        player_list += option.value()
                        #Check if the list of players contains only 1 Goalkeeper
                        if option.label == "Goalkeeper:" and len(option.value()) > 1:
                            errormsg.append("[ERROR]: Too many goalies!")
                    #Check if the list of players contains 11 players
                    if len(player_list) != 11:
                        errormsg.append('[ERROR]: Picked {} players (requires 11) for {}!'.format(len(player_list), form.team.name))
                    else:
                        team_dict[form].field_team.clear()
                        #Add all input to the field team
                        for player in player_list:
                            team_dict[form].field_team.append(team_dict[form].get_player(player))
            else:
                errormsg.append('[ERROR]: Did not pick at least one player on each position!')
        #Input is asking for random players
        elif request.POST.get("random"):
            settings.english_team.populate_team()
            settings.dutch_team.populate_team()

        #If request.POST.get("retry") = true, the following code also executes.
        if len(errormsg) == 0 and not request.POST.get("goback"):
            game = Main(settings.dutch_team, settings.english_team).play_match()
            return render(request, "matchup/match.html", {'game': game, 'final': game[-1]})

    return render(request, "matchup/setup.html", {'form_e': form_english,'form_d': form_dutch, 'error': errormsg})
