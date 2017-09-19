from django.http import HttpResponse, JsonResponse
from ..models import Player, Club
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
    A lot of research... Get the Module(file) get the class (getattr), instansiate the class () call the function
    """
    clubs = list(Club.objects.values('id', 'name', 'logo', 'player_plugin__class_package', 'player_plugin__class_name', 'data'))
    for club in clubs:
        classModule = importlib.import_module('golf.playerplugins.'+club['player_plugin__class_package'])
        classAccess = getattr(classModule, club['player_plugin__class_name'])
        classInst = classAccess()
        classInst.loadPlayers(club['data'])
    resultList = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    return JsonResponse({'data' : resultList})

def addRoundToPlayer(request):
    return HttpResponse('Test')