from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Course, CourseTee, Tee, Hole

def editCourses(request):
    """
    View function for editting the list of courses
    """
    return render_to_response('golf/editcourses.html')

def getCourses(request):
    """
    Getter function for list of courses
    """
    result_list = list(Course.objects.values('id', 'default', 'priority', 'name'))
    return JsonResponse({'data' : result_list})

def updateCourse(request, courseId):
    """
    Setter function for existing course
    """
    if (request.POST['default'] == 'true'):
        c = Course(id=courseId, default=True, priority=request.POST['priority'], name=request.POST['name'])
        c.save()
    else:
        c = Course(id=courseId, default=False, priority=request.POST['priority'], name=request.POST['name'])
        c.save()
    return JsonResponse({'data' : [{'id':c.id, 'default':c.default, 'priority':c.priority, 'name':c.name}]})

def createCourse(request):
    """
    Create function for course
    """
    if (request.POST['default'] == 'true'):
        c = Course(default=True, priority=request.POST['priority'], name=request.POST['name'])
        c.save()
    else:
        c = Course(default=False, priority=request.POST['priority'], name=request.POST['name'])
        c.save()
    return JsonResponse({'data' : [{'id':c.id, 'default':c.default, 'priority':c.priority, 'name':c.name}]})

def removeCourse(request, courseId):
    """
    Delete function for course
    """
    Course.objects.filter(id=courseId).delete()
    return HttpResponse('OK')

def editCourseTees(request, courseId):
    """
    View function for editting the list of course holes and tees
    """
    courseTees = list(CourseTee.objects.filter(course_id=courseId).values('id', 'default', 'priority', 'name', 'slope', 'color'))
    context = {
        'courseId': courseId,
        'courseTees': courseTees
    }
    return render(request, 'golf/editcoursetees.html', context=context)

def getCourseTees(request, courseId):
    """
    Getter function for list of courses and tees
    """
    resultList = list(CourseTee.objects.filter(course_id=courseId).values('id', 'default', 'priority', 'name', 'course_id'))
    return JsonResponse({'data' : resultList})

def updateCourseTee(request, courseId, courseTeeId):
    """
    Setter function for existing course tee
    """
    if (request.POST['default'] == 'true'):
        ct = CourseTee(id=courseTeeId, default=True, priority=request.POST['priority'], name=request.POST['name'], slope=request.POST['slope'], color=request.POST['color'], course_id=courseId)
        ct.save()
    else:
        ct = CourseTee(id=courseTeeId, default=False, priority=request.POST['priority'], name=request.POST['name'], slope=request.POST['slope'], color=request.POST['color'], course_id=courseId)
        ct.save()
    return JsonResponse({'data' : [{'id':ct.id, 'default':ct.default, 'priority':ct.priority, 'name':ct.name, 'slope':ct.slope, 'color':ct.color, 'course_id':ct.course_id}]})

def createCourseTee(request, courseId):
    """
    Create function for course tee
    """
    if (request.POST['default'] == 'true'):
        ct = CourseTee(default=True, priority=request.POST['priority'], name=request.POST['name'], slope=request.POST['slope'], color=request.POST['color'], course_id=courseId)
        ct.save()
    else:
        ct = CourseTee(default=False, priority=request.POST['priority'], name=request.POST['name'], slope=request.POST['slope'], color=request.POST['color'], course_id=courseId)
        ct.save()
    return JsonResponse({'data' : [{'id':ct.id, 'default':ct.default, 'priority':ct.priority, 'name':ct.name, 'slope':ct.slope, 'color':ct.color, 'course_id':ct.course_id}]})

def removeCourseTee(request, courseTeeId):
    """
    Delete function for course tee
    """
    CourseTee.objects.filter(id=courseTeeId).delete()
    return HttpResponse('OK')

def editCourseTeeHoles(request, courseId, courseTeeId):
    """
    View function for editting the list of courses
    """
    return render(request, 'golf/editcourseteeholes.html', context={'course_id': courseId, 'course_tee_id': courseTeeId, })

def getCourseTeeHoles(request, courseId, courseTeeId):
    """
    Getter function for list of courses and tees
    """
    resultList = list(Tee.objects.filter(course_tee_id=courseTeeId).values('id', 'yardage', 'par', 'handicap', 'hole__id', 'hole__name', 'hole__number'))
    return JsonResponse({'data' : resultList})

def updateCourseTeeHole(request, courseId, courseTeeId, teeId):
    """
    Setter function for existing course tee hole
    """
    try:
        h = Hole.objects.get(number=request.POST['number'], name=request.POST['name'], course_id=courseId)
    except Hole.DoesNotExist:
        h = Hole(number=request.POST['number'], name=request.POST['name'], course_id=courseId)
        h.save()
    t = Tee(id=teeId, hole_id=h.id, course_tee_id=courseTeeId, yardage=request.POST['yardage'], par=request.POST['par'], handicap=request.POST['handicap'])
    t.save()
    return JsonResponse({'data' : [{'id':t.id, 'yardage':t.yardage, 'par':t.par, 'handicap':t.handicap, 'name':t.hole.name, 'number':t.hole.number}]})

def createCourseTeeHole(request, courseId, courseTeeId):
    """
    Create function for course tee hole
    """
    try:
        h = Hole.objects.get(number=request.POST['number'], course_id=courseId)
    except Hole.DoesNotExist:
        h = Hole(number=request.POST['number'], name=request.POST['name'], course_id=courseId)
        h.save()
    t = Tee(hole_id=h.id, course_tee_id=courseTeeId, yardage=request.POST['yardage'], par=request.POST['par'], handicap=request.POST['handicap'])
    t.save()
    return JsonResponse({'data' : [{'id':t.id, 'yardage':t.yardage, 'par':t.par, 'handicap':t.handicap, 'name':t.hole.name, 'number':t.hole.number}]})

def removeCourseTeeHole(request, teeId):
    """
    Delete function for course tee
    """
    Tee.objects.filter(id=teeId).delete()
    return HttpResponse('OK')
