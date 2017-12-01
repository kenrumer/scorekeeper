from ..abc_base import FormatBase
import json
import math
from datetime import datetime

"""
    Class for calculating player gross and net scores in a skins and pins tournament
    In order to help calculate netScores, call courseTee = super().getCourseTeeById(teeId)
        also call super().getTournamentStandings(tournamentId) for the latest tournament results
    You can use it or call updatedTournamentStandings = super().mergePlayerResults(tournamentId, newPlayerResultsList)
        the newPlayerResultsList param in mergePlayers is [{clubMemberNumber:clubMemberNumber, teeId:teeId, grossScores:[grossScores], netScores:[netScores]}]
        the returned updatedTournamentStandings will have the same format, but include all scored players so you can set the styles
    You also need to call super().updateTournament(updatedTournamentStandings) in order to update the database
        updatedTournamentStandings has the format:
        [{clubMemberNumber:clubMemberNumber, teeId:teeId, grossScores:[grossScores], grossStyles:[grossStyles], netScores:[netScores], netStyles:[netStyles]}]
        and will write the database so the tournament tables can be drawn with the background colors for low net/skins
"""
class SkinsAndPinsFormat(FormatBase):

    def __init__(self, tournamentId, tournamentRoundId):
        super().__init__(tournamentId, tournamentRoundId)
        pass

    def updateScores(self, players):
        """
            Based on all scores from each player (on save from scorecard), what is the 'value' (store raw && net && cell style in the score table, assign score to player, round and scorecard)
            Retrieve players from the input (this saved scorecard) source and return an object.
            scores = '[{"clubMemberNumber":"12345","playerName":"Doe, John","hcpIndex":"25.7","teeId":7,"courseHCP":20,"hole0":4,"hole1":3,"hole2":3,"hole3":3,"hole4":4,"hole5":4,"hole6":3,"hole7":3,"hole8":3,"totalOut":30,"hole9":3,"hole10":3,"hole11":3,"hole12":4,"hole13":4,"hole14":3,"hole15":4,"hole16":3,"hole17":3,"totalIn":30,"total":60,"totalnet":40}]'
            tournamentId = '55'
        """
        a = datetime.now()
        print('players')
        print (players)
        updatedTournamentPlayers = super().mergePlayerResults(players)
        print('updatedTournamentPlayers')
        print (updatedTournamentPlayers)
        lowestTotalGrossCount = 0
        lowestTotalNetCount = 0
        lowestTotalOutCount = 0
        lowestTotalOutNetCount = 0
        lowestTotalInCount = 0
        lowestTotalInNetCount = 0
        for player in updatedTournamentPlayers:
            courseTee = super().getCourseTeeById(player['round']['courseTeeId'])
            totHcp = math.floor(player['round']['courseHCP']/2)
            player['round']['grossScores'] = []
            player['round']['netScores'] = []
            player['round']['grossStyles'] = []
            player['round']['netStyles'] = []
            player['round']['grossSkins'] = []
            player['round']['netSkins'] = []
            lowestTotalGross = 1000
            lowestTotalNet = 1000
            lowestTotalOut = 1000
            lowestTotalOutNet = 1000
            lowestTotalIn = 1000
            lowestTotalInNet = 1000
            for i in range(18):
                player['round']['grossScores'].append(player['round']['score']['hole'+str(i)])
                if (courseTee[i]['handicap'] <= totHcp):
                    player['round']['netScores'].append(int(player['round']['score']['hole'+str(i)]) - 1)
                else:
                    player['round']['netScores'].append(player['round']['score']['hole'+str(i)])
            player['round']['totalOutNet'] = math.ceil(player['round']['totalOut'] - (player['round']['courseHCP']/2))
            player['round']['totalInNet'] = math.floor(player['round']['totalIn'] - (player['round']['courseHCP']/2))
            if (player['round']['total'] == lowestTotalGross):
                lowestTotalGrossCount += 1
            if (player['round']['total'] < lowestTotalGross):
                lowestTotalGrossCount = 1
                lowestTotalGross = player['round']['total']
                
            if (player['round']['totalNet'] == lowestTotalNet):
                lowestTotalNetCount += 1
            if (player['round']['totalNet'] < lowestTotalNet):
                lowestTotalNetCount = 1
                lowestTotalNet = player['round']['totalNet']
                
            if (player['round']['totalOut'] == lowestTotalOut):
                lowestTotalOutCount += 1
            if (player['round']['totalOut'] < lowestTotalOut):
                lowestTotalOutCount = 1
                lowestTotalOut = player['round']['totalOut']
                
            if (player['round']['totalOutNet'] == lowestTotalOutNet):
                lowestTotalOutNetCount += 1
            if (player['round']['totalOutNet'] < lowestTotalOutNet):
                lowestTotalOutNetCount = 1
                lowestTotalOutNet = player['round']['totalOutNet']
                
            if (player['round']['totalIn'] == lowestTotalIn):
                lowestTotalInCount += 1
            if (player['round']['totalIn'] < lowestTotalIn):
                lowestTotalInCount = 1
                lowestTotalIn = player['round']['totalIn']
                
            if (player['round']['totalInNet'] == lowestTotalInNet):
                lowestTotalInNetCount += 1
            if (player['round']['totalInNet'] < lowestTotalInNet):
                lowestTotalInNetCount = 1
                lowestTotalInNet = player['round']['totalInNet']

        for player in updatedTournamentPlayers:
            if (lowestTotalGrossCount == 1):
                if (player['round']['total'] == lowestTotalGross):
                    player['round']['totalStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalStyle'] = ''
            else:
                if (player['round']['total'] == lowestTotalGross):
                    player['round']['totalStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalStyle'] = ''
                
            if (lowestTotalNetCount == 1):
                if (player['round']['totalNet'] == lowestTotalNet):
                    player['round']['totalNetStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalNetStyle'] = ''
            else:
                if (player['round']['totalNet'] == lowestTotalNet):
                    player['round']['totalNetStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalNetStyle'] = ''
                
            if (lowestTotalOutCount == 1):
                if (player['round']['totalOut'] == lowestTotalOut):
                    player['round']['totalOutStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalOutStyle'] = ''
            else:
                if (player['round']['totalOut'] == lowestTotalOut):
                    player['round']['totalOutStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalOutStyle'] = ''
                    
            if (lowestTotalOutNetCount == 1):
                if (player['round']['totalOutNet'] == lowestTotalOutNet):
                    player['round']['totalOutNetStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalOutNetStyle'] = ''
            else:
                if (player['round']['totalOutNet'] == lowestTotalOutNet):
                    player['round']['totalOutNetStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalOutNetStyle'] = ''
                
            if (lowestTotalInCount == 1):
                if (player['round']['totalIn'] == lowestTotalIn):
                    player['round']['totalInStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalInStyle'] = ''
            else:
                if (player['round']['totalIn'] == lowestTotalIn):
                    player['round']['totalInStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalInStyle'] = ''
                
            if (lowestTotalInNetCount == 1):
                if (player['round']['totalInNet'] == lowestTotalInNet):
                    player['round']['totalInNetStyle'] = 'background-color:greenyellow'
                else:
                    player['round']['totalInNetStyle'] = ''
            else:
                if (player['round']['totalInNet'] == lowestTotalInNet):
                    player['round']['totalInNetStyle'] = 'background-color:LightGray'
                else:
                    player['round']['totalInNetStyle'] = ''

        for i in range(18):
            lowestGross = 1000
            lowestNet = 1000
            lowestGrossCount = 0
            lowestNetCount = 0
            for player in updatedTournamentPlayers:

                if (player['round']['grossScores'][i] == lowestGross):
                    lowestGrossCount += 1
                if (player['round']['grossScores'][i] < lowestGross):
                    lowestGrossCount = 1
                    lowestGross = player['round']['grossScores'][i]

                if (player['round']['netScores'][i] == lowestNet):
                    lowestNetCount += 1
                if (player['round']['netScores'][i] < lowestNet):
                    lowestNetCount = 1
                    lowestNet = player['round']['netScores'][i]

            for player in updatedTournamentPlayers:
                if (lowestGrossCount == 1):
                    if (player['round']['grossScores'][i] == lowestGross):
                        player['round']['grossStyles'].append('background-color:greenyellow')
                        player['round']['grossSkins'].append(1)
                    else:
                        player['round']['grossStyles'].append('')
                        player['round']['grossSkins'].append(0)
                        player['round']['grossStyles'].append('background-color:yellow')
                    if (player['round']['grossScores'][i] == lowestGross):
                        player['round']['grossStyles'].append('background-color:LightGray')
                        player['round']['grossSkins'].append(0)
                    else:
                        player['round']['grossStyles'].append('')
                        player['round']['grossSkins'].append(0)

                if (lowestNetCount == 1):
                    if (player['round']['netScores'][i] == lowestNet):
                        player['round']['netStyles'].append('background-color:greenyellow')
                        player['round']['netSkins'].append(1)
                    else:
                        player['round']['netStyles'].append('')
                        player['round']['netSkins'].append(0)
                else:
                    if (player['round']['netScores'][i] == lowestNet):
                        player['round']['netStyles'].append('background-color:LightGray')
                        player['round']['netSkins'].append(0)
                    else:
                        player['round']['netStyles'].append('')
                        player['round']['netSkins'].append(0)

        c = datetime.now() - a
        print('updateScores time: '+str(c.seconds))
        super().updateTournament(updatedTournamentPlayers)
        return True
    