from ..models import Tournament, TournamentDate, FormatPlugin, Player, Course, CourseTee, Club, Activity, PlayerPlugin
from django.shortcuts import render

def index(request):
    """
    View function for home page
    """
    clubs = list(Club.objects.values('id', 'name', 'logo', 'default_tournament_name', 'player_plugin__name', 'players_last_updated', 'data'))
    playerPlugins = list(PlayerPlugin.objects.values('id', 'name', 'class_package', 'class_name'))
    courses = list(Course.objects.values('id', 'name', 'priority', 'default'))
    courseTees = list(CourseTee.objects.values('id', 'name', 'priority', 'default', 'slope', 'course', 'course__name', 'color'))
    tournamentDates = list(TournamentDate.objects.values('id', 'date', 'tournament__id', 'tournament__name'))
    tournaments = list(Tournament.objects.values('id', 'name'))
    formats = list(FormatPlugin.objects.values('id', 'name', 'priority'))
    players = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    activities = list(Activity.objects.values('id', 'date', 'title', 'notes'))
    context = {
        'clubs': clubs,
        'playerplugins': playerPlugins,
        'courses': courses,
        'courseTees': courseTees,
        'tournamentDates': tournamentDates,
        'formats': formats,
        'tournaments': tournaments,
        'players': players,
        'activities': activities
    }
    return render(request, 'golf/index.html', context=context)