from abc import ABCMeta, abstractmethod
from .models import Player, Club, CourseTee, Tee, Round, Score, Tournament, TournamentRound, Scorecard
from django.utils import timezone
from datetime import datetime
import json

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
        a = datetime.now()
        pl = self.player_list
        for newPlayer in newPlayerList:
            found = False
            for i in range(len(pl)):
                if (int(pl[i]['club_member_number']) == int(newPlayer['club_member_number'])):
                    found = True
                    pl[i]['name'] = newPlayer['name']
                    pl[i]['handicap_index'] = newPlayer['handicap_index']
                    if (newPlayer['handicap_index'] == ''):
                        newPlayer['handicap_index'] = 1.0
                        pl[i]['high_handicap_index'] = 1.0
                        pl[i]['low_handicap_index'] = 36.0
                    else:
                        if (float(pl[i]['high_handicap_index']) < float(newPlayer['handicap_index'])):
                            pl[i]['high_handicap_index'] = newPlayer['handicap_index']
                        if (float(pl[i]['low_handicap_index']) > float(newPlayer['handicap_index'])):
                            pl[i]['low_handicap_index'] = newPlayer['handicap_index']
                    continue
            if (found == False):
                if (newPlayer['handicap_index'] == ''):
                    newPlayer['handicap_index'] = 1.0
                    newPlayer['high_handicap_index'] = 1.0
                    newPlayer['low_handicap_index'] = 36.0
                    #print(newPlayer)
                    pl.append({'id':-1, 'club_member_number':newPlayer['club_member_number'], 'name':newPlayer['name'], 'handicap_index':newPlayer['handicap_index'], 'data':newPlayer['data'], 'high_handicap_index':newPlayer['high_handicap_index'], 'low_handicap_index':newPlayer['low_handicap_index']})
                else:
                    #print(newPlayer)
                    pl.append({'id':-1, 'club_member_number':newPlayer['club_member_number'], 'name':newPlayer['name'], 'handicap_index':newPlayer['handicap_index'], 'data':newPlayer['data'], 'high_handicap_index':newPlayer['handicap_index'], 'low_handicap_index':newPlayer['handicap_index']})
        self.player_list = pl
        c = datetime.now() - a
        print('mergePlayers time: '+str(c.seconds))

    def storePlayers(self):
        a = datetime.now()
        pl = self.player_list
        c = Club.objects.get(id=self.club['id'])
        c.players_last_updated = timezone.now()
        c.save()
        for player in pl:
            if (player['high_handicap_index'] == ''):
                player['high_handicap_index'] = player['handicap_index']
            if (player['low_handicap_index'] == ''):
                player['low_handicap_index'] = player['handicap_index']
            if (player['id'] != -1):
                p = Player.objects.get(id=player['id'])
                p.club_member_number=player['club_member_number']
                p.name=player['name']
                p.handicap_index=player['handicap_index']
                p.data=player['data']
                p.high_handicap_index=player['high_handicap_index']
                p.low_handicap_index=player['low_handicap_index']
                p.last_updated=timezone.now()
                p.club_id=1
                p.save()
            else:
                p = Player(club=1, club_member_number=player['club_member_number'], name=player['name'], handicap_index=player['handicap_index'], data=player['data'], high_handicap_index=player['high_handicap_index'], low_handicap_index=player['low_handicap_index'], last_updated=timezone.now())
                p.save()
        c = datetime.now() - a
        print('storePlayers time: '+str(c.seconds))

class FormatBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, tournamentId, tournamentRoundId):
        self.tournamentId = tournamentId
        self.tournamentRoundId = tournamentRoundId
        pass

    @abstractmethod
    def updateScores(self, scores):
        return

    @abstractmethod
    def showPayout(self):
        """
            Needs to be implemented by the plugin to show the dollars per person for the tournament.
            Giving free reign to the plugin at this point. Plugin should have stored most things in payout table in data column.
            Use getPayoutData to get what the plugin has stored before.
        """
        print('showPayout?')
        return

    def mergePlayerResults(self, newPlayerResultList):
        """
        Merges the existing players from the database with the new players
        TODO: Need to return response time
        """
        a = datetime.now()
        playerResultList = []
        try:
            rounds = Round.objects.filter(tournament_round=self.tournamentRoundId)
        except (Round.DoesNotExist):
            print ('there are not any rounds for this tournament_round')
            print (self.tournamentRoundId)
            return newPlayerResultList

        if (len(rounds) == 0):
            return newPlayerResultList
            
        #TODO: Normalizing when I don't need to...
        for round in rounds:
            player = {}
            player['clubMemberNumber'] = round.player.club_member_number
            player['playerName'] = round.player.name
            player['handicapIndex'] = round.handicap_index
            player['scorecardId'] = round.scorecard.id
            player['round'] = {}
            player['round']['courseTeeId'] = round.course_tee.id
            player['round']['courseHCP'] = round.course_handicap
            player['round']['totalOut'] = round.total_out
            player['round']['totalIn'] = round.total_in
            player['round']['total'] = round.total
            player['round']['totalNet'] = round.net
            player['round']['score'] = {}
            for i in range(18):
                ss = Score.objects.filter(round=round.id, tee__hole__number=int(i+1)).values()[0]
                player['round']['score']['hole'+str(i)] = ss['score']
            playerResultList.append(player)
        for player in newPlayerResultList:
            nfound = True
            for result in playerResultList:
                if (result['clubMemberNumber'] == player['clubMemberNumber']):
                    nfound = False
                    result['playerName'] = player['playerName']
                    result['handicapIndex'] = player['handicapIndex']
                    result['round'] = {}
                    result['round']['courseTeeId'] = player['round']['courseTeeId']
                    result['round']['courseHCP'] = player['round']['courseHandicap']
                    result['round']['totalOut'] = player['round']['totalOut']
                    result['round']['totalIn'] = player['round']['totalIn']
                    result['round']['total'] = player['round']['total']
                    result['round']['totalNet'] = player['round']['totalNet']
                    result['round']['score'] = {}
                    for i in range(18):
                        result['score']['hole'+str(i)] = player.score['hole'+str(i)]
                    pass
            if (nfound):
                playerResultList.append(player)
        c = datetime.now() - a
        print('mergePlayerResults time: '+str(c.seconds))
        return playerResultList

    def updateTournament(self, playerResultList):
        """
            Sets the current tournament values in the database
            return True for success and False for fail
            TODO: Probably should say how many where updated.
            TODO: Return response time
        """
        a = datetime.now()
        try:
            tr = TournamentRound.objects.get(id=self.tournamentRoundId)
        except:
            print('Failed to get the tournament round')
            print(self.tournamentRoundId)
            return False
        for player in playerResultList:
            try:
                p = Player.objects.get(club_member_number=player['clubMemberNumber'])
            except (Player.DoesNotExist):
                print ('Get player failed');
                print (player['clubMemberNumber'])
                return False
            try:
                sc = Scorecard.objects.get(id=player['scorecardId'])
            except (Scorecard.DoesNotExist):
                print ('Get Scorecard failed')
                print (player['scorecardId'])
                return False
            try:
                ct = CourseTee.objects.get(id=player['round']['courseTeeId'])
            except (CourseTee.DoesNotExist):
                print ('Get CourseTee failed')
                print (player['round']['courseTeeId'])
                return False
            try:
                r = Round.objects.get(tournament_round=tr, player=p)
                r.scorecard = sc
                r.course_tee = ct
                r.handicap_index = player['handicapIndex']
                r.course_handicap = player['round']['courseHCP']
                r.total_out = player['round']['totalOut']
                r.total_out_style = player['round']['totalOutStyle']
                r.total_out_net = player['round']['totalOutNet']
                r.total_out_net_style = player['round']['totalOutNetStyle']
                r.total_in = player['round']['totalIn']
                r.total_in_style = player['round']['totalInStyle']
                r.total_in_net = player['round']['totalInNet']
                r.total_in_net_style = player['round']['totalInNetStyle']
                r.total = player['round']['total']
                r.total_style = player['round']['totalStyle']
                r.net = player['round']['totalNet']
                r.net_style = player['round']['totalNetStyle']
                r.save()
            except (Round.DoesNotExist):
                #Create the round because it doesn't exist
                r = Round(tournament_round=tr, player=p, scorecard=sc, course_tee=ct, handicap_index=player['handicapIndex'], course_handicap=player['round']['courseHCP'], total_out=player['round']['totalOut'], total_out_style=player['round']['totalOutStyle'], total_out_net=player['round']['totalOutNet'], total_out_net_style=player['round']['totalOutNetStyle'], total_in=player['round']['totalIn'], total_in_style=player['round']['totalInStyle'], total_in_net=player['round']['totalInNet'], total_in_net_style=player['round']['totalInNetStyle'], total=player['round']['total'], total_style=player['round']['totalStyle'], net=player['round']['totalNet'], net_style=player['round']['totalNetStyle'])
                r.save()
            #except:
            #    print ('Get Round failed')
            #    print (self.tournamentRoundId)
            #    return False
            for i in range (18):
                try:
                    te = Tee.objects.get(course_tee=player['round']['courseTeeId'], hole__number=int(i+1))
                except (Tee.DoesNotExist):
                    print ('Get Tee failed')
                    print (player['round']['courseTeeId'])
                    print (int(i+1))
                    return False
                try:
                    s = Score.objects.get(tee=te.id, round=r)
                    s.tee = te
                    s.score = player['round']['grossScores'][i]
                    s.score_style = player['round']['grossStyles'][i]
                    s.skin = player['round']['grossSkins'][i]
                    s.score_net = player['round']['netScores'][i]
                    s.score_net_style = player['round']['netStyles'][i]
                    s.skin_net = player['round']['netSkins'][i]
                    s.save()
                except Score.DoesNotExist:
                    s = Score(round=r, tee=te, score=player['round']['grossScores'][i], score_style=player['round']['grossStyles'][i], skin=player['round']['grossSkins'][i], score_net=player['round']['netScores'][i], score_net_style=player['round']['netStyles'][i], skin_net=player['round']['netSkins'][i])
                    s.save()
                except:
                    print ('Get Score failed')
                    print (te.id)
                    return False
        c = datetime.now() - a
        print('updateTournament time: '+str(c.seconds))
        return True

    def getCourseTeeById(self, teeId):
        """
            get the course tee for the tee id played
        """
        resultList = list(Tee.objects.filter(course_tee__id=teeId).values('id', 'yardage', 'par', 'handicap', 'hole__id', 'hole__number'))
        return resultList

    def getFormatData(self):
        """
            get the format data for the tournament round
        """
        resultList = list(TournamentRound.objects.filter(id=self.tournamentRoundId).values('id', 'data'))[0]
        return resultList

    def getPlayerData(self):
        """
            get the data for the payout of the tournament
        """
        players = []
        netPlayers = []
        try:
            rounds = Round.objects.filter(tournament_round=self.tournamentRoundId).order_by('total')
            netRounds = Round.objects.filter(tournament_round=self.tournamentRoundId).order_by('net')
        except:
            print ('Failed to get rounds')
            print (self.tournamentRoundId)
            return False
        i = 1
        for r in rounds:
            try:
                s = Score.objects.filter(round=r.id).order_by('tee__hole__number')
            except:
                print ('Failed to get scores')
                print (r.id)
                return False
            player = {}
            player['name'] = r.player.name
            player['course_handicap'] = r.course_handicap
            player['rank'] = i
            player['total_out'] = r.total_out
            player['total_in'] = r.total_in
            player['total'] = r.total
            player['scores'] = []
            player['skins'] = []
            for index, item in enumerate(s):
                player['scores'].append(item.score)
                player['skins'].append(item.skin)
            i += 1
            players.append(player)
        for r in netRounds:
            try:
                s = Score.objects.filter(round=r.id).order_by('tee__hole__number')
            except:
                print ('Failed to get scores')
                print (r.id)
                return False
            player = {}
            player['name'] = r.player.name
            player['course_handicap'] = r.course_handicap
            player['rank'] = i
            player['total_out_net'] = r.total_out_net
            player['total_in_net'] = r.total_in_net
            player['net'] = r.net
            player['scores'] = []
            player['skins'] = []
            for index, item in enumerate(s):
                player['scores'].append(item.score_net)
                player['skins'].append(item.skin_net)
            i += 1
            netPlayers.append(player)
        return json.dumps({ 'players': players, 'netPlayers': netPlayers })

    def getPayoutPercents(self, count, height, bend):
        """
            get a list of payout percentages based on a curved algorithm
            needs total players, height (percentage of players paid), bend (integer representing the depth of the curve.  0 is linear)
        """
        payoutCount = int(count*height/100);
        
        payoutList = []
        payoutTextList = []
        if (payoutCount <= 1):
            payoutCount = 1
            payoutList = [100]
            payoutTextList = ['First']
        if (payoutCount == 2):
            payoutList = [75,25]
            payoutTextList = ['First','Second']
        if (payoutCount == 3):
            payoutList = [43,33,24]
            payoutTextList = ['First','Second','Third']
        if (payoutCount == 4):
            payoutList = [40,30,20,10]
            payoutTextList = ['First','Second','Third','Forth']
        if (payoutCount == 5):
            payoutList = [30,25,20,15,10]
            payoutTextList = ['First','Second','Third','Forth','Fifth']
        if (payoutCount == 6):
            payoutList = [25,21,18,15,12,9]
            payoutTextList = ['First','Second','Third','Forth','Fifth','Sixth']
        if (payoutCount == 7):
            payoutList = [23,19,16,14,12,10,6]
            payoutTextList = ['First','Second','Third','Forth','Fifth','Sixth','Seventh']
        return json.dumps({'payoutCount':payoutCount, 'payoutList':payoutList, 'payoutTextList':payoutTextList})