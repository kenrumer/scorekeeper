from abc import ABCMeta, abstractmethod
from .models import Player, Club, CourseTee, Tee, Round, Score, Tournament, TournamentRound, Scorecard
from django.utils import timezone

"""
    Base class for loading players from a plugin.  The plugin class name and filename are in the Club table
    TODO: Activate, Inactivate, Delete
"""
class PlayerBase(object):
    __metaclass__ = ABCMeta
    """
        Get the existing list of players for the plugin
    """
    player_list = list(Player.objects.values('id', 'club_member_number', 'name', 'handicap_index', 'high_handicap_index', 'low_handicap_index', 'data', 'priority'))
    club = list(Club.objects.values('id'))[0]

    def __init__(self):
        pass

    @abstractmethod
    def loadPlayers(self, data):
        """
            Get the updated list from plugin
        """
        raise NotImplementedError

    def mergePlayers(self, newPlayerList):
        pl = self.player_list
        for newPlayer in newPlayerList:
            found = False
            for i in range(len(pl)):
                if (int(pl[i]['club_member_number']) == int(newPlayer['club_member_number'])):
                    found = True
                    pl[i]['name'] = newPlayer['name']
                    pl[i]['handicap_index'] = newPlayer['handicap_index']
                    pl[i]['data'] = newPlayer['data']
                    pl[i]['player_type__id'] = newPlayer['player_type__id']
                    if (float(pl[i]['high_handicap_index']) < float(newPlayer['handicap_index'])):
                        pl[i]['high_handicap_index'] = newPlayer['handicap_index']
                    if (float(pl[i]['low_handicap_index']) > float(newPlayer['handicap_index'])):
                        pl[i]['low_handicap_index'] = newPlayer['handicap_index']
                    continue
            if (found == False):
                pl.append({'id':-1, 'club_member_number':newPlayer['club_member_number'], 'name':newPlayer['name'], 'handicap_index':newPlayer['handicap_index'], 'player_type__id':1, 'data':newPlayer['data'], 'high_handicap_index':newPlayer['handicap_index'], 'low_handicap_index':newPlayer['handicap_index']})
        self.player_list = pl

    def storePlayers(self):
        pl = self.player_list
        c = Club.objects.get(id=self.club['id'])
        c.players_last_updated = timezone.now()
        c.save()
        for player in pl:
            if (player['id'] != -1):
                p = Player.objects.get(id=player['id'])
                p.club_member_number=player['club_member_number']
                p.name=player['name']
                p.handicap_index=player['handicap_index']
                p.data=player['data']
                p.high_handicap_index=player['high_handicap_index']
                p.low_handicap_index=player['low_handicap_index']
                p.last_updated=timezone.now()
                p.save()
            else:
                p = Player(club_member_number=player['club_member_number'], name=player['name'], handicap_index=player['handicap_index'], data=player['data'], high_handicap_index=player['high_handicap_index'], low_handicap_index=player['low_handicap_index'], last_updated=timezone.now())
                p.save()

class FormatBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, tournamentId, tournamentRoundId, scorecardId):
        self.tournamentId = tournamentId
        self.tournamentRoundId = tournamentRoundId
        self.scorecardId = scorecardId
        print(tournamentRoundId)
        pass

    @abstractmethod
    def calculateScores(self, scores):
        return

    def mergePlayerResults(self, newPlayerResultList):
        resultList = []
        try:
            tr = TournamentRound.objects.get(id=self.tournamentRoundId)
        except (TournamentRound.DoesNotExist):
            print ('Failed to get tournament round')
            print (self.tournamentRoundId)
            return False
        try:
            rounds = Round.objects.filter(tournament_round=tr.id)
        except (Round.DoesNotExist):
            print ('there are not any rounds for this tournament_round')
            print (tr.id)
            return newPlayerResultList
        if (len(rounds) == 0):
            return newPlayerResultList
        for round in rounds:
            score = {}
            score['clubMemberNumber'] = round.player.club_member_number
            score['playerName'] = round.player.name
            score['handicapIndex'] = round.handicap_index
            score['courseTeeId'] = round.course_tee.id
            score['courseHCP'] = round.course_handicap
            score['totalOut'] = round.total_out
            score['totalIn'] = round.total_in
            score['total'] = round.total
            score['totalNet'] = round.net
            for i in range(18):
                ss = Score.objects.filter(round=round.id, tee__hole__number=int(i+1)).values()[0]
                score['hole'+str(i)] = ss['score']
            resultList.append(score)
        print ('resultList')
        print (resultList)
        for score in newPlayerResultList:
            nfound = True
            for result in resultList:
                if (result['clubMemberNumber'] == score['clubMemberNumber']):
                    nfound = False
                    result['playerName'] = score['playerName']
                    result['handicapIndex'] = score['handicapIndex']
                    result['courseTeeId'] = score['courseTeeId']
                    result['courseHCP'] = score['courseHandicap']
                    result['totalOut'] = score['totalOut']
                    result['totalIn'] = score['totalIn']
                    result['total'] = score['total']
                    result['totalNet'] = score['totalNet']
                    for i in range(18):
                        result['hole'+str(i)] = score.score['hole'+str(i)]
                    pass
            if (nfound):
                resultList.append(score)
        return resultList

    def updateTournament(self, currentTournamentResults):
        """
            Sets the current tournament values in the database
            return True for success and False for fail
            TODO: Probably should say how many where updated.
        """
        for player in currentTournamentResults:
            try:
                p = Player.objects.get(club_member_number=player['clubMemberNumber'])
            except (Player.DoesNotExist):
                print ('Get player failed');
                print (player['clubMemberNumber'])
                return False
            try:
                tr = TournamentRound.objects.get(id=self.tournamentRoundId)
            except (TournamentRound.DoesNotExist):
                print ('Get TournamentRound failed')
                print (self.tournamentRoundId)
                return False
            try:
                sc = Scorecard.objects.get(id=self.scorecardId)
            except (Scorecard.DoesNotExist):
                print ('Get Scorecard failed')
                print (self.scorecardId)
                return False
            try:
                ct = CourseTee.objects.get(id=player['courseTeeId'])
            except (CourseTee.DoesNotExist):
                print ('Get CourseTee failed')
                print (player['courseTeeId'])
                return False
            try:
                r = Round.objects.get(tournament_round=tr.id, player=p)
                r.scorecard = sc
                r.course_tee = ct
                r.handicap_index = player['handicapIndex']
                r.course_handicap = player['courseHCP']
                r.total_out = player['totalOut']
                r.total_out_style = player['totalOutStyle']
                r.total_out_net = player['totalOutNet']
                r.total_out_net_style = player['totalOutNetStyle']
                r.total_in = player['totalIn']
                r.total_in_style = player['totalInStyle']
                r.total_in_net = player['totalInNet']
                r.total_in_net_style = player['totalInNetStyle']
                r.total = player['total']
                r.total_style = player['totalStyle']
                r.net = player['totalNet']
                r.net_style = player['totalNetStyle']
                r.save()
            except (Round.DoesNotExist):
                #Create the round because it doesn't exist
                r = Round(tournament_round=tr, player=p, scorecard=sc, course_tee=ct, handicap_index=player['handicapIndex'], course_handicap=player['courseHCP'], total_out=player['totalOut'], total_out_style=player['totalOutStyle'], total_out_net=player['totalOutNet'], total_out_net_style=player['totalOutNetStyle'], total_in=player['totalIn'], total_in_style=player['totalInStyle'], total_in_net=player['totalInNet'], total_in_net_style=player['totalInNetStyle'], total=player['total'], total_style=player['totalStyle'], net=player['totalNet'], net_style=player['totalNetStyle'])
                r.save()
            except:
                print ('Get Round failed')
                print (self.tournamentDateId)
                return False
            for i in range (18):
                try:
                    te = Tee.objects.get(course_tee=player['courseTeeId'], hole__number=int(i+1))
                except (Tee.DoesNotExist):
                    print ('Get Tee failed')
                    print (player['courseTeeId'])
                    print (int(i+1))
                    return False
                try:
                    s = Score.objects.get(tee=te.id, round=r)
                    s.tee = te
                    s.score = player['grossScores'][i]
                    s.score_style = player['grossStyles'][i]
                    s.score_net = player['netScores'][i]
                    s.score_net_style = player['netStyles'][i]
                    s.save()
                except Score.DoesNotExist:
                    s = Score(round=r, tee=te, score=player['grossScores'][i], score_style=player['grossStyles'][i], score_net=player['netScores'][i], score_net_style=player['netStyles'][i])
                    s.save()
                except:
                    print ('Get Score failed')
                    print (te.id)
                    return False
        return True

    def getCourseTeeById(self, teeId):
        """
            get the course tee for the tee id played
        """
        resultList = list(Tee.objects.filter(course_tee__id=teeId).values('id', 'yardage', 'par', 'handicap', 'hole__id', 'hole__number'))
        return resultList

    def calculatePayout(self, output, data):
        """
            Based on all scores from each player, what is the 'value' of this hole for an individual player
            Needs to return a json that will represent the
        """
        return