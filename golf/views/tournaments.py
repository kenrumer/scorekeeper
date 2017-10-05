from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Tournament, TournamentDate, FormatPlugin, Course, CourseTee, Player, Tee, Round, Scorecard
from django.forms.models import model_to_dict
import importlib
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

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
    tournamentDuplicate = False
    tournamentDateDuplicate = False
    tournamentName = request.POST.get('tournamentName')
    dateStart = request.POST.get('dateStart')
    formatId = request.POST.get('formatId')
    setupId = request.POST.get('setupId')
    numRounds = request.POST.get('numRounds')
    coursesJSON = json.loads(request.POST.get('coursesJSON'))
    courseTeesJSON = json.loads(request.POST.get('courseTeesJSON'))
    print (tournamentName)
    print (dateStart)
    print (formatId)
    print (setupId)
    print (numRounds)
    print (coursesJSON)
    print (courseTeesJSON)
    
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
        t = Tournament.objects.get(name=tournamentName)
        tournamentDuplicate = True
    except Tournament.DoesNotExist:
        t = Tournament(name=tournamentName)
    t.format_plugin = FormatPlugin.objects.get(id=formatId)
    t.save()
    
    """
    Get courses
    """
    for course in coursesJSON:
        t.courses.add(course['id'])
    t.save()
    coursesJSON = json.dumps(coursesJSON, cls=DjangoJSONEncoder)

    """
    Get tees
    """
    for courseTee in courseTeesJSON:
        t.course_tees.add(courseTee['id'])
        courseTee["tees"] = list(Tee.objects.filter(course_tee__id=courseTee['id']).values('id', 'yardage', 'par', 'hole__name', 'hole__number').order_by('hole__number'))
        courseTee["hole_count"] = len(courseTee['tees'])
        courseTee['yardageOut'] = 0
        courseTee['parOut'] = 0
        courseTee['yardageIn'] = 0
        courseTee['parIn'] = 0
        #Someday should be able to work with 9 hole courses... Not today
        if (int(courseTee['hole_count']) == 9):
            for front in range(0, 9):
                courseTee['yardageOut'] += int(courseTee['tees'][front]['yardage'])
                courseTee['parOut'] += int(courseTee['tees'][front]['par'])
            courseTee['yardageOut'] = courseTee['yardageOut']
            courseTee['yardageTotal'] = courseTee['yardageOut']
            courseTee['parOut'] = courseTee['parOut']
            courseTee['parTotal'] = courseTee['parOut']
        if (int(courseTee['hole_count']) == 18):
            for front in range(0, 9):
                courseTee['yardageOut'] += int(courseTee['tees'][front]['yardage'])
                courseTee['parOut'] += int(courseTee['tees'][front]['par'])
            for back in range(9, 18):
                courseTee['yardageIn'] += int(courseTee['tees'][back]['yardage'])
                courseTee['parIn'] += int(courseTee['tees'][back]['par'])
            courseTee['yardageTotal'] = courseTee['yardageOut'] + courseTee['yardageIn']
            courseTee['parTotal'] = courseTee['parOut'] + courseTee['parIn']
    courseTeesJSON = json.dumps(courseTeesJSON, cls=DjangoJSONEncoder)
    print (courseTeesJSON)
    t.save()

    """
    Get all players
    """
    players = list(Player.objects.values('id', 'name', 'club_member_number', 'handicap_index'))
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)

    """
    Set tournament first round/only round date
    """
    d = datetime.strptime(request.POST.get('dateStart'), '%m/%d/%Y')
    try:
        td = TournamentDate.objects.get(date=d)
        tournamentDateDuplicate = True
    except TournamentDate.DoesNotExist:
        td = TournamentDate(date=d, tournament=t)
        td.save()

    """
    Render the page
    """
    context = {
        "id": t.id,
        "name": request.POST.get('name'),
        "duplicate": tournamentDuplicate,
        "dateId": td.id,
        "date": request.POST.get('dateStart'),
        "dateDuplicate": tournamentDateDuplicate,
        "numRounds": request.POST.get('numRounds'),
        "coursesJSON": coursesJSON,
        "courseTeesJSON": courseTeesJSON,
        "players": players,
        "playersJSON": playersJSON
    }
    print (context)
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