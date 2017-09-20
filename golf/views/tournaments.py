from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Tournament, TournamentDate, FormatPlugin, Course, CourseTee, Player, Tee, Round
from django.forms.models import model_to_dict
import importlib
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
    teeIds = request.POST.getlist('tees')
    try:
        t = Tournament.objects.get(name=request.POST.get('name'))
        print('WARNING: duplicate tournament name')
    except Tournament.DoesNotExist:
        t = Tournament(name=request.POST.get('name'))
    t.format_plugin = FormatPlugin.objects.get(id=request.POST.get('formatId'))
    t.save()
    for i, teeId in enumerate(teeIds):
        ct = CourseTee.objects.get(id=teeId)
        t.course_tees.add(ct)
        courseTees.append(list(CourseTee.objects.filter(id=teeId).values('id', 'name', 'slope', 'course__name', 'color'))[0])
        courseTees[i]['color_text'] = CourseTee.COLOR_CHOICES[courseTees[i]['color']][1]
        courseTees[i]['tees'] = list(Tee.objects.filter(course_tee__id=teeId).values('id', 'yardage', 'par', 'hole__name', 'hole__number'))
        courseTees[i]['hole_count'] = len(courseTees[i]['tees'])
        yardageIn = 0
        yardageOut = 0
        parIn = 0
        parOut = 0
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
    for courseId in courseIds:
        c = Course.objects.get(id=courseId)
        courses.append(model_to_dict(c))
        t.courses.add(c)
    from datetime import datetime
    d = datetime.strptime(request.POST.get('dateStart'), '%m/%d/%Y')
    td = TournamentDate(date=d, tournament=t)
    td.save()
    numRoundsRange = range(2, int(request.POST.get('numRounds'))+1)
    context = {
        "tournamentId": t.id,
        "name": request.POST.get('name'),
        "numRoundsRange": numRoundsRange,
        "numRounds": request.POST.get('numRounds'),
        "courses": courses,
        "courseTees": courseTees,
        "players": serializers.serialize('json', Player.objects.all())
    }
    return render(request, 'golf/newtournament.html', context=context)

def calculateScores(request):
    """
    Score the tournament
    Save the data
    Return the rankings grosses and nets and colors per cell
    """
    tournament = model_to_dict(Tournament.objects.get(id=request.POST['tournamentId']))
    formatPlugin = model_to_dict(FormatPlugin.objects.get(id=tournament['format_plugin']))
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin['class_package'])
    classAccess = getattr(classModule, formatPlugin['class_name'])
    classInst = classAccess()
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