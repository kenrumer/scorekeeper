from ..models import Tournament, TournamentDate, FormatPlugin, Player, Course, CourseTee, Club, Activity, PlayerPlugin
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def homeView(request):
    """
    View function for home page
    """
    clubs = list(Club.objects.all().values('id', 'name', 'logo', 'default_tournament_name', 'player_plugin__name', 'players_last_updated', 'data'))
    clubsJSON = json.dumps(clubs, cls=DjangoJSONEncoder)
    playerPlugins = list(PlayerPlugin.objects.all().values('id', 'name', 'class_package', 'class_name'))
    playerPluginsJSON = json.dumps(playerPlugins, cls=DjangoJSONEncoder)
    courses = list(Course.objects.all().values('id', 'name', 'priority', 'default').order_by('priority'))
    coursesJSON = json.dumps(courses, cls=DjangoJSONEncoder)
    courseTees = list(CourseTee.objects.all().values('id', 'name', 'priority', 'default', 'slope', 'course', 'course__name', 'color').order_by('priority'))
    courseTeesJSON = json.dumps(courseTees, cls=DjangoJSONEncoder)
    tournamentDates = list(TournamentDate.objects.all().values('id', 'date', 'tournament__id', 'tournament__name'))
    tournamentDatesJSON = json.dumps(tournamentDates, cls=DjangoJSONEncoder)
    tournaments = list(Tournament.objects.all().values('id', 'name'))
    tournamentsJSON = json.dumps(tournaments, cls=DjangoJSONEncoder)
    formats = list(FormatPlugin.objects.all().values('id', 'name', 'priority').order_by('priority'))
    formatsJSON = json.dumps(formats, cls=DjangoJSONEncoder)
    players = list(Player.objects.all().values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)
    activities = list(Activity.objects.all().values('id', 'date', 'title', 'notes'))
    activitiesJSON = json.dumps(activities, cls=DjangoJSONEncoder)
    context = {
        'clubs': clubs,
        'playerplugins': playerPlugins,
        'courseTees': courseTees,
        'courses': courses,
        'tournamentDates': tournamentDates,
        'formats': formats,
        'tournaments': tournaments,
        'players': players,
        'activities': activities,
    }
    if (len(clubs) == 0):
        context['clubsJSON'] = {}
    else:
        context['clubsJSON'] = clubsJSON
    if (len(playerPlugins) == 0):
        context['playerPluginsJSON'] = {}
    else:
        context['playerPluginsJSON'] = playerPluginsJSON
    if (len(courses) == 0):
        context['coursesJSON'] = {}
    else:
        context['coursesJSON'] = coursesJSON
    if (len(courseTees) == 0):
        context['courseTeesJSON'] = {}
    else:
        context['courseTeesJSON'] = courseTeesJSON
    if (len(tournamentDates) == 0):
        context['tournamentDatesJSON'] = {}
    else:
        context['tournamentDatesJSON'] = tournamentDatesJSON
    if (len(formats) == 0):
        context['formatsJSON'] = {}
    else:
        context['formatsJSON'] = formatsJSON
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