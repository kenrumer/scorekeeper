from abc import ABCMeta, abstractmethod
from .models import Player, Club, Tee, Round, Score
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

    def mergePlayers(self, new_player_list):
        pl = self.player_list
        for new_player in new_player_list:
            found = False
            for i in range(len(pl)):
                if (int(pl[i]['club_member_number']) == int(new_player['club_member_number'])):
                    found = True
                    pl[i]['name'] = new_player['name']
                    pl[i]['handicap_index'] = new_player['handicap_index']
                    pl[i]['data'] = new_player['data']
                    pl[i]['player_type__id'] = new_player['player_type__id']
                    if (float(pl[i]['high_handicap_index']) < float(new_player['handicap_index'])):
                        pl[i]['high_handicap_index'] = new_player['handicap_index']
                    if (float(pl[i]['low_handicap_index']) > float(new_player['handicap_index'])):
                        pl[i]['low_handicap_index'] = new_player['handicap_index']
                    continue
            if (found == False):
                pl.append({'id':-1, 'club_member_number':new_player['club_member_number'], 'name':new_player['name'], 'handicap_index':new_player['handicap_index'], 'player_type__id':1, 'data':new_player['data'], 'high_handicap_index':new_player['handicap_index'], 'low_handicap_index':new_player['handicap_index']})
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

    @abstractmethod
    def calculateScores(self, input):
        return

    def mergePlayerResults(self, tournament_id, new_player_results_list):
        try:
            resultList = list(Score.objects.filter(round__tournament__id=tournament_id).values('score', 'score_style', 'score_net', 'score_net_style', 'round__handicap_index', 'round__course_handicap', 'round__total_out', 'round__total_out_style', 'round__total_out_net', 'round__total_out_net_style', 'round__total_in', 'round__total_in_style', 'round__total_in_net', 'round__total_in_net_style', 'round__total', 'round__total_style', 'round__net', 'round__net_style', 'round__player__club_member_number'))
        except (Round.DoesNotExist):
            resultList = []
        for result in new_player_results_list:
        return
        return resultList

    def updateTournament(self, tournament_id, current_tournament_results):
        return

    def getCourseTeeById(self, tee_id):
        resultList = list(Tee.objects.filter(course_tee__id=tee_id).values('id', 'yardage', 'par', 'handicap', hole__number'))
        return resultList

    def calculatePayout(self, output, data):
        """
            Based on all scores from each player, what is the 'value' of this hole for an individual player
            Needs to return a json that will represent the
        """
        return