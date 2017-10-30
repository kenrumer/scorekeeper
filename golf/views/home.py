from ..models import Tournament, TournamentRound, Round, Scorecard, FormatPlugin, Player, Course, CourseTee, Club, Activity, PlayerPlugin
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

def homeView(request):
    """
    View function for home page
    Sends the club name
    """
    retObject = getClub()
    return render(request, 'golf/home.html', retObject)
def getAllTournamentRounds(request):
    return JsonResponse(json.dumps(list(TournamentRound.objects.all().values()), cls=DjangoJSONEncoder))
def getAllCourseTees(request):
    return JsonResponse(json.dumps(list(CourseTee.objects.all().values('id', 'name', 'priority', 'default', 'slope', 'color', 'course__name', 'course__id').order_by('priority')), cls=DjangoJSONEncoder))
def getAllPlayerPlugins(request):
    return JsonResponse(json.dumps(list(PlayerPlugin.objects.all().values()), cls=DjangoJSONEncoder))
def getAllActivities(request):
    return JsonResponse(json.dumps(list(Activity.objects.all().values()), cls=DjangoJSONEncoder))

def getClub():
    retObject = {}
    retObject['club'] = json.dumps(Club.objects.order_by('-id').values('name', 'logo', 'default_tournament_name', 'players_last_updated')[0], cls=DjangoJSONEncoder)
    retObject['data'] = json.dumps(json.loads(json.loads(json.dumps(Club.objects.order_by('-id').values('data')[0], cls=DjangoJSONEncoder))['data']))
    return retObject

def checkForTournamentDuplicate(request):
    """
    Ajax function to check if the tournament already exists
    """
    tournamentName = request.POST.get('tournamentName')
    try:
        Tournament.objects.get(name=tournamentName)
        retObject = '{"duplicate": true}'
    except Tournament.MultipleObjectsReturned:
        retObject = '{"duplicate": true}'
    except Tournament.DoesNotExist:
        retObject = '{"duplicate": false}'
    return JsonResponse(json.loads(retObject))

def getAllFormatPlugins(request):
    return JsonResponse({'formatPlugins':list(FormatPlugin.objects.all().values().order_by('priority'))})

def getAllCourses(request):
    return JsonResponse({'courses':list(Course.objects.all().values().order_by('priority'))})

def getCourseTees(request):
    retObject = []
    courseJSON = json.loads(request.POST.get('courses'))
    for course in courseJSON:
        print (course)
        #print (courseJSON)
        courseId = course['id']
        for courseTee in list(CourseTee.objects.filter(course=courseId).values('id', 'name', 'priority', 'default', 'slope', 'color', 'course__name', 'course__id').order_by('priority')):
            retObject.append(courseTee);
    print (retObject)
    return JsonResponse({'courseTees':retObject})

def getAllTournaments(request):
    retObjects = []
    tournaments = Tournament.objects.order_by('-id').values()
    for tournament in tournaments:
        retObject = {}
        retObject['name'] = tournament['name']
        retObject['id'] = tournament['id']
        trs = TournamentRound.objects.filter(tournament=tournament['id'])
        for tr in trs:
            retObject['start_time'] = tr.scheduled_date
            retObject['finish_time'] = tr.scheduled_date
            scs = Scorecard.objects.filter(round__tournament_round=tr.id)
            for sc in scs:
                if sc.start_time.date() < tr.scheduled_date:
                    retObject['start_time'] = sc.start_time
                if sc.finish_time.date() > tr.scheduled_date:
                    retObject['finish_time'] = sc.finish_time
        retObjects.append(retObject)
                    
    return JsonResponse({'tournaments':retObjects})

def getAllPlayers(request):
    return JsonResponse({'players':list(Player.objects.all().values().order_by('priority'))})