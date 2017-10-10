from abc import ABCMeta, abstractmethod
from .models import Player, Club, Tee, Round, Score, Tournament, Scorecard
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

    def __init__(self, tournamentId, scorecardId):
        self.tournamentId = tournamentId
        self.scorecardId = scorecardId
        print (self.tournamentId)
        pass

    @abstractmethod
    def calculateScores(self, scores):
        return

    def mergePlayerResults(self, newPlayerResultList):
        resultList = []
        try:
            t = Tournament.objects.get(id=self.tournamentId)
        except (Tournament.DoesNotExist):
            return resultList
        try:
            roundList = list(Round.objects.filter(tournament=t.id).values('id'))
            for round in roundList:
                try:
                    resultList.append(list(Score.objects.filter(round=round['id']).values('score', 'score_style', 'score_net', 'score_net_style', 'round__handicap_index', 'round__course_handicap', 'round__total_out', 'round__total_out_style', 'round__total_out_net', 'round__total_out_net_style', 'round__total_in', 'round__total_in_style', 'round__total_in_net', 'round__total_in_net_style', 'round__total', 'round__total_style', 'round__net', 'round__net_style', 'round__player__club_member_number')))
                    print ('resultList')
                    print (resultList)
                except (Score.DoesNotExist):
                    pass
        except (Round.DoesNotExist):
            pass
        for result in newPlayerResultList:
            resultList.append(result)
        return resultList

    def updateTournament(self, currentTournamentResults):
        """
            Sets the current tournament values in the database
        """
        for player in currentTournamentResults:
            try:
                p = Player.objects.get(club_member_number=player['clubMemberNumber'])
            except (Player.DoesNotExist):
                return
            try:
                t = Tournament.objects.get(id=self.tournamentId)
            except (Tournament.DoesNotExist):
                return
            try:
                sc = Scorecard.objects.get(id=self.scorecardId)
            except (Scorecard.DoesNotExist):
                return
            try:
                r = Round.objects.get(tournament=t.id, player=p)
            except (Round.DoesNotExist):
                r = Round(tournament=t, player=p, scorecard=sc, handicap_index=player['handicapIndex'], course_handicap=player['courseHCP'], total_out=player['totalOut'], total_out_style=player['totalOutStyle'], total_out_net=player['totalOutNet'], total_out_net_style=player['totalOutNetStyle'], total_in=player['totalIn'], total_in_style=player['totalInStyle'], total_in_net=player['totalInNet'], total_in_net_style=player['totalInNetStyle'], total=player['total'], total_style=player['totalStyle'], net=player['totalNet'], net_style=player['totalNetStyle'])
                r.save()
            try:
                s = list(Score.objects.filter(round=r.id).values('score', 'score_style', 'score_net', 'score_net_style', 'round__handicap_index', 'round__course_handicap', 'round__total_out', 'round__total_out_style', 'round__total_out_net', 'round__total_out_net_style', 'round__total_in', 'round__total_in_style', 'round__total_in_net', 'round__total_in_net_style', 'round__total', 'round__total_style', 'round__net', 'round__net_style', 'round__player__club_member_number'))
            except (Score.DoesNotExist):
                for i in range(0,17):
                    s = Score(round=r, score=player['gross_scores'][i], score_style=player['gross_styles'][i], score_netscore=player['net_scores'][i], score_net_style=player['net_styles'][i])
                    s.save()
        return

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