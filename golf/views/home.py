from ..models import Tournament, TournamentDate, FormatPlugin, Player, Course, CourseTee, Club, Activity, PlayerPlugin
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    """
    View function for home page
    """
    clubs = list(Club.objects.values('id', 'name', 'logo', 'default_tournament_name', 'player_plugin__name', 'players_last_updated', 'data'))
    clubsJSON = json.dumps(clubs, cls=DjangoJSONEncoder)
    playerPlugins = list(PlayerPlugin.objects.all().values('id', 'name', 'class_package', 'class_name'))
    playerPluginsJSON = json.dumps(playerPlugins, cls=DjangoJSONEncoder)
    courses = list(Course.objects.values('id', 'name', 'priority', 'default'))
    coursesJSON = json.dumps(courses, cls=DjangoJSONEncoder)
    courseTees = list(CourseTee.objects.values('id', 'name', 'priority', 'default', 'slope', 'course', 'course__name', 'color'))
    courseTeesJSON = json.dumps(courseTees, cls=DjangoJSONEncoder)
    tournamentDates = list(TournamentDate.objects.values('id', 'date', 'tournament__id', 'tournament__name'))
    tournamentDatesJSON = json.dumps(tournamentDates, cls=DjangoJSONEncoder)
    tournaments = list(Tournament.objects.values('id', 'name'))
    tournamentsJSON = json.dumps(tournaments, cls=DjangoJSONEncoder)
    formats = list(FormatPlugin.objects.values('id', 'name', 'priority'))
    formatsJSON = json.dumps(formats, cls=DjangoJSONEncoder)
    players = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)
    activities = list(Activity.objects.values('id', 'date', 'title', 'notes'))
    activitiesJSON = json.dumps(activities, cls=DjangoJSONEncoder)
    context = {
        'clubs': clubs,
        'clubsJSON': clubsJSON,
        'playerplugins': playerPlugins,
        'playerpluginsJSON': playerPluginsJSON,
        'courses': courses,
        'coursesJSON': coursesJSON,
        'courseTees': courseTees,
        'courseTeesJSON': courseTeesJSON,
        'tournamentDates': tournamentDates,
        'tournamentDatesJSON': tournamentDatesJSON,
        'formats': formats,
        'formatsJSON': formatsJSON,
        'tournaments': tournaments,
        'tournamentsJSON': tournamentsJSON,
        'players': players,
        'playersJSON': playersJSON,
        'activities': activities,
        'activitiesJSON': activitiesJSON
    }
    print(context)
    return render(request, 'golf/index.html', context=context)