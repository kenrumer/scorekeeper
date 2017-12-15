from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template import Context
from ..models import Player, CourseTee, Club, Course, Hole, Tee, PlayerPlugin, FormatPlugin, TournamentRoundImportPlugin
from django.http import HttpResponse, JsonResponse, FileResponse
import json
from django.forms.models import model_to_dict
import zipfile
import os
import tempfile
from django.conf import settings

def getClub():
    retObject = {}
    retObject['club'] = json.dumps(Club.objects.order_by('-id').values('name', 'logo', 'default_tournament_name', 'players_last_updated')[0], cls=DjangoJSONEncoder)
    retObject['data'] = json.dumps(json.loads(json.loads(json.dumps(Club.objects.order_by('-id').values('data')[0], cls=DjangoJSONEncoder))['data']))
    return retObject

def courses(request, courseId):
    """
    View function for home page
    Sends the selected course, tees and holes in json format
    """
    retObject = {}
    c = Course.objects.get(id=courseId)
    retObject['priority'] = c.priority
    retObject['default'] = c.default
    retObject['name'] = c.name
    retObject['holes'] = {}
    retObject['holes'] = list(Hole.objects.filter(course_id=courseId).order_by('number').values('number', 'name'))
    cts = CourseTee.objects.filter(course_id=courseId).values('id', 'priority', 'default', 'slope', 'color', 'name')
    retObject['courseTees'] = []
    i = 0
    for ct in cts:
        tempObject = {}
        tempObject['priority'] = ct['priority']
        tempObject['default'] = ct['default']
        tempObject['slope'] = ct['slope']
        tempObject['color'] = ct['color']
        tempObject['name'] = ct['name']
        tempObject['tees'] = {}
        tempObject['tees'] = list(Tee.objects.filter(course_tee_id=ct['id']).order_by('hole__number').values('handicap', 'par', 'yardage', 'hole__number'))
        retObject['courseTees'].append(tempObject)
    return JsonResponse({'course':retObject})

def loadPlayersPlugin(request, loadPlayersPluginId):
    """
    View function for home page
    Sends the selected load player plugin in json format
    """
    # Get the json data for the playerPlugin
    retObject = {}
    pp = PlayerPlugin.objects.get(id=loadPlayersPluginId)
    retObject['name'] = pp.name
    retObject['description'] = pp.description
    retObject['version'] = pp.version
    retObject['class_module'] = pp.class_module
    retObject['class_name'] = pp.class_name
    retObject['priority'] = pp.priority
    retObject['data'] = pp.data
    
    # make a temporary directory and a data subdirectory which we will add module and json
    with tempfile.TemporaryDirectory() as tmpdir:
        datadir = os.path.join(tmpdir, 'data')
        os.mkdir(datadir)
        with open(os.path.join(datadir, 'context.json'), 'w') as outfile:
            json.dump(retObject, outfile)
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'x') as datazip:
            datazip.write(os.path.join(datadir, 'context.json'), arcname='context.json')
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
            datazip.write(os.path.join(settings.BASE_DIR, 'golf/playerplugins/'+pp.class_module+'.py'), arcname=pp.class_module+'.py')
        response = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        response['Content-Disposition'] = ('attachment; filename="'+pp.name+'.zip"')
    return response

def tournamentFormatPlugin(request, tournamentFormatPluginId):
    """
    View function for home page
    Sends the selected tournament format plugin in json format
    """
    # Get the json data for the formatPlugin
    retObject = {}
    fp = FormatPlugin.objects.get(id=tournamentFormatPluginId)
    retObject['name'] = fp.name
    retObject['description'] = fp.description
    retObject['version'] = fp.version
    retObject['class_module'] = fp.class_module
    retObject['class_name'] = fp.class_name
    retObject['priority'] = fp.priority
    retObject['data'] = fp.data
    
    # make a temporary directory and a data subdirectory which we will add module and json
    with tempfile.TemporaryDirectory() as tmpdir:
        datadir = os.path.join(tmpdir, 'data')
        os.mkdir(datadir)
        with open(os.path.join(datadir, 'context.json'), 'w') as outfile:
            json.dump(retObject, outfile)
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'x') as datazip:
            datazip.write(os.path.join(datadir, 'context.json'), arcname='context.json')
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
            datazip.write(os.path.join(settings.BASE_DIR, 'golf/formatplugins/'+fp.class_module+'.py'), arcname=fp.class_module+'.py')
        response = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        response['Content-Disposition'] = ('attachment; filename="'+fp.name+'.zip"')
    return response

def tournamentRoundImportPlugin(request, TournamentRoundImportPluginId):
    """
    View function for home page
    Sends the selected tournament round import plugin in json format
    """
    # Get the json data for the formatPlugin
    retObject = {}
    trip = TournamentRoundImportPlugin.objects.get(id=TournamentRoundImportPluginId)
    retObject['name'] = trip.name
    retObject['description'] = trip.description
    retObject['version'] = trip.version
    retObject['class_module'] = trip.class_module
    retObject['class_name'] = trip.class_name
    retObject['priority'] = trip.priority
    retObject['data'] = trip.data
    
    # make a temporary directory and a data subdirectory which we will add module and json
    with tempfile.TemporaryDirectory() as tmpdir:
        datadir = os.path.join(tmpdir, 'data')
        os.mkdir(datadir)
        with open(os.path.join(datadir, 'context.json'), 'w') as outfile:
            json.dump(retObject, outfile)
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'x') as datazip:
            datazip.write(os.path.join(datadir, 'context.json'), arcname='context.json')
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
            datazip.write(os.path.join(settings.BASE_DIR, 'golf/formatplugins/'+trip.class_module+'.py'), arcname=trip.class_module+'.py')
        response = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        response['Content-Disposition'] = ('attachment; filename="'+trip.name+'.zip"')
    return response

def database(request):
    # make a temporary directory and a data subdirectory which we will add module and json
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'x') as datazip:
            datazip.write('/home/ubuntu/workspace/db.sqlite3', arcname='db.sqlite3')
        response = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        response['Content-Disposition'] = ('attachment; filename="db.sqlite3.zip"')
    return response