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
    url: '/golf/newtournament/'
    """
    tournamentName = request.POST.get('tournamentName')
    tournamentRounds = json.loads(request.POST.get('tournamentRounds'))
    roundCount = request.POST.get('roundCount')
    courses = json.loads(request.POST.get('courses'))
    courseTees = json.loads(request.POST.get('courseTees'))

    resObject = {}
    resObject['courseTees'] = courseTees
    resObject['courses'] = courses

    """
    Create tournament
    """
    t = Tournament(name=tournamentName)
    t.save()
    tempTournament = serializers.serialize('json', [t])
    resObject['tournament'] = json.loads(tempTournament[1:-1])

    """
    Create tournament rounds
    """
    for tournamentRound in tournamentRounds:
        """
        Get the tournament formatId
        Initialize Format Data
        """
        fp = FormatPlugin.objects.get(id=tournamentRound['formatId'])
        d = datetime.strptime(tournamentRound['scheduledDate'], '%m/%d/%Y')
        tr = TournamentRound(scheduled_date=d, tournament=t, format_plugin=fp, data=fp.data, name=tournamentRound['name'])
        tr.save()
        """
        Set tournament round courses and tees
        """
        for course in courses:
            tr.courses.add(course['pk'])
        for courseTee in courseTees:
            tr.course_tees.add(courseTee['pk'])
        tr.save()
    resObject['tournamentRounds'] = json.loads(serializers.serialize('json', TournamentRound.objects.filter(tournament=t)))

    """
    Set tournament course tees
    """
    courseTeeIds = []
    for courseTee in courseTees:
        courseTeeIds.append(courseTee['pk'])
    resObject['tees'] = json.loads(serializers.serialize('json', Tee.objects.filter(course_tee__in=courseTeeIds).order_by('hole__number')))

    """
    Get all players
    """
    resObject['players'] = json.loads(serializers.serialize('json', Player.objects.all().order_by('name', 'priority')))
    return JsonResponse(resObject)

def tournament(request):
    """
    View function for editting a tournament (even if new)
    url: '/golf/tournament/'
    """
    resObject = {}
    resObject['courseTees'] = request.POST.get('courseTees')
    resObject['courses'] = request.POST.get('courses')
    resObject['tees'] = request.POST.get('tees')
    resObject['tournament'] = request.POST.get('tournament')
    resObject['tournamentRounds'] = request.POST.get('tournamentRounds')
    resObject['players'] = request.POST.get('players')

    return render(request, 'golf/tournament.html', context=resObject)

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
    tournamentRound = json.loads(request.POST['tournamentRound'])
    viewTab = request.POST['viewTab']
    roundStatus = getTournamentRoundStatus(tournamentRound, viewTab)
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
    
def getTournamentRoundStatus(tournamentRound, viewTab):
    """
    This method returns the current tournament status in an easy way for datatables to read
    """
    rows = []
    styles = []
    order = 'total'
    if (viewTab == 'net'):
        order = 'net'
    try:
        rounds = Round.objects.filter(tournament_round=tournamentRound['pk']).order_by(order)
    except:
        print ('Failed to get rounds')
        print (tournamentRound)
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