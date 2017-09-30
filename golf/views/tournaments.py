from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Tournament, TournamentDate, FormatPlugin, Course, CourseTee, Player, Tee, Round, Scorecard
from django.forms.models import model_to_dict
import importlib
from datetime import datetime
import json

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
    from django.core import serializers
    courses = []
    courseTees = []
    courseIds = request.POST.getlist('courses')
    courseTeeIds = request.POST.getlist('tees')
    tournamentDuplicate = False
    
    """
    Get tournament information.  This may have changed because of user error
        Tournament (by name) already exists
        Date start change
        Format change
        Course add/remove
        Course tee add/remove
    Will send this data to the newTournament template
    """
    try:
        t = Tournament.objects.get(name=request.POST.get('name'))
        tournamentDuplicate = True
    except Tournament.DoesNotExist:
        t = Tournament(name=request.POST.get('name'))
    t.format_plugin = FormatPlugin.objects.get(id=request.POST.get('formatId'))
    t.save()
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    
    """
    Get courses
    """
    for courseId in courseIds:
        c = Course.objects.get(id=courseId)
        courses.append(list(Course.objects.filter(id=courseId).values('name', 'priority', 'default'))[0])
        t.courses.add(c)
    coursesJSON = json.dumps(courses, cls=DjangoJSONEncoder)
    
    """
    Get tees
    """
    for i, courseTeeId in enumerate(courseTeeIds):
        ct = CourseTee.objects.get(id=courseTeeId)
        t.course_tees.add(ct)
        courseTees.append(list(CourseTee.objects.filter(id=courseTeeId).values('id', 'name', 'slope', 'course__name', 'color'))[0])
        courseTees[i]["tees"] = list(Tee.objects.filter(course_tee__id=courseTeeId).values('id', 'yardage', 'par', 'hole__name', 'hole__number'))
        courseTees[i]["hole_count"] = len(courseTees[i]['tees'])
        courseTees[i]['yardageOut'] = 0
        courseTees[i]['parOut'] = 0
        courseTees[i]['yardageIn'] = 0
        courseTees[i]['parIn'] = 0
        #Someday should be able to work with 9 hole courses... Not today
        #if (int(courseTees[i]['hole_count']) == 9):
        #    for front in range(0, 9):
        #        courseTees[i]['yardageOut'] += int(courseTees[i]['tees'][front]['yardage'])
        #        courseTees[i]['parOut'] += int(courseTees[i]['tees'][front]['par'])
        #    courseTees[i]['yardageOut'] = courseTees[i]['yardageOut']
        #    courseTees[i]['yardageTotal'] = courseTees[i]['yardageOut']
        #    courseTees[i]['parOut'] = courseTees[i]['parOut']
        #    courseTees[i]['parTotal'] = courseTees[i]['parOut']
        #if (int(courseTees[i]['hole_count']) == 18):
        for front in range(0, 9):
            courseTees[i]['yardageOut'] += int(courseTees[i]['tees'][front]['yardage'])
            courseTees[i]['parOut'] += int(courseTees[i]['tees'][front]['par'])
        for back in range(9, 18):
            courseTees[i]['yardageIn'] += int(courseTees[i]['tees'][back]['yardage'])
            courseTees[i]['parIn'] += int(courseTees[i]['tees'][back]['par'])
        courseTees[i]['yardageTotal'] = courseTees[i]['yardageOut'] + courseTees[i]['yardageIn']
        courseTees[i]['parTotal'] = courseTees[i]['parOut'] + courseTees[i]['parIn']
    courseTeesJSON = json.dumps(courseTees, cls=DjangoJSONEncoder)
    t.save()

    """
    Get all players
    """
    players = Player.objects.all().values('id', 'name', 'club_member_number', 'handicap_index')
    playersJSON = json.dumps(list(Player.objects.all().values('id', 'name', 'club_member_number', 'handicap_index')), cls=DjangoJSONEncoder)

    """
    Set tournament first round/only round date
    """
    d = datetime.strptime(request.POST.get('dateStart'), '%m/%d/%Y')
    td = TournamentDate(date=d, tournament=t)
    td.save()
    context = {
        "tournamentId": t.id,
        "tournamentDuplicate": tournamentDuplicate,
        "name": request.POST.get('name'),
        "numRounds": request.POST.get('numRounds'),
        "courses": courses,
        "coursesJSON": coursesJSON,
        "courseTees": courseTees,
        "courseTeesJSON": courseTeesJSON,
        "players": players,
        "playersJSON": playersJSON
    }
    return render(request, 'golf/newtournament.html', context=context)

def calculateScores(request):
    """
    Score the tournament
    Save the data
    Return the rankings grosses and nets and colors per cell
    """
    tournamentId = request.POST['tournamentId']
    s = Scorecard(date=request.POST['date'], tee_time=request.POST['teeTime'], finish_time=request.POST['finishTime'], scorer=request.POST['scorer'], attest=request.POST['attest'])
    t = Tournament.objects.get(id=tournamentId)
    formatPlugin = model_to_dict(FormatPlugin.objects.get(id=t.format_plugin__id))
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin['class_package'])
    classAccess = getattr(classModule, formatPlugin['class_name'])
    classInst = classAccess(tournamentId, s.id)
    classInst.calculateScores(request.POST)

    resultList = list(Round.objects.get(tournament_id=request.POST['tournamentId']).all())
    print(resultList)
    return JsonResponse(resultList)

def editTournament(request, tournamentId):
    """
    View function for editting a tournament
    Tournaments are associated with rounds
    Scorecards are associated with rounds
    """
    return render(request, 'golf/edittournament.html', context={'tournament_id': tournamentId})