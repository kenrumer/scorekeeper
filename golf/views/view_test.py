from django.template.loader import get_template
from django.template import Context
from django.core import serializers
from ..models import Player, CourseTee, Club, Course, Hole, Tee, PlayerPlugin, FormatPlugin, TournamentRoundImportPlugin
from django.http import HttpResponse, JsonResponse, FileResponse
import json
import zipfile
from django.shortcuts import render


def test(request):
    retObject = {}
    return render(request, 'golf/test.html', retObject)

def testView(request):
    """
    Trying to find the best way to serialize data
    """
    #club = Club.objects.order_by('-id').values('name', 'logo', 'default_tournament_name', 'players_last_updated')[0]
    data = serializers.serialize("json", Club.objects.all().order_by('-id'), fields=('name', 'logo', 'default_tournament_name', 'players_last_updated', 'data'))
    #data = serializers.serialize("json", CourseTee.objects.all().order_by('-default', 'priority'), fields=('id', 'name', 'priority', 'default', 'slope', 'color', 'course__name', 'course__id'))
    print(data)
    return JsonResponse(data, safe=False)