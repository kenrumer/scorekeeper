from django.http import HttpResponse, JsonResponse
from ..models import Player, Club, PlayerPlugin
import importlib

def editPlayers(request):
    return HttpResponse('Test')

def getPlayers(request):
    """
    Getter function for list of players
    """
    resultList = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    return JsonResponse({'data' : resultList})

def newPlayer(request):
    return HttpResponse('Test')

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
    resultList = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    return JsonResponse({'data' : resultList})

def addRoundToPlayer(request):
    return HttpResponse('Test')