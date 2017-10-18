from ..models import Tournament, TournamentRound, TournamentFormatPlugin, Player, Course, CourseTee, Club, Activity, PlayerPlugin
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def homeView(request):
    """
    View function for home page
    Basically sending the database for clubs, courses, tees, tournament rounds, tournaments, tournament formats, players, player plugins, activities
    """
    clubs = list(Club.objects.all().values())
    clubsJSON = json.dumps(clubs, cls=DjangoJSONEncoder)
    courses = list(Course.objects.all().values().order_by('priority'))
    coursesJSON = json.dumps(courses, cls=DjangoJSONEncoder)
    courseTees = list(CourseTee.objects.all().values().order_by('priority'))
    courseTeesJSON = json.dumps(courseTees, cls=DjangoJSONEncoder)
    tournaments = list(Tournament.objects.all().values())
    tournamentsJSON = json.dumps(tournaments, cls=DjangoJSONEncoder)
    tournamentRounds = list(TournamentRound.objects.all().values())
    tournamentRoundsJSON = json.dumps(tournamentRounds, cls=DjangoJSONEncoder)
    tournamentFormats = list(TournamentFormatPlugin.objects.all().values().order_by('priority'))
    tournamentFormatsJSON = json.dumps(tournamentFormats, cls=DjangoJSONEncoder)
    players = list(Player.objects.all().values())
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)
    playerPlugins = list(PlayerPlugin.objects.all().values())
    playerPluginsJSON = json.dumps(playerPlugins, cls=DjangoJSONEncoder)
    activities = list(Activity.objects.all().values())
    activitiesJSON = json.dumps(activities, cls=DjangoJSONEncoder)
    context = {
        'clubs': clubs,
        'courseTees': courseTees,
        'courses': courses,
        'tournaments': tournaments,
        'tournamentRounds': tournamentRounds,
        'tournamentFormats': tournamentFormats,
        'players': players,
        'playerplugins': playerPlugins,
        'activities': activities,
    }
    #Used in settings and new tournament
    if (len(clubs) == 0):
        context['clubsJSON'] = {}
    else:
        context['clubsJSON'] = clubsJSON

    #Used in load players and edit players
    if (len(playerPlugins) == 0):
        context['playerPluginsJSON'] = {}
    else:
        context['playerPluginsJSON'] = playerPluginsJSON

    #Used in new tournament
    if (len(courses) == 0):
        context['coursesJSON'] = {}
    else:
        context['coursesJSON'] = coursesJSON

    #Used in new tournament
    if (len(courseTees) == 0):
        context['courseTeesJSON'] = {}
    else:
        context['courseTeesJSON'] = courseTeesJSON

    if (len(tournamentRounds) == 0):
        context['tournamentRoundsJSON'] = {}
    else:
        context['tournamentRoundsJSON'] = tournamentRoundsJSON

    if (len(tournamentFormats) == 0):
        context['tournamentFormatsJSON'] = {}
    else:
        context['tournamentFormatsJSON'] = tournamentFormatsJSON

    if (len(tournaments) == 0):
        context['tournamentsJSON'] = {}
    else:
        context['tournamentsJSON'] = tournamentsJSON

    if (len(players) == 0):
        context['playersJSON'] = {}
    else:
        context['playersJSON'] = playersJSON

    if (len(activities) == 0):
        context['activitiesJSON'] = {}
    else:
        context['activitiesJSON'] = activitiesJSON
    return render(request, 'golf/home.html', context=context)