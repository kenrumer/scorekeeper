from ..models import Player, CourseTee, Club, Course, Hole, Tee, PlayerPlugin, FormatPlugin, RoundImportPlugin
from django.http import JsonResponse, FileResponse
import json
import zipfile
import os
import tempfile
from django.conf import settings
from django.core import serializers

def getClub():
    tempClub = serializers.serialize('json', [Club.objects.get(pk=1)])
    club = tempClub[1:-1]
    return club

def createFileResponse(context, name, archiveName, classModuleName, classModule, readme=None):
    """
    Helper function to limit the redundancy
    Make a temporary directory and a data subdirectory which we will add module and json
    TODO: Add README.txt file which explains the format and how the file can be used to import
    """
    retObject = {}
    with tempfile.TemporaryDirectory() as tmpdir:
        datadir = os.path.join(tmpdir, 'data')
        os.mkdir(datadir)
        with open(os.path.join(datadir, 'context.json'), 'w') as outfile:
            json.dump(context, outfile)
        if readme:
            with open(os.path.join(datadir, 'readme.txt'), 'w') as outfile:
                outfile.write(readme)
            with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
                datazip.write(os.path.join(datadir, 'readme.txt'), arcname='readme.txt')
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
            datazip.write(os.path.join(datadir, 'context.json'), arcname='context.json')
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'a') as datazip:
            datazip.write(classModule, arcname=classModuleName+'.py')
        retObject = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        retObject['Content-Disposition'] = ('attachment; filename="'+name+'.zip"')
    return retObject

def getTeesAndHoles(request):
    """
    View function for import export backup dialog in home page
    Sends the selected load player plugin in json format
    url: '/golf/getteesandholes/$'
    context:
        {
            courseId: id,
            courseTeeIds: '[ids]'
        }
    """
    courseId = request.POST['courseId']
    courseTeeIds = json.loads(request.POST['courseTeeIds'])
    resObject = {}
    resObject['tees'] = list(Tee.objects.filter(course_tee__id__in=courseTeeIds).values('id', 'yardage', 'par', 'handicap', 'course_tee', 'course_tee__name', 'hole', 'hole__number'))
    resObject['holes'] = json.loads(serializers.serialize('json', Hole.objects.filter(course=courseId)))
    return JsonResponse(resObject, safe=False)

def roundImportPlugin(request, roundImportPluginId):
    """
    View function for import export backup dialog in home page
    Sends the selected tournament format plugin in json format
    url: 'exportroundimportplugin/(?P<roundImportPluginId>\d+)$'
    """
    plugin = RoundImportPlugin.objects.get(pk=roundImportPluginId)
    tempModel = serializers.serialize('json', [plugin])
    context = json.loads(tempModel[1:-1])
    del context['pk']
    del context['model']
    del context['fields']['class_module']
    del context['fields']['class_module_name']
    del context['fields']['class_archive']
    del context['fields']['class_archive_name']
    del context['fields']['version']
    readme = 'The archive must include context.json and 1 python module\r\ncontext.json:\r\nbecause data is a free-form field, you cannot use single-quotes (\') and double-quotes must be escaped (\\")\r\n\tname: is unique to each plugin and if you upload a duplicate a new version will be created\r\n\tpriority: is used to sort the plugin list in club settings, -1 priority plugins are sorted only by name\r\n\tdata: is sent to your plugin when it is run\r\n\tclass_name: is the class within the module that will be used by Abstract Base Class\r\n\tdescription: helpful text for the users of the plugin'
    return createFileResponse(context, plugin.name, plugin.class_archive_name, plugin.class_module_name, os.path.join(settings.BASE_DIR, 'golf/media/'+plugin.class_module.name), readme)

def playerPlugin(request, playersPluginId):
    """
    View function for import export backup dialog in home page
    Sends the selected load player plugin in json format
    url: '/golf/exportplayerplugin/(?P<playersPluginId>\d+)$'
    """
    plugin = PlayerPlugin.objects.get(pk=playersPluginId)
    tempModel = serializers.serialize('json', [plugin])
    context = json.loads(tempModel[1:-1])
    del context['pk']
    del context['model']
    del context['fields']['class_module']
    del context['fields']['class_module_name']
    del context['fields']['class_archive']
    del context['fields']['class_archive_name']
    del context['fields']['version']
    readme = 'The archive must include context.json and 1 python module\r\ncontext.json:\r\nbecause data is a free-form field, you cannot use single-quotes (\') and double-quotes must be escaped (\\")\r\n\tname: is unique to each plugin and if you upload a duplicate a new version will be created\r\n\tpriority: is used to sort the plugin list in club settings, -1 priority plugins are sorted only by name\r\n\tdata: is sent to your plugin when it is run\r\n\tclass_name: is the class within the module that will be used by Abstract Base Class\r\n\tdescription: helpful text for the users of the plugin'
    return createFileResponse(context, plugin.name, plugin.class_archive_name, plugin.class_module_name, os.path.join(settings.BASE_DIR, 'golf/media/'+plugin.class_module.name), readme)

def formatPlugin(request, formatPluginId):
    """
    View function for import export backup dialog in home page
    Sends the selected format plugin in json format
    url: '/golf/exportformatplugin/(?P<formatPluginId>\d+)$'
    """
    plugin = FormatPlugin.objects.get(pk=formatPluginId)
    tempModel = serializers.serialize('json', [plugin])
    context = json.loads(tempModel[1:-1])
    del context['pk']
    del context['model']
    del context['fields']['class_module']
    del context['fields']['class_module_name']
    del context['fields']['class_archive']
    del context['fields']['class_archive_name']
    del context['fields']['version']
    readme = 'The archive must include context.json and 1 python module\r\ncontext.json:\r\nbecause data is a free-form field, you cannot use single-quotes (\') and double-quotes must be escaped (\\")\r\n\tname: is unique to each plugin and if you upload a duplicate a new version will be created\r\n\tpriority: is used to sort the plugin list in club settings, -1 priority plugins are sorted only by name\r\n\tdata: is sent to your plugin when it is run\r\n\tclass_name: is the class within the module that will be used by Abstract Base Class\r\n\tdescription: helpful text for the users of the plugin'
    return createFileResponse(context, plugin.name, plugin.class_archive_name, plugin.class_module_name, os.path.join(settings.BASE_DIR, 'golf/media/'+plugin.class_module.name), readme)

def database(request):
    """
    View function for import export backup dialog in home page
    Exports the database compressed in a zip file
    url: 'exportroundimportplugin/(?P<roundImportPluginId>\d+)$'
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(os.path.join(tmpdir, 'data.zip'), 'x') as datazip:
            datazip.write(settings.DATABASES['default']['NAME'], arcname='db.sqlite3')
        response = FileResponse(open(os.path.join(tmpdir, 'data.zip'), 'rb'))
        response['Content-Disposition'] = ('attachment; filename="db.sqlite3.zip"')
    return response