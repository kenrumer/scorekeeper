from ..models import Player, CourseTee, Club, Course, Hole, Tee, PlayerPlugin, FormatPlugin, RoundImportPlugin
from django.http import JsonResponse
import json
import zipfile
import os
import tempfile
from django.conf import settings
from django.core import serializers

def courses(request):
    """
    Update function to import courses from uploaded json file
    TODO: json validation, try catch
    url: '/golf/importcourses/'
    """
    resObject = {}
    for f in request.FILES:
        if (request.FILES[f].size < 10000):
            reqFile = request.FILES[f].read().decode('utf-8')
            reqObject = json.loads(reqFile)
            for course in serializers.deserialize('json', json.dumps([reqObject['course']])):
                course.save()
            for hole in serializers.deserialize('json', json.dumps(reqObject['holes'])):
                hole.save()
            for courseTee in serializers.deserialize('json', json.dumps(reqObject['courseTees'])):
                courseTee.save()
            for tee in reqObject['tees']:
                ct = CourseTee.objects.get(name=tee['course_tee__name'], course__name=reqObject['course']['fields']['name'])
                h = Hole.objects.get(number=tee['hole__number'], course__name=reqObject['course']['fields']['name'])
                t = Tee.objects.get_or_create(course_tee=ct, hole=h, yardage=tee['yardage'], handicap=tee['handicap'], par=tee['par'])

    return JsonResponse({'data':'success'})
    
def importRoundImportPlugins(request):
    """
    Update function to import tournament round import plugins from uploaded zip files
    Need to extract each file, then import context file, then save the class file and the archive file
    Always creates a new row in the database, if new plugin, will have a version of 1 otherwize will increment by 1
    TODO: json and class validation, try catch
    url: '/golf/importroundimportplugins/'
    """
    resList = []
    for f in request.FILES:
        thisObject = {}
        thisObject['filename'] = request.FILES[f].name
        if (request.FILES[f].size < 1000000):
            uploadedFileData = os.path.splitext(request.FILES[f].name)
            if uploadedFileData[1] != '.zip':
                thisObject['error'] = 'file does not have .zip extension'
                thisObject['status'] = 'failed'
            else:
                with zipfile.ZipFile(request.FILES[f]) as datazip:
                    class_module_name = ''
                    for filename in datazip.namelist():
                        filenameData = os.path.splitext(filename)
                        pyFilecount = 0
                        if filenameData[1] == '.py':
                            pyFilecount = pyFilecount + 1
                            class_module_name = filenameData[0]
                    if pyFilecount != 1:
                        thisObject['error'] = 'Must include exactly 1 python module'
                        thisObject['status'] = 'failed'
                    else:
                        reqFile = '['+datazip.read('context.json').decode('utf-8')+']'
                        reqJson = json.loads(reqFile)
                        reqJson[0]['model'] = 'golf.playerplugin'
                        reqJson[0]['pk'] = None
                        reqJson[0]['fields']['class_module_name'] = class_module_name
                        reqJson[0]['fields']['class_archive_name'] = request.FILES[f].name
                        for model in serializers.deserialize('json', json.dumps(reqJson)):
                            model.object.class_archive = request.FILES[f]
                            model.object.class_module.save(class_module_name+'.py', datazip.open(class_module_name+'.py'))
                            plugin = RoundImportPlugin.objects.filter(name=model.object.name).order_by('-version')
                            if len(plugin) > 0:
                                # This plugin exists, need to create a new version
                                model.object.version = plugin[0].version + 1
                            else:
                                # This is a new plugin, set the version to 1
                                model.object.version = 1
                            model.save()
                            thisObject['version'] = model.object.version
                            thisObject['pk'] = model.object.pk
                            thisObject['class_module_filename'] = model.object.class_module.name
                            thisObject['class_archive_filename'] = model.object.class_archive.name
                            thisObject['name'] = model.object.name
                            thisObject['description'] = model.object.description
                            thisObject['class_archive_name'] = model.object.class_archive_name
                            thisObject['class_module_name'] = model.object.class_module_name
                            thisObject['class_name'] = model.object.class_name
                            thisObject['priority'] = model.object.priority
                            thisObject['data'] = model.object.data
                            thisObject['status'] = 'success'
        resList.append(thisObject)
    return JsonResponse(resList, safe=False)

def playerPlugins(request):
    """
    Update function to import player plugins from uploaded zip files
    Need to extract each file, then import context file, then save the class file and the archive file
    Always creates a new row in the database, if new plugin, will have a version of 1 otherwize will increment by 1
    TODO: json and class validation, try catch
    url: '/golf/importplayerplugins/'
    """
    resList = []
    for f in request.FILES:
        thisObject = {}
        thisObject['filename'] = request.FILES[f].name
        if (request.FILES[f].size < 1000000):
            uploadedFileData = os.path.splitext(request.FILES[f].name)
            if uploadedFileData[1] != '.zip':
                thisObject['error'] = 'file does not have .zip extension'
                thisObject['status'] = 'failed'
            else:
                with zipfile.ZipFile(request.FILES[f]) as datazip:
                    class_module_name = ''
                    for filename in datazip.namelist():
                        filenameData = os.path.splitext(filename)
                        pyFilecount = 0
                        if filenameData[1] == '.py':
                            pyFilecount = pyFilecount + 1
                            class_module_name = filenameData[0]
                    if pyFilecount != 1:
                        thisObject['error'] = 'Must include exactly 1 python module'
                        thisObject['status'] = 'failed'
                    else:
                        reqFile = '['+datazip.read('context.json').decode('utf-8')+']'
                        reqJson = json.loads(reqFile)
                        reqJson[0]['model'] = 'golf.playerplugin'
                        reqJson[0]['pk'] = None
                        reqJson[0]['fields']['class_module_name'] = class_module_name
                        reqJson[0]['fields']['class_archive_name'] = request.FILES[f].name
                        for model in serializers.deserialize('json', json.dumps(reqJson)):
                            model.object.class_archive = request.FILES[f]
                            model.object.class_module.save(class_module_name+'.py', datazip.open(class_module_name+'.py'))
                            plugin = PlayerPlugin.objects.filter(name=model.object.name).order_by('-version')
                            if len(plugin) > 0:
                                # This plugin exists, need to create a new version
                                model.object.version = plugin[0].version + 1
                            else:
                                # This is a new plugin, set the version to 1
                                model.object.version = 1
                            model.save()
                            thisObject['version'] = model.object.version
                            thisObject['pk'] = model.object.pk
                            thisObject['class_module_filename'] = model.object.class_module.name
                            thisObject['class_archive_filename'] = model.object.class_archive.name
                            thisObject['name'] = model.object.name
                            thisObject['description'] = model.object.description
                            thisObject['class_archive_name'] = model.object.class_archive_name
                            thisObject['class_module_name'] = model.object.class_module_name
                            thisObject['class_name'] = model.object.class_name
                            thisObject['priority'] = model.object.priority
                            thisObject['data'] = model.object.data
                            thisObject['status'] = 'success'
        resList.append(thisObject)
    return JsonResponse(resList, safe=False)

def formatPlugins(request):
    """
    Update function to import format plugins from uploaded zip files
    Need to extract each file, then import context file, then save the class file and the archive file
    Always creates a new row in the database, if new plugin, will have a version of 1 otherwize will increment by 1
    TODO: json and class validation, try catch
    url: '/golf/importformatplugins/'
    """
    resList = []
    for f in request.FILES:
        thisObject = {}
        thisObject['filename'] = request.FILES[f].name
        if (request.FILES[f].size < 1000000):
            uploadedFileData = os.path.splitext(request.FILES[f].name)
            if uploadedFileData[1] != '.zip':
                thisObject['error'] = 'file does not have .zip extension'
                thisObject['status'] = 'failed'
            else:
                with zipfile.ZipFile(request.FILES[f]) as datazip:
                    class_module_name = ''
                    for filename in datazip.namelist():
                        filenameData = os.path.splitext(filename)
                        pyFilecount = 0
                        if filenameData[1] == '.py':
                            pyFilecount = pyFilecount + 1
                            class_module_name = filenameData[0]
                    if pyFilecount != 1:
                        thisObject['error'] = 'Must include exactly 1 python module'
                        thisObject['status'] = 'failed'
                    else:
                        reqFile = '['+datazip.read('context.json').decode('utf-8')+']'
                        reqJson = json.loads(reqFile)
                        reqJson[0]['model'] = 'golf.formatplugin'
                        reqJson[0]['pk'] = None
                        reqJson[0]['fields']['class_module_name'] = class_module_name
                        reqJson[0]['fields']['class_archive_name'] = request.FILES[f].name
                        for model in serializers.deserialize('json', json.dumps(reqJson)):
                            model.object.class_archive = request.FILES[f]
                            model.object.class_module.save(class_module_name+'.py', datazip.open(class_module_name+'.py'))
                            plugin = FormatPlugin.objects.filter(name=model.object.name).order_by('-version')
                            if len(plugin) > 0:
                                # This plugin exists, need to create a new version
                                model.object.version = plugin[0].version + 1
                            else:
                                # This is a new plugin, set the version to 1
                                model.object.version = 1
                            model.save()
                            thisObject['version'] = model.object.version
                            thisObject['pk'] = model.object.pk
                            thisObject['class_module_filename'] = model.object.class_module.name
                            thisObject['class_archive_filename'] = model.object.class_archive.name
                            thisObject['name'] = model.object.name
                            thisObject['description'] = model.object.description
                            thisObject['class_archive_name'] = model.object.class_archive_name
                            thisObject['class_module_name'] = model.object.class_module_name
                            thisObject['class_name'] = model.object.class_name
                            thisObject['priority'] = model.object.priority
                            thisObject['data'] = model.object.data
                            thisObject['status'] = 'success'
        resList.append(thisObject)
    return JsonResponse(resList, safe=False)