from django.shortcuts import render
from . import forms
from backend import settings
from backend.gameflow import GameFlow

# Create your views here.


def home(request):
    # Set up forms
    form_english = forms.TeamSelection(team=settings.english_team)
    form_dutch = forms.TeamSelection(team=settings.dutch_team)
    error = False

    # Received input
    if request.method == "POST":
        #Input is submitting players
        if request.POST.get("input"):
            form_english = forms.TeamSelection(settings.english_team, request.POST)
            form_dutch = forms.TeamSelection(settings.dutch_team, request.POST)
            team_dict = {form_dutch: settings.dutch_team, form_english: settings.english_team}

            #Create a list of players for each team.
            for form in (form_dutch, form_english):
                if form.is_valid():
                    #Add all input to the field team
                    player_list = []
                    for option in form.cleaned_data.keys():
                        player_list += form.cleaned_data.get(option)
                    team_dict[form].create_field_team(player_list)
                else:
                    error = True

        #Input is asking for random players
        elif request.POST.get("random"):
            settings.english_team.populate_team()
            settings.dutch_team.populate_team()

        #If request.POST.get("retry") = true, the following code also executes.
        if not error and not request.POST.get("goback"):
            game = GameFlow(settings.dutch_team, settings.english_team).play_match()
            return render(request, "matchup/match.html", {'game': game, 'final': game[-1], 'highlights': GameFlow.compose_highlights(game)})

    return render(request, "matchup/setup.html", {'form_e': form_english,'form_d': form_dutch })
