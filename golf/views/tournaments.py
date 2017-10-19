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
    Ajax function to create a new tournament.
    TODO: Setup is an interesting concept... Can we ask if this is a team tourney
    """
    tournamentName = request.POST.get('tournamentName')
    numRounds = request.POST.get('numRounds')
    tournamentRoundsJSON = json.loads(request.POST.get('tournamentRoundsJSON'))
    availableCoursesJSON = json.loads(request.POST.get('availableCoursesJSON'))
    availableCourseTeesJSON = json.loads(request.POST.get('availableCourseTeesJSON'))

    """
    Set tournament
    """
    t = Tournament(name=tournamentName)
    t.save()

    """
    Set tournament rounds
    """
    for tournamentRound in tournamentRoundsJSON:
        d = datetime.strptime(tournamentRound['scheduledDate'], '%m/%d/%Y')
        fp = FormatPlugin.objects.get(id=tournamentRound['formatId'])
        tr = TournamentRound(scheduled_date=d, tournament=t, format_plugin=fp, name=tournamentRound['name'])
        tr.save()
        tournamentRound['id'] = tr.id
        """
        Set tournament courses and tees
        """
        for availableCourse in availableCoursesJSON:
            tr.available_courses.add(availableCourse['id'])
        for availableCourseTee in availableCourseTeesJSON:
            tr.available_course_tees.add(availableCourseTee['id'])
        tr.save()
    tournamentRoundsJSON = json.dumps(tournamentRoundsJSON, cls=DjangoJSONEncoder)
    availableCoursesJSON = json.dumps(availableCoursesJSON, cls=DjangoJSONEncoder)


    """
    Set tournament course tees
    """
    for availableCourseTee in availableCourseTeesJSON:
        availableCourseTee["tees"] = list(Tee.objects.filter(course_tee__id=availableCourseTee['id']).values('id', 'yardage', 'par', 'hole__name', 'hole__number').order_by('hole__number'))
        availableCourseTee["hole_count"] = len(availableCourseTee['tees'])
        availableCourseTee['yardageOut'] = 0
        availableCourseTee['parOut'] = 0
        availableCourseTee['yardageIn'] = 0
        availableCourseTee['parIn'] = 0
        #Someday should be able to work with 9 hole courses... Not today
        if (int(availableCourseTee['hole_count']) == 9):
            for front in range(9):
                availableCourseTee['yardageOut'] += int(availableCourseTee['tees'][front]['yardage'])
                availableCourseTee['parOut'] += int(availableCourseTee['tees'][front]['par'])
            availableCourseTee['yardageOut'] = availableCourseTee['yardageOut']
            availableCourseTee['yardageTotal'] = availableCourseTee['yardageOut']
            availableCourseTee['parOut'] = availableCourseTee['parOut']
            availableCourseTee['parTotal'] = availableCourseTee['parOut']
        if (int(availableCourseTee['hole_count']) == 18):
            for front in range(9):
                availableCourseTee['yardageOut'] += int(availableCourseTee['tees'][front]['yardage'])
                availableCourseTee['parOut'] += int(availableCourseTee['tees'][front]['par'])
            for back in range(9, 18):
                availableCourseTee['yardageIn'] += int(availableCourseTee['tees'][back]['yardage'])
                availableCourseTee['parIn'] += int(availableCourseTee['tees'][back]['par'])
            availableCourseTee['yardageTotal'] = availableCourseTee['yardageOut'] + availableCourseTee['yardageIn']
            availableCourseTee['parTotal'] = availableCourseTee['parOut'] + availableCourseTee['parIn']
    availableCourseTeesJSON = json.dumps(availableCourseTeesJSON, cls=DjangoJSONEncoder)
    print (availableCourseTeesJSON)

    context = {
        "tournamentId": t.id,
        "tournamentName": tournamentName,
        "numRounds": numRounds,
        "tournamentRoundsJSON": tournamentRoundsJSON,
        "availableCoursesJSON": availableCoursesJSON,
        "availableCourseTeesJSON": availableCourseTeesJSON
    }
    return JsonResponse(context)

def tournament(request):
    """
    View function for editting a tournament (even if new)
    """
    tournamentId = request.POST.get('tournamentId')
    tournamentName = request.POST.get('tournamentName')
    numRounds = request.POST.get('numRounds')
    tournamentRoundsJSON = json.loads(request.POST.get('tournamentRoundsJSON'))
    availableCoursesJSON = json.loads(request.POST.get('availableCoursesJSON'))
    availableCourseTeesJSON = json.loads(request.POST.get('availableCourseTeesJSON'))

    """
    Get all players
    """
    players = list(Player.objects.values())
    playersJSON = json.dumps(players, cls=DjangoJSONEncoder)

    context = {
        "tournamentId": tournamentId,
        "tournamentName": tournamentName,
        "numRounds": numRounds,
        "tournamentRoundsJSON": json.dumps(tournamentRoundsJSON, cls=DjangoJSONEncoder),
        "availableCoursesJSON": json.dumps(availableCoursesJSON, cls=DjangoJSONEncoder),
        "availableCourseTeesJSON": json.dumps(availableCourseTeesJSON, cls=DjangoJSONEncoder),
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
    tournamentRound = json.loads(request.POST['tournamentRoundJSON'])

    s = Scorecard()
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

    if (request.POST['startTime'] != ''):
        s.start_time = request.POST['startTime']

    if (request.POST['finishTime'] != ''):
        s.finish_time = request.POST['finishTime']

    s.save()

    try:
        t = Tournament.objects.get(id=tournamentId)
    except Tournament.DoesNotExist:
        return JsonResponse(json.loads('{}'))

    formatPlugin = FormatPlugin.objects.get(id=tournamentRound['formatId'])
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_package)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRound['id'], s.id)
    resultList = classInst.calculateScores(request.POST)

    resultListJSON = json.dumps(resultList, cls=DjangoJSONEncoder)
    print(resultListJSON)
    return JsonResponse({'results':resultList})

def clearRoundData(request):
    tournamentId = request.POST['tournamentId']
    tournamentName = request.POST['tournamentName']
    tournamentRound = json.loads(request.POST['tournamentRoundJSON'])

    try:
        tr = TournamentRound.objects.get(id=tournamentRound['id'])
    except TournamentRound.DoesNotExist:
        return False

    rounds = Round.objects.filter(tournament_round=tournamentRound['id'])
    for r in rounds:
        try:
            Scorecard.objects.filter(id=tr.scorecard.id).delete()
        except:
            pass
        Score.objects.filter(round=r.id).delete()
    return JsonResponse(json.loads('{}'))


def editTournament(request, tournamentId):
    """
    View function for editting a tournament
    Tournaments are associated with rounds
    Scorecards are associated with rounds
    """
    return render(request, 'golf/edittournament.html', context={'tournament_id': tournamentId})