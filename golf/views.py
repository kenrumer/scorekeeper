import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Tournament, TournamentDate, Format, Player, Round, Score, Course, CourseTee, Tee, Hole, Club, Activity, PlayerPlugin
from django.forms.models import model_to_dict
import importlib

def docs(request):
    """
    View function for documentation
    """
    return render(request, 'golf/documentation.html', {})

def docscodestyle(request):
    """
    View function for code style documentation
    """
    return render(request, 'golf/docscodestyle.html', {})

def docsinstall(request):
    """
    View function for software installation documentation
    """
    return render(request, 'golf/docsinstall.html', {})

def docseditting(request):
    """
    View function for source code editting documentation
    """
    return render(request, 'golf/docseditting.html', {})

def index(request):
    """
    View function for home page
    """
    clubs = list(Club.objects.values('id', 'name', 'logo', 'default_tournament_name', 'player_plugin__name', 'players_last_updated', 'data'))
    playerPlugins = list(PlayerPlugin.objects.values('id', 'name', 'class_package', 'class_name'))
    courses = list(Course.objects.values('id', 'name', 'priority', 'default'))
    courseTees = list(CourseTee.objects.values('id', 'name', 'priority', 'default', 'slope', 'course', 'course__name', 'color'))
    tournamentDates = list(TournamentDate.objects.values('id', 'date', 'tournament__id', 'tournament__name'))
    tournaments = list(Tournament.objects.values('id', 'name'))
    formats = list(Format.objects.values('id', 'name', 'priority', 'default'))
    players = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    activities = list(Activity.objects.values('id', 'date', 'title', 'notes'))
    context = {
        'clubs': clubs,
        'playerplugins': playerPlugins,
        'courses': courses,
        'courseTees': courseTees,
        'tournamentDates': tournamentDates,
        'formats': formats,
        'tournaments': tournaments,
        'players': players,
        'activities': activities
    }
    return render(request, 'golf/index.html', context=context)

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
        classModule = importlib.import_module('golf.plugins.'+club['player_plugin__class_package'])
        classAccess = getattr(classModule, club['player_plugin__class_name'])
        classInst = classAccess()
        classInst.loadPlayers(club['data'])
    resultList = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'last_updated', 'data', 'priority'))
    return JsonResponse({'data' : resultList})

def printPlayers(request):
    """
    View function for printing player roster, handicaps, and course index (if default)
    """
    from weasyprint import HTML, CSS
    from django.template.loader import get_template
    from django.template import Context
    context = {
        'players': Player.objects.all(),
        'clubs': Club.objects.all(),
        'courseTees': CourseTee.objects.filter(default=True).values('id', 'name', 'slope', 'course__name')
    }
    htmlTemplate = get_template('golf/playerpdf.html')
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="players.pdf"'
    return response

def printSignupSheets(request):
    """
    View function for printing signup sheet and starter sheet
    """
    from weasyprint import HTML, CSS
    from django.template.loader import get_template
    from django.template import Context
    context = {
        'clubs': Club.objects.all()
    }
    htmlTemplate = get_template('golf/signupsheets.html')
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="signupsheets.pdf"'
    return response

def editFormats(request):
    """
    View function for editting a tournament formats
    """
    return render_to_response('golf/editformats.html')

def getFormats(request):
    return HttpResponse('Test')

def newTournament(request):
    """
    Create function for tournaments
    Need to ask several questions about course, tee, format, if multi-round - how many... how do you ask from a plugin?
    """
    courses = []
    courseTees = []
    tees = []
    teeColors = []
    courseIds = request.POST.getlist('courses')
    teeIds = request.POST.getlist('tees')
    for i, teeId in enumerate(teeIds):
        courseTees.append(CourseTee.objects.filter(id=teeId).values('id', 'name', 'slope', 'course__name', 'color')[0])
        courseTees[i]['color_text'] = CourseTee.COLOR_CHOICES[courseTees[i]['color']][1]
        courseTees[i]['tees'] = list(Tee.objects.filter(course_tee__id=teeId).values('id', 'yardage', 'par', 'hole__name', 'hole__number'))
        courseTees[i]['hole_count'] = len(courseTees[i]['tees'])
        yardageIn = 0
        yardageOut = 0
        yardageTotal = 0
        parIn = 0
        parOut = 0
        parTotal = 0
        if (int(courseTees[i]['hole_count']) == 9):
            for front in range(0, 9):
                yardageOut += int(courseTees[i]['tees'][front]['yardage'])
                parOut += int(courseTees[i]['tees'][front]['par'])
            courseTees[i]['yardageOut'] = yardageOut
            courseTees[i]['yardageTotal'] = yardageOut
            courseTees[i]['parOut'] = parOut
            courseTees[i]['parTotal'] = parOut
        if (int(courseTees[i]['hole_count']) == 18):
            for front in range(0, 9):
                yardageOut += int(courseTees[i]['tees'][front]['yardage'])
                parOut += int(courseTees[i]['tees'][front]['par'])
            courseTees[i]['yardageOut'] = yardageOut
            courseTees[i]['parOut'] = parOut
            for back in range(9, 18):
                yardageIn += int(courseTees[i]['tees'][back]['yardage'])
                parIn += int(courseTees[i]['tees'][back]['par'])
            courseTees[i]['yardageIn'] = yardageIn
            courseTees[i]['yardageTotal'] = yardageOut + yardageIn
            courseTees[i]['parIn'] = parIn
            courseTees[i]['parTotal'] = parOut + parIn
    if (len(teeIds) != 1):
        for courseId in courseIds:
            courses.append(model_to_dict(Course.objects.get(id=courseId)))
    numRoundsRange = range(2, int(request.POST.get('numRounds'))+1)
    players = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'priority'))
    from django.core import serializers
    context = {
        "name": request.POST.get('name'),
        "dateStart": request.POST.get('dateStart'),
        "numRoundsRange": numRoundsRange,
        "numRounds": request.POST.get('numRounds'),
        "courses": courses,
        "courseTees": courseTees,
        "players": serializers.serialize('json', Player.objects.all())
    }
    return render(request, 'golf/newtournament.html', context=context)

def editTournament(request, tournamentId):
    """
    View function for editting a tournament
    Tournaments are associated with rounds
    Scorecards are associated with rounds
    """
    return render(request, 'golf/edittournament.html', context={'tournament_id': tournamentId})

def storeSettings(request):
    """
    Update function for club settings
    """
    c = Club(id=request.POST['id'], name=request.POST['name'], logo=request.POST['logo'], default_tournament_name=request.POST['default_tournament_name'], player_plugin__name=request.POST['player_plugin__name'], players_last_updated=request.POST['players_last_updated'], data=request.POST['data'])
    c.save()
    

def newScorecard(request):
    return HttpResponse('Test')

def addPlayerToScorecard(request):
    return HttpResponse('Test')

def addScoreToScorecard(request):
    return HttpResponse('Test')

def addRoundToPlayer(request):
    return HttpResponse('Test')
