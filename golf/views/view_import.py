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

def courses(request):
    """
    View function for import
    Sends the selected course, tees and holes in json format
    """
    retObject = {}
    for f in request.FILES:
        if (request.FILES[f].size < 10000):
            req = request.FILES[f].read().decode('utf-8')
            reqObject = json.loads(req)
            retObject['name'] = reqObject['course']['name']
            try:
                # Not a new course
                c = Course.objects.get(name=reqObject['course']['name'])
                retObject['addCourse'] = False
            except Course.DoesNotExist:
                # New course will deal with the addition of course here
                retObject['addCourse'] = True
                c = Course(name=reqObject['course']['name'], default=reqObject['course']['default'], priority=reqObject['course']['priority'])
                c.save()
                hole_ids = {}
                for hole in reqObject['course']['holes']:
                    h = Hole(course_id=c.id, number=hole['number'], name=hole['name'])
                    h.save()
                    hole_ids[hole['number']] = h.id
                for courseTee in reqObject['course']['courseTees']:
                    ct = CourseTee(course_id=c.id, slope=courseTee['slope'], priority=courseTee['priority'], color=courseTee['color'], default=courseTee['default'], name=courseTee['name'])
                    ct.save()
                    for tee in courseTee['tees']:
                        t = Tee(coursetee_id=ct['id'], hole_id=hole_ids[tee['hole__number']], yardage=tee['yardage'], par=tee['par'], handicap=tee['handicap'])
                        t.save()
                print(retObject)
                return JsonResponse({'data':retObject})
            if retObject['addCourse'] == False:
                # Course isn't new, have to check holes, course tees, tees
                # Checking holes, for now we are not adding or removing, only change, assuming all courses will be 18 holes
                retObject['changedHoles'] = []
                retObject['addedHoles'] = []
                retObject['deletedHoles'] = []
                retObject['changedCourseTees'] = []
                retObject['addedCourseTees'] = []
                retObject['deletedCourseTees'] = []
                retObject['changedTees'] = []
                retObject['addedTees'] = []
                retObject['deletedTees'] = []
                for hole in reqObject['course']['holes']:
                    try:
                        h = Hole.objects.filter(course_id=c.id, number=hole['number']).values('id', 'number', 'name')
                        if len(h) == 0:
                            # no hole of this number on this course, create it
                            h = Hole(course_id=c.id, number=hole['number'], name=hole['name'])
                            h.save()
                            obj = {}
                            obj['id'] = h.id
                            obj['number'] = hole['number']
                            obj['name'] = hole['name']
                            retObject['addedHoles'] = obj
                        else:
                            # hole exists, check what has changed
                            # The hole exists, now need to find out which are different (name)
                            h = Hole.objects.get(id=h[0]['id'])
                            if h.name != hole['name']:
                                h.name = hole['name']
                                h.save()
                                obj = {}
                                obj['id'] = h.id
                                obj['oldName'] = h.name
                                obj['newName'] = hole['name']
                                retObject['changedHoles'].append(obj)
                    except Hole.DoesNotExist:
                        pass
                try:
                    # Check for holes that need to be removed
                    hs = Hole.objects.filter(course_id=c.id).order_by('number').values('id', 'number', 'name')
                    for h in hs:
                        found = False
                        for reqHole in reqObject['course']['holes']:
                            if reqHole['number'] == h['number']:
                                found = True
                        if not found:
                            # Remove this hole
                            obj = {}
                            obj['id'] = h['id']
                            obj['number'] = h['number']
                            obj['name'] = h['name']
                            retObject['deletedHoles'] = obj
                            hdel = Hole.objects.get(id=h['id'])
                            hdel.delete()
                except Hole.DoesNotExist:
                    # There are no holes for this course and none were just added (odd)
                    pass
                # Work on course tees, could be adding, removing, or replacing there could be 100, but they are unique by course and name (makes name a tag field for the user)
                for reqCourseTee in reqObject['course']['courseTees']:
                    try:
                        ct = CourseTee.objects.filter(course_id=c.id, name=reqCourseTee['name']).values('id', 'priority', 'default', 'slope', 'color', 'name')
                        if len(ct) == 0:
                            # This is a new course tee, plz add to db
                            ct = CourseTee(course_id=c.id, name=reqCourseTee['name'], priority=reqCourseTee['priority'], default=reqCourseTee['default'], slope=reqCourseTee['slope'], color=reqCourseTee['color'])
                            ct.save()
                            obj = {}
                            obj['id'] = ct.id
                            obj['name'] = reqCourseTee['name']
                            obj['priority'] = reqCourseTee['priority']
                            obj['default'] = reqCourseTee['default']
                            obj['slope'] = reqCourseTee['slope']
                            obj['color'] = reqCourseTee['color']
                            retObject['addedCourseTees'].append(obj)
                        else:
                            # Course tee exists, check what has changed
                            # The course tee exists, now need to find out which are different (priority, default, rating, slope, color and name)
                            ct = CourseTee.objects.get(id=ct[0]['id'])
                            if ct.priority != reqCourseTee['priority']:
                                ct.priority = reqCourseTee['priority']
                                ct.save()
                                obj = {}
                                obj['id'] = ct.id
                                obj['oldPriority'] = ct.priority
                                obj['newPriority'] = reqCourseTee['priority']
                                retObject['changedCourseTees'].append(obj)
                            if ct.default != reqCourseTee['default']:
                                ct.default = reqCourseTee['default']
                                ct.save()
                                obj = {}
                                obj['id'] = ct.id
                                obj['oldDefault'] = ct.default
                                obj['newDefault'] = reqCourseTee['default']
                                retObject['changedCourseTees'].append(obj)
                            if ct.slope != reqCourseTee['slope']:
                                ct.slope = reqCourseTee['slope']
                                ct.save()
                                obj = {}
                                obj['id'] = ct.id
                                obj['oldSlope'] = ct.slope
                                obj['newSlope'] = reqCourseTee['slope']
                                retObject['changedCourseTees'].append(obj)
                            if ct.color != reqCourseTee['color']:
                                ct.color = reqCourseTee['color']
                                ct.save()
                                obj = {}
                                obj['id'] = ct.id
                                obj['oldColor'] = ct.color
                                obj['newColor'] = reqCourseTee['color']
                                retObject['changedCourseTees'].append(obj)
                    except CourseTee.DoesNotExist:
                        pass
                try:
                    # Check for course tees that need to be removed
                    cts = CourseTee.objects.filter(course_id=c.id).values('id', 'name', 'priority', 'default', 'slope', 'color')
                    for ct in cts:
                        found = False
                        for reqCourseTee in reqObject['course']['courseTees']:
                            if reqCourseTee['name'] == ct['name']:
                                found = True
                        if not found:
                            # Remove this course tee
                            obj = {}
                            obj['id'] = ct['id']
                            obj['name'] = ct['name']
                            obj['priority'] = ct['priority']
                            obj['default'] = ct['default']
                            obj['slope'] = ct['slope']
                            obj['color'] = ct['color']
                            retObject['deletedCourseTees'] = obj
                            ctdel = CourseTee.objects.get(id=ct['id'])
                            ctdel.delete()
                except CourseTee.DoesNotExist:
                    # There are no course tee for this course and none were just added (odd)
                    pass
                
                # Work on tees, could be adding, removing, or replacing there could be 100, but they are unique by course, course tee, hole number (makes name a tag field for the user)
                for reqCourseTee in reqObject['course']['courseTees']:
                    for reqTee in reqCourseTee['tees']:
                        try:
                            t = Tee.objects.filter(course_tee__course_id=c.id, course_tee__name=reqCourseTee['name'], hole__number=reqTee['hole__number']).values('id', 'yardage', 'handicap', 'hole__number', 'par')
                            if len(t) == 0:
                                # This is a new course tee, plz add to db
                                ct = CourseTee.objects.get(course_id=c.id, name=reqCourseTee['name'])
                                h = Hole.objects.get(course_id=c.id, number=reqTee['hole__number'])
                                t = Tee(course_tee=ct, hole=h, yardage=reqTee['yardage'], handicap=reqTee['handicap'], par=reqTee['par'])
                                t.save()
                                obj = {}
                                obj['id'] = t.id
                                obj['courseTeeName'] = reqCourseTee['name']
                                obj['holeNumber'] = reqTee['hole__number']
                                obj['yardage'] = reqTee['yardage']
                                obj['handicap'] = reqTee['handicap']
                                obj['par'] = reqTee['par']
                                retObject['addedTees'].append(obj)
                            else:
                            # Tee exists, check what has changed
                                # The tee exists, now need to find out which are different ()
                                t = Tee.objects.get(id=t[0]['id'])
                                if t.yardage != reqTee['yardage']:
                                    t.yardage = reqTee['yardage']
                                    t.save()
                                    obj = {}
                                    obj['id'] = t.id
                                    obj['oldYardage'] = t.yardage
                                    obj['newYardage'] = reqTee['yardage']
                                    retObject['changedTees'].append(obj)
                                if t.handicap != reqTee['handicap']:
                                    t.handicap = reqTee['handicap']
                                    t.save()
                                    obj = {}
                                    obj['id'] = t.id
                                    obj['oldHandicap'] = t.handicap
                                    obj['newHandicap'] = reqTee['handicap']
                                    retObject['changedTees'].append(obj)
                                if t.hole.number != reqTee['hole__number']:
                                    t.hole.number = reqTee['hole__number']
                                    t.save()
                                    obj = {}
                                    obj['id'] = t.id
                                    obj['oldHoleNumber'] = t.hole__number
                                    obj['newHoleNumber'] = reqTee['hole__number']
                                    retObject['changedTees'].append(obj)
                                if t.par != reqTee['par']:
                                    t.par = reqTee['par']
                                    t.save()
                                    obj = {}
                                    obj['id'] = t.id
                                    obj['oldPar'] = t.par
                                    obj['newPar'] = reqTee['par']
                                    retObject['changedTees'].append(obj)
                        except Tee.DoesNotExist:
                            pass
                try:
                    # Check for tees that need to be removed
                    ts = Tee.objects.filter(course_tee__course_id=c.id).values('id', 'yardage', 'handicap', 'hole__number', 'par')
                    for t in ts:
                        found = False
                        for reqCourseTee in reqObject['course']['courseTees']:
                            for reqTee in reqCourseTee['tees']:
                                if reqTee['hole__number'] == t['hole__number']:
                                    found = True
                        if not found:
                            # Remove this tee
                            obj = {}
                            obj['id'] = t['id']
                            obj['yardage'] = t['yardage']
                            obj['handicap'] = t['handicap']
                            obj['holeNumber'] = t['hole__number']
                            obj['par'] = t['par']
                            retObject['deletedCourseTees'] = obj
                            tdel = Tee.objects.get(id=t['id'])
                            tdel.delete()
                except CourseTee.DoesNotExist:
                    # There are no course tee for this course and none were just added (odd)
                    pass
    return JsonResponse({'data':retObject})