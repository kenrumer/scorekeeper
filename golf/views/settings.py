from ..models import Club

def storeSettings(request):
    """
    Update function for club settings
    """
    c = Club(id=request.POST['id'], name=request.POST['name'], logo=request.POST['logo'], default_tournament_name=request.POST['default_tournament_name'], player_plugin__name=request.POST['player_plugin__name'], players_last_updated=request.POST['players_last_updated'], data=request.POST['data'])
    c.save()