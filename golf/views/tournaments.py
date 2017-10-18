from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Tournament, TournamentRound, FormatPlugin, Course, CourseTee, Player, Tee, Round, Scorecard, Score
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

def checkForTournamentDuplicate(request):
    """
    Ajax function to check if the tournament already exists
    """
    tournamentName = request.POST.get('tournamentName')
    try:
        Tournament.objects.get(name=tournamentName)
        responseJSON = '{"duplicate": true}'
    except:
        responseJSON = '{"duplicate": false}'
    return JsonResponse(json.loads(responseJSON))

def newTournament(request):
    """
    Ajax function to create a new tournament.  Required because the reload button is creating new tournaments instead of showing the data
    how do you ask from a plugin?
    """
    tournamentName = request.POST.get('tournamentName')
    formatId = request.POST.get('formatId')
    setupId = request.POST.get('setupId')
    numRounds = request.POST.get('numRounds')
    tournamentRoundsJSON = json.loads(request.POST.get('tournamentRoundsJSON'))
    coursesJSON = json.loads(request.POST.get('coursesJSON'))
    courseTeesJSON = json.loads(request.POST.get('courseTeesJSON'))
    
    """
    Get tournament information.  This may have changed because of user error
        Tournament (by name) already exists
        Date start change
        Format change
        Course add/remove
        Course tee add/remove
    Will send this data to the newTournament template
    """
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
    print (courseTeesJSON)
    for courseTee in courseTeesJSON:
        t.course_tees.add(courseTee['id'])
        t.save()
        courseTee["tees"] = list(Tee.objects.filter(course_tee__id=courseTee['id']).values('id', 'yardage', 'par', 'hole__name', 'hole__number').order_by('hole__number'))
        courseTee["hole_count"] = len(courseTee['tees'])
        courseTee['yardageOut'] = 0
        courseTee['parOut'] = 0
        courseTee['yardageIn'] = 0
        courseTee['parIn'] = 0
        #Someday should be able to work with 9 hole courses... Not today
        if (int(courseTee['hole_count']) == 9):
            for front in range(9):
                courseTee['yardageOut'] += int(courseTee['tees'][front]['yardage'])
                courseTee['parOut'] += int(courseTee['tees'][front]['par'])
            courseTee['yardageOut'] = courseTee['yardageOut']
            courseTee['yardageTotal'] = courseTee['yardageOut']
            courseTee['parOut'] = courseTee['parOut']
            courseTee['parTotal'] = courseTee['parOut']
        if (int(courseTee['hole_count']) == 18):
            for front in range(9):
                courseTee['yardageOut'] += int(courseTee['tees'][front]['yardage'])
                courseTee['parOut'] += int(courseTee['tees'][front]['par'])
            for back in range(9, 18):
                courseTee['yardageIn'] += int(courseTee['tees'][back]['yardage'])
                courseTee['parIn'] += int(courseTee['tees'][back]['par'])
            courseTee['yardageTotal'] = courseTee['yardageOut'] + courseTee['yardageIn']
            courseTee['parTotal'] = courseTee['parOut'] + courseTee['parIn']
    courseTeesJSON = json.dumps(courseTeesJSON, cls=DjangoJSONEncoder)
    print (courseTeesJSON)

    """
    Set tournament rounds
    """
    tournamentRoundIds = []
    for tournamentRound in tournamentRoundsJSON:
        d = datetime.strptime(tournamentRound.date, '%m/%d/%Y')
        try:
            tr = TournamentRound.objects.get(date=d)
        except TournamentRound.DoesNotExist:
            tr = TournamentRound(date=d, tournament=t)
            tr.save()
        tournamentRoundIds.append(tr.id)
    tournamentRoundIdsJSON = json.dumps(tournamentRoundIds, cls=DjangoJSONEncoder)
    tournamentRoundsJSON = json.dumps(tournamentRoundsJSON, cls=DjangoJSONEncoder)
    context = {
        "tournamentId": t.id,
        "tournamentName": tournamentName,
        "tournamentRoundIdsJSON": tournamentRoundIdsJSON,
        "tournamentRoundsJSON": tournamentRoundsJSON,
        "numRounds": numRounds,
        "formatId": formatId,
        "setupId": setupId,
        "coursesJSON": coursesJSON,
        "courseTeesJSON": courseTeesJSON
    }
    return JsonResponse(context)

def tournament(request):
    """
    View function for editting a tournament (even if new)
    """
    tournamentId = request.POST.get('tournamentId')
    tournamentName = request.POST.get('tournamentName')
    formatId = request.POST.get('formatId')
    setupId = request.POST.get('setupId')
    numRounds = request.POST.get('numRounds')
    tournamentRoundsJSON = json.loads(request.POST.get('tournamentRoundsJSON'))
    tournamentRoundIdsJSON = json.loads(request.POST.get('tournamentRoundIdsJSON'))
    coursesJSON = json.loads(request.POST.get('coursesJSON'))
    courseTeesJSON = json.loads(request.POST.get('courseTeesJSON'))

    """
    Get all players
    """
    players = list(Player.objects.values('id', 'name', 'club_member_number', 'handicap_index'))
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)

    context = {
        "tournamentId": tournamentId,
        "tournamentName": tournamentName,
        "formatId": formatId,
        "setupId": setupId,
        "numRounds": numRounds,
        "tournamentRoundIdsJSON": json.dumps(tournamentRoundIdsJSON, cls=DjangoJSONEncoder),
        "tournamentRoundsJSON": json.dumps(tournamentRoundsJSON, cls=DjangoJSONEncoder),
        "coursesJSON": json.dumps(coursesJSON, cls=DjangoJSONEncoder),
        "courseTeesJSON": json.dumps(courseTeesJSON, cls=DjangoJSONEncoder),
        "players": players,
        "playersJSON": playersJSON
    }
    return render(request, 'golf/tournament.html', context=context)

def calculateScores(request):
    """
    Score the tournament
    Save the data
    Return the rankings grosses and nets and colors per cell
    """
    tournamentId = request.POST['tournamentId']
    tournamentRoundId = request.POST['tournamentRoundId']
    try:
        td = TournamentRound.objects.get(id=tournamentRoundId);
    except TournamentRound.DoesNotExist:
        return JsonResponse(json.loads('{}'))

    s = Scorecard(tournament_date=td)
    if (request.POST['scorer'] != ''):
        try:
            scorer = Player.objects.get(club_member_number=request.POST['scorerId'])
            s.scorer = scorer
        except Player.DoesNotExist:
            s.external_scorer = request.POST['scorer']

    if (request.POST['attest'] != ''):
        try:
            attest = Player.objects.get(club_member_number=request.POST['attestId'])
            s.attest = attest
        except Player.DoesNotExist:
            s.external_attest = request.POST['attest']

    if (request.POST['teeTime'] != ''):
        s.tee_time = request.POST['teeTime']

    if (request.POST['finishTime'] != ''):
        s.finish_time = request.POST['finishTime']

    s.save()

    try:
        t = Tournament.objects.get(id=tournamentId)
    except Tournament.DoesNotExist:
        return JsonResponse(json.loads('{}'))

    formatPlugin = FormatPlugin.objects.get(id=t.format_plugin.id)
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_package)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRoundId, s.id)
    resultList = classInst.calculateScores(request.POST)

    resultListJSON = json.dumps(resultList, cls=DjangoJSONEncoder)
    print(resultListJSON)
    return JsonResponse({'results':resultList})

def clearRoundData(request):
    tournamentId = request.POST['tournamentId']
    tournamentName = request.POST['tournamentName']
    tournamentRoundId = request.POST['tournamentRoundId']
    tournamentRound = request.POST['tournamentRound']
    roundId = request.POST['roundId']
    try:
        tr = TournamentRound.objects.get(id=tournamentRoundId);
    except TournamentRound.DoesNotExist:
        return JsonResponse(json.loads('{}'))
    
    scorecards = Scorecard.objects.filter(tournament_round=tr).delete()
    rounds = Round.objects.filter(tournament_round=tr)
    for r in rounds:
        Score.objects.filter(round=r.id).delete()
    return JsonResponse(json.loads('{}'))
        

def editTournament(request, tournamentId):
    """
    View function for editting a tournament
    Tournaments are associated with rounds
    Scorecards are associated with rounds
    """
    return render(request, 'golf/edittournament.html', context={'tournament_id': tournamentId})