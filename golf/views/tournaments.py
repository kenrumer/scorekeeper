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

def newTournament(request):
    """
    Ajax function to create a new tournament.
    TODO: Setup is an interesting concept... Can we ask if this is a team tourney
    """
    tournamentName = request.POST.get('tournamentName')
    roundCount = request.POST.get('roundCount')
    tournamentRounds = json.loads(request.POST.get('tournamentRounds'))
    availableCourses = json.loads(request.POST.get('availableCourses'))
    availableCourseTees = json.loads(request.POST.get('availableCourseTees'))

    """
    Set tournament
    """
    t = Tournament(name=tournamentName)
    t.save()

    """
    Set tournament rounds
    """
    for tournamentRound in tournamentRounds:
        d = datetime.strptime(tournamentRound['scheduledDate'], '%m/%d/%Y')
        fp = FormatPlugin.objects.get(id=tournamentRound['formatId'])
        tr = TournamentRound(scheduled_date=d, tournament=t, format_plugin=fp, name=tournamentRound['name'])
        tr.save()
        tournamentRound['id'] = tr.id
        """
        Set tournament courses and tees
        """
        for availableCourse in availableCourses:
            tr.available_courses.add(availableCourse['id'])
        for availableCourseTee in availableCourseTees:
            tr.available_course_tees.add(availableCourseTee['id'])
        tr.save()
    tournamentRounds = json.dumps(tournamentRounds, cls=DjangoJSONEncoder)
    availableCourses = json.dumps(availableCourses, cls=DjangoJSONEncoder)


    """
    Set tournament course tees
    """
    for availableCourseTee in availableCourseTees:
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
    availableCourseTees = json.dumps(availableCourseTees, cls=DjangoJSONEncoder)

    context = {
        "tournamentId": t.id,
        "tournamentName": tournamentName,
        "roundCount": roundCount,
        "tournamentRounds": tournamentRounds,
        "availableCourses": availableCourses,
        "availableCourseTees": availableCourseTees
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
    availableCourseTees = json.loads(request.POST.get('availableCourseTees'))

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
        "availableCourseTees": json.dumps(availableCourseTees, cls=DjangoJSONEncoder),
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
    tournamentRound = json.loads(request.POST['tournamentRound'])
    view = request.POST['view']

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
    
    scores = request.POST['scores']
    for score in scores:
        score['scorecardId'] = s.id

    formatPlugin = FormatPlugin.objects.get(id=tournamentRound['formatId'])
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_package)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRound['id'])
    classInst.updateScores(request.POST)
    
    roundStatus = getTournamentRoundStatus(tournamentRound['id'], view)
    return JsonResponse(roundStatus)

def getScores(request):
    tournamentId = request.POST['tournamentId']
    tournamentRound = json.loads(request.POST['tournamentRound'])
    view = request.POST['view']
    roundStatus = getTournamentRoundStatus(tournamentRound['id'], view)
    return JsonResponse(roundStatus)

def getPayout(request):
    tournamentId = request.POST['tournamentId']
    tournamentRound = json.loads(request.POST['tournamentRound'])

    formatPlugin = FormatPlugin.objects.get(id=tournamentRound['formatId'])
    classModule = importlib.import_module('golf.formatplugins.'+formatPlugin.class_package)
    classAccess = getattr(classModule, formatPlugin.class_name)
    classInst = classAccess(tournamentId, tournamentRound['id'])
    resultList = classInst.calculateScores(request.POST)
    
    roundStatus = getTournamentRoundPayoutStatus(tournamentRound['id'])
    return JsonResponse(roundStatus)

def getTournamentRoundPayoutStatus(tournamentRoundId):
    return {
        'net': getTournamentRoundStatus(tournamentRoundId, 'net'),
        'gross': getTournamentRoundStatus(tournamentRoundId, 'gross'),
        'netSkins':getTournamentRoundSkinStatus(tournamentRoundId, 'net'),
        'skins':getTournamentRoundSkinStatus(tournamentRoundId, 'gross')
    }

def getTournamentRoundSkinStatus(tournamentRoundId, view):
    """
    This method returns the current tournament status
    """
    skins = []
    order = 'total'
    if (view == 'net'):
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
        skin = []
        playerName = r.player.name
        for index, item in enumerate(scores):
            if (view == 'net'):
                if (item.skin_net == 1):
                    skin.append(i)
            else:
                if (item.skin == 1):
                    skin.append(i)
        skins.append(skin)
    return { 'playerName': playerName, 'skins': skins }
    
def getTournamentRoundStatus(tournamentRoundId, view):
    """
    This method returns the current tournament status in an easy way for datatables to read
    """
    rows = []
    styles = []
    order = 'total'
    if (view == 'net'):
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
        row.append('<div class="btn-group"><button type="button" class="btn btn-default" onclick="javascript:editScorecard();" aria-label="Edit Scorecard"><span class="glyphicon glyphicon-menu-hamburger" aria-hidden="true"></span></button><button type="button" class="btn btn-default" onclick="javascript:editScorecardRow();" aria-label="Edit Scorecard Row"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button></div>')
        row.append(r.player.name)
        row.append(r.course_handicap)
        for index, item in enumerate(scores):
            if (index == 9):
                row.append(r.total_out)
            if (view == 'net'):
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