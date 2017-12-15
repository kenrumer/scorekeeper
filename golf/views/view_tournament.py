from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from ..models import Tournament, TournamentRound, FormatPlugin, Course, CourseTee, Player, Tee, Round, Scorecard, Score
from django.forms.models import model_to_dict
import importlib
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

def editFormats(request):
    """
    View function for editting a tournament formats
    """
    return render_to_response('golf/editformats.html')

def getFormats(request):
    return HttpResponse('Test')

def newTournament(request):
    """
    Ajax function to create a new tournament.
    TODO: Setup is an interesting concept... Can we ask if this is a team tourney
    """
    tournamentName = request.POST.get('tournamentName')
    tournamentRounds = json.loads(request.POST.get('tournamentRounds'))
    roundCount = request.POST.get('roundCount')
    courses = json.loads(request.POST.get('courses'))
    courseTees = json.loads(request.POST.get('courseTees'))

    retObject = {}
    """
    Create tournament
    """
    t = Tournament(name=tournamentName)
    t.save()
    retObject['tournamentName'] = serializers.serialize('json', t)

    """
    Create tournament rounds
    """
    tournamentRoundsAry = []
    for tournamentRound in tournamentRounds:
        """
        Get the tournament formatId
        Initialize Format Data
        """
        fp = FormatPlugin.objects.get(id=tournamentRound['formatId'])
        d = datetime.strptime(tournamentRound['scheduledDate'], '%m/%d/%Y')
        tr = TournamentRound(scheduled_date=d, tournament=t, format_plugin=fp, data=fp.data, name=tournamentRound['name'])
        tr.save()
        tournamentRoundsAry.append(tr.id)
        """
        Set tournament courses and tees
        """
        for course in courses:
            tr.courses.add(course['pk'])
        for courseTee in courseTees:
            tr.course_tees.add(courseTee['pk'])
        tr.save()
    retObject['tournamentRounds'] = serializers.serialize('json', TournamentRound.objects.filter(id__in=tournamentRoundsAry))
    #tournamentRounds = json.dumps(tournamentRounds, cls=DjangoJSONEncoder)
    #courses = json.dumps(courses, cls=DjangoJSONEncoder)

    """
    Set tournament course tees
    """
    for courseTee in courseTees:
        courseTee["tees"] = list(Tee.objects.filter(course_tee__id=courseTee['pk']).values('id', 'yardage', 'par', 'hole__name', 'hole__number').order_by('hole__number'))
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
    courseTees = json.dumps(courseTees, cls=DjangoJSONEncoder)
    retObject['tournament'] = serializers.serialize('json', t)
    print(retObject)

    context = {
        "tournamentId": t.id,
        "tournamentName": tournamentName,
        "roundCount": roundCount,
        "tournamentRounds": tournamentRounds,
        "courses": courses,
        "courseTees": courseTees
    }
    return JsonResponse(context)

def tournament(request):
    """
    View function for editting a tournament (even if new)
    """
    tournamentId = request.POST.get('tournamentId')
    tournamentName = request.POST.get('tournamentName')
    roundCount = request.POST.get('roundCount')
    tournamentRounds = json.loads(request.POST.get('tournamentRounds'))
    availableCourses = json.loads(request.POST.get('availableCourses'))
    courseTees = json.loads(request.POST.get('courseTees'))

    """
    Get all players
    """
    players = list(Player.objects.values())
    players = json.dumps(players, cls=DjangoJSONEncoder)

    context = {
        "tournamentId": tournamentId,
        "tournamentName": tournamentName,
        "roundCount": roundCount,
        "tournamentRounds": json.dumps(tournamentRounds, cls=DjangoJSONEncoder),
        "availableCourses": json.dumps(availableCourses, cls=DjangoJSONEncoder),
        "courseTees": json.dumps(courseTees, cls=DjangoJSONEncoder),
        "players": players
    }
    return render(request, 'golf/tournament.html', context=context)

def updateScores(request):
    """
    Score the tournament
    Save the data
    Return the rankings grosses and nets and colors per cell
    """
    tournamentId = request.POST['tournamentId']
    tournamentName = request.POST['tournamentName']
    tournamentRound = json.loads(request.POST['tournamentRound'])
    scorecard = json.loads(request.POST['scorecard'])
    players = json.loads(request.POST['players'])
    viewTab = request.POST['viewTab']

    s = Scorecard()
    if (scorecard['scorer'] != ''):
        try:
            scorer = Player.objects.get(club_member_number=scorecard['scorerId'])
            s.scorer = scorer
        except Player.DoesNotExist:
            s.external_scorer = scorecard['scorer']
    if (scorecard['attest'] != ''):
        try:
            attest = Player.objects.get(club_member_number=scorecard['attestId'])
            s.attest = attest
        except Player.DoesNotExist:
            s.external_attest = scorecard['attest']
    if (scorecard['startTime'] != ''):
        s.start_time = scorecard['startTime']
    if (scorecard['finishTime'] != ''):
        s.finish_time = scorecard['finishTime']
    s.save()

    for player in players:
        player['scorecardId'] = s.id

    formatPlugin = FormatPlugin.objects.get(id=tournamentRound['formatId'])
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_module)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRound['id'])
    classInst.updateScores(players)
    
    roundStatus = getTournamentRoundStatus(tournamentRound['id'], viewTab)
    return JsonResponse(roundStatus)

def getScores(request):
    tournamentId = request.POST['tournamentId']
    tournamentRound = json.loads(request.POST['tournamentRound'])
    viewTab = request.POST['viewTab']
    roundStatus = getTournamentRoundStatus(tournamentRound['id'], viewTab)
    return JsonResponse(roundStatus)

def getPayout(request):
    tournamentId = request.POST['tournamentId']
    tournamentRound = json.loads(request.POST['tournamentRound'])

    formatPlugin = FormatPlugin.objects.get(id=tournamentRound['formatId'])
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_package)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRound['id'])
    resultHtml = classInst.showPayout()

    return HttpResponse(resultHtml)
    
def getTournamentRoundStatus(tournamentRoundId, viewTab):
    """
    This method returns the current tournament status in an easy way for datatables to read
    """
    rows = []
    styles = []
    order = 'total'
    if (viewTab == 'net'):
        order = 'net'
    try:
        rounds = Round.objects.filter(tournament_round=tournamentRoundId).order_by(order)
    except:
        print ('Failed to get rounds')
        print (tournamentRoundId)
        return False
    i = 1
    for r in rounds:
        try:
            scores = Score.objects.filter(round=r.id).order_by('tee__hole__number')
        except:
            print ('Failed to get scores')
            print (r.id)
            return False
        style = []
        row = []
        row.append(i)
        row.append('<div class="btn-group"><button type="button" class="btn btn-xs btn-default" onclick="javascript:editScorecard();" aria-label="Edit Scorecard"><span class="glyphicon glyphicon-menu-hamburger" aria-hidden="true"></span></button><button type="button" class="btn btn-xs btn-default" onclick="javascript:editScorecardRow();" aria-label="Edit Scorecard Row"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button></div>')
        row.append(r.player.name)
        row.append(r.course_handicap)
        for index, item in enumerate(scores):
            if (index == 9):
                row.append(r.total_out)
            if (viewTab == 'net'):
                style.append(item.score_net_style)
                row.append(item.score_net)
            else:
                style.append(item.score_style)
                row.append(item.score)
        row.append(r.total_in)
        row.append(r.total)
        row.append(r.course_handicap)
        row.append(r.net)
        i += 1
        rows.append(row)
        styles.append(style)
    return { 'rows': rows, 'styles': styles }

def clearRoundData(request):
    tournamentRound = json.loads(request.POST['tournamentRound'])

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
        r.delete()
    return JsonResponse(json.loads('{}'))


def editTournament(request, tournamentId):
    """
    View function for editting a tournament
    Tournaments are associated with rounds
    Scorecards are associated with rounds
    """
    return render(request, 'golf/edittournament.html', context={'tournament_id': tournamentId})