from ..models import Tournament, TournamentRound, Round, Scorecard, FormatPlugin, Player, Course, CourseTee, Hole, Tee, Club, Activity, PlayerPlugin, RoundImportPlugin
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.conf import settings
import importlib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def directorView(request):
    """
    View function for director home page
    Sends the club, the name and logo are used in the banner
    Sends the courses and courseTees for the printouts button
    url: '/golf/'
    """
    resObject = {}
    tempClub = serializers.serialize('json', [Club.objects.get(pk=1)])
    resObject['club'] = tempClub[1:-1]
    resObject['courseTees'] = serializers.serialize('json', CourseTee.objects.all().order_by('-default', 'priority'))
    resObject['courses'] = serializers.serialize('json', Course.objects.all().order_by('priority'))
    return render(request, 'golf/director.html', resObject)

def getAllFormatPlugins(request):
    """
    Ajax function to return all formatPlugins for this club
    url: '/golf/getallformatplugins/'
    """
    resStr = serializers.serialize('json', FormatPlugin.objects.all().order_by('priority'))
    return JsonResponse(json.loads(resStr), safe=False)

def checkForTournamentDuplicate(request):
    """
    Ajax function to check if the tournament already exists
    url: '/golf/checkfortournamentduplicate/'
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

def getAllTournaments(request):
    """
    Ajax function to return all tournaments for this club
    retuns all tournament rounds that are associated with a tournament
    TODO: This logic is bad as the number of tournaments grows.  Need to build in some kind of pagination
    url: '/golf/getalltournaments/'
    """
    resObject = {}
    t = Tournament.objects.all().order_by('-id')
    resObject['tournaments'] = json.loads(serializers.serialize('json', t))
    resObject['tournamentRounds'] = json.loads(serializers.serialize('json', TournamentRound.objects.filter(tournament__in=t)))
    return JsonResponse(resObject)

def loadPlayers(request):
    """
    Getter function for list of players from ghin, this calls a plugin from club PlayerPlugin
    Get the Module(file) get the class (getattr), instansiate the class () call the function
    url: /golf/loadplayers/
    """
    plugin = PlayerPlugin.objects.get(club__id=1)
    classModule = importlib.import_module('golf.media.'+plugin.class_module.name.replace('/', '.').replace('.py', ''))
    classAccess = getattr(classModule, plugin.class_name)
    classInst = classAccess()
    classInst.loadPlayers(plugin.data)
    return getAllPlayers(request)

def getAllPlayers(request):
    """
    Ajax function to return all players
    url: '/golf/getallplayers/'
    """
    resStr = serializers.serialize('json', Player.objects.all().order_by('priority', 'name'))
    return JsonResponse(json.loads(resStr), safe=False)
    
def getAllRecentActivities(request):
    """
    Ajax function to return all activities
    url: '/golf/getallrecentactivities/'
    """
    resStr = serializers.serialize('json', Activity.objects.all().order_by('id'))
    return JsonResponse(json.loads(resStr), safe=False)

def getImportExportBackupData(request):
    """
    Ajax function to return all import export backup data
    Gets the size of the database and pretty prints it
    url: '/golf/getimportexportbackupdata/'
    """
    import os
    size = os.path.getsize('/home/ubuntu/workspace/db.sqlite3')
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1
        size = size/1024.0
    databaseSize = "%.*f%s" % (2, size, suffixes[suffixIndex])
    
    resObject = {}
    resObject['playerPlugins'] = json.loads(serializers.serialize('json', PlayerPlugin.objects.all().order_by('priority')))
    resObject['formatPlugins'] = json.loads(serializers.serialize('json', FormatPlugin.objects.all().order_by('priority')))
    resObject['roundImportPlugins'] = json.loads(serializers.serialize('json', RoundImportPlugin.objects.all().order_by('priority')))
    resObject['database'] = json.loads('{"databaseSize": "'+databaseSize+'"}')
    return JsonResponse(resObject)