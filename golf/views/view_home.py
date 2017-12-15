from ..models import Tournament, TournamentRound, Round, Scorecard, FormatPlugin, Player, Course, CourseTee, Hole, Tee, Club, Activity, PlayerPlugin, TournamentRoundImportPlugin
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

def getAllTournamentRounds(request):
    return JsonResponse(json.dumps(list(TournamentRound.objects.all().values()), cls=DjangoJSONEncoder))
def getAllCourseTees(request):
    return JsonResponse(json.dumps(list(CourseTee.objects.all().values('id', 'name', 'priority', 'default', 'slope', 'color', 'course__name', 'course__id').order_by('priority')), cls=DjangoJSONEncoder))
def getAllPlayerPlugins(request):
    return JsonResponse(json.dumps(list(PlayerPlugin.objects.all().values()), cls=DjangoJSONEncoder))

def homeView(request):
    """
    View function for home page
    Sends the club name
    """
    resObject = {}
    resObject['club'] = serializers.serialize('json', Club.objects.all().order_by('-id'))
    resObject['courseTees'] = serializers.serialize('json', CourseTee.objects.all().order_by('-default', 'priority'))
    resObject['courses'] = serializers.serialize('json', Course.objects.all().order_by('priority'))
    return render(request, 'golf/home.html', resObject)

def checkForTournamentDuplicate(request):
    """
    Ajax function to check if the tournament already exists
    """
    tournamentName = request.POST.get('tournamentName')
    try:
        Tournament.objects.get(name=tournamentName)
        resStr = '{"duplicate": true}'
    except Tournament.MultipleObjectsReturned:
        resStr = '{"duplicate": true}'
    except Tournament.DoesNotExist:
        resStr = '{"duplicate": false}'
    return JsonResponse(json.loads(resStr), safe=False)

def getAllFormatPlugins(request):
    """
    Ajax function to return all formatPlugins for this club
    """
    resStr = serializers.serialize('json', FormatPlugin.objects.all().order_by('priority'))
    return JsonResponse(json.loads(resStr), safe=False)

def getAllCourses(request):
    """
    Ajax function to return all courses for this club
    """
    resStr = serializers.serialize("json", Course.objects.all().order_by('priority'))
    return JsonResponse(json.loads(resStr), safe=False)

def getCourseTees(request):
    """
    Ajax function to return all course tees for the requested courses
    """
    courses = json.loads(request.POST.get('courses'))
    courseIds = []
    for course in courses:
        courseIds.append(course['pk'])
    resStr = serializers.serialize('json', CourseTee.objects.filter(course__id__in=courseIds).order_by('priority'))
    return JsonResponse(json.loads(resStr), safe=False)

def getAllTournaments(request):
    resObject = {}
    t = Tournament.objects.all().order_by('-id')
    resObject['tournaments'] = json.loads(serializers.serialize('json', t))
    resObject['tournamentRounds'] = json.loads(serializers.serialize('json', TournamentRound.objects.filter(tournament__in=t)))
    return JsonResponse(resObject)

def getAllPlayers(request):
    """
    Ajax function to return all players
    """
    resStr = serializers.serialize('json', Player.objects.all().order_by('priority', 'name'))
    return JsonResponse(json.loads(resStr), safe=False)
    
def getAllRecentActivities(request):
    """
    Ajax function to return all activities
    """
    resStr = serializers.serialize('json', Activity.objects.all().order_by('id'))
    return JsonResponse(json.loads(resStr), safe=False)

def getImportExportBackupData(request):
    import os
    size = os.path.getsize('/home/ubuntu/workspace/db.sqlite3')
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1
        size = size/1024.0
    databaseSize = "%.*f%s" % (2, size, suffixes[suffixIndex])
    
    retObject = {}
    retObject['courses'] = list(Course.objects.all().values('id', 'name').order_by('priority'))
    retObject['playerPlugins'] = list(PlayerPlugin.objects.all().values('id', 'name'))
    retObject['formatPlugins'] = list(FormatPlugin.objects.all().values('id', 'name'))
    retObject['tournamentRoundImportPlugins'] = list(TournamentRoundImportPlugin.objects.all().values('id', 'name'))
    retObject['databaseSize'] = databaseSize
    return JsonResponse({'importExportBackupData':retObject})