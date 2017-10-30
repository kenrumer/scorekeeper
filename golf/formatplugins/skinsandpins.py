from ..abc_base import FormatBase
import json
import math

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

    def __init__(self, tournamentId, tournamentRoundId, scorecardId):
        super().__init__(tournamentId, tournamentRoundId, scorecardId)
        pass

    def updateScores(self, request):
        """
            Based on all scores from each player (on save from scorecard), what is the 'value' (store raw && net && cell style in the score table, assign score to player, round and scorecard)
            Retrieve players from the input (this saved scorecard) source and return an object.
            scores = '[{"clubMemberNumber":"12345","playerName":"Doe, John","hcpIndex":"25.7","teeId":7,"courseHCP":20,"hole0":4,"hole1":3,"hole2":3,"hole3":3,"hole4":4,"hole5":4,"hole6":3,"hole7":3,"hole8":3,"totalOut":30,"hole9":3,"hole10":3,"hole11":3,"hole12":4,"hole13":4,"hole14":3,"hole15":4,"hole16":3,"hole17":3,"totalIn":30,"total":60,"totalnet":40}]'
            tournamentId = '55'
        """
        scores = json.loads(request['scores'])
        print (scores)
        updatedTournamentStandings = super().mergePlayerResults(scores)
        print('updatedTournamentStandings')
        print (updatedTournamentStandings)
        lowestTotalGrossCount = 0
        lowestTotalNetCount = 0
        lowestTotalOutCount = 0
        lowestTotalOutNetCount = 0
        lowestTotalInCount = 0
        lowestTotalInNetCount = 0
        for standing in updatedTournamentStandings:
            courseTee = super().getCourseTeeById(standing['courseTeeId'])
            totHcp = math.floor(standing['courseHCP']/2)
            standing['grossScores'] = []
            standing['netScores'] = []
            standing['grossStyles'] = []
            standing['netStyles'] = []
            standing['grossSkins'] = []
            standing['netSkins'] = []
            lowestTotalGross = 1000
            lowestTotalNet = 1000
            lowestTotalOut = 1000
            lowestTotalOutNet = 1000
            lowestTotalIn = 1000
            lowestTotalInNet = 1000
            for i in range(18):
                standing['grossScores'].append(standing['hole'+str(i)])
                if (courseTee[i]['handicap'] <= totHcp):
                    standing['netScores'].append(int(standing['hole'+str(i)]) - 1)
                else:
                    standing['netScores'].append(standing['hole'+str(i)])
            standing['totalOutNet'] = math.ceil(standing['totalOut'] - (standing['courseHCP']/2))
            standing['totalInNet'] = math.floor(standing['totalIn'] - (standing['courseHCP']/2))
            if (standing['total'] == lowestTotalGross):
                lowestTotalGrossCount += 1
            if (standing['total'] < lowestTotalGross):
                lowestTotalGrossCount = 1
                lowestTotalGross = standing['total']
                
            if (standing['totalNet'] == lowestTotalNet):
                lowestTotalNetCount += 1
            if (standing['totalNet'] < lowestTotalNet):
                lowestTotalNetCount = 1
                lowestTotalNet = standing['totalNet']
                
            if (standing['totalOut'] == lowestTotalOut):
                lowestTotalOutCount += 1
            if (standing['totalOut'] < lowestTotalOut):
                lowestTotalOutCount = 1
                lowestTotalOut = standing['totalOut']
                
            if (standing['totalOutNet'] == lowestTotalOutNet):
                lowestTotalOutNetCount += 1
            if (standing['totalOutNet'] < lowestTotalOutNet):
                lowestTotalOutNetCount = 1
                lowestTotalOutNet = standing['totalOutNet']
                
            if (standing['totalIn'] == lowestTotalIn):
                lowestTotalInCount += 1
            if (standing['totalIn'] < lowestTotalIn):
                lowestTotalInCount = 1
                lowestTotalIn = standing['totalIn']
                
            if (standing['totalInNet'] == lowestTotalInNet):
                lowestTotalInNetCount += 1
            if (standing['totalInNet'] < lowestTotalInNet):
                lowestTotalInNetCount = 1
                lowestTotalInNet = standing['totalInNet']

        for standing in updatedTournamentStandings:
            if (lowestTotalGrossCount == 1):
                if (standing['total'] == lowestTotalGross):
                    standing['totalStyle'] = 'background-color:#eee'
                else:
                    standing['totalStyle'] = ''
            else:
                if (standing['total'] == lowestTotalGross):
                    standing['totalStyle'] = 'background-color:#ccc'
                else:
                    standing['totalStyle'] = ''
                
            if (lowestTotalNetCount == 1):
                if (standing['totalNet'] == lowestTotalNet):
                    standing['totalNetStyle'] = 'background-color:#eee'
                else:
                    standing['totalNetStyle'] = ''
            else:
                if (standing['totalNet'] == lowestTotalNet):
                    standing['totalNetStyle'] = 'background-color:#ccc'
                else:
                    standing['totalNetStyle'] = ''
                
            if (lowestTotalOutCount == 1):
                if (standing['totalOut'] == lowestTotalOut):
                    standing['totalOutStyle'] = 'background-color:#eee'
                else:
                    standing['totalOutStyle'] = ''
            else:
                if (standing['totalOut'] == lowestTotalOut):
                    standing['totalOutStyle'] = 'background-color:#ccc'
                else:
                    standing['totalOutStyle'] = ''
                    
            if (lowestTotalOutNetCount == 1):
                if (standing['totalOutNet'] == lowestTotalOutNet):
                    standing['totalOutNetStyle'] = 'background-color:#eee'
                else:
                    standing['totalOutNetStyle'] = ''
            else:
                if (standing['totalOutNet'] == lowestTotalOutNet):
                    standing['totalOutNetStyle'] = 'background-color:#ccc'
                else:
                    standing['totalOutNetStyle'] = ''
                
            if (lowestTotalInCount == 1):
                if (standing['totalIn'] == lowestTotalIn):
                    standing['totalInStyle'] = 'background-color:#eee'
                else:
                    standing['totalInStyle'] = ''
            else:
                if (standing['totalIn'] == lowestTotalIn):
                    standing['totalInStyle'] = 'background-color:#ccc'
                else:
                    standing['totalInStyle'] = ''
                
            if (lowestTotalInNetCount == 1):
                if (standing['totalInNet'] == lowestTotalInNet):
                    standing['totalInNetStyle'] = 'background-color:#eee'
                else:
                    standing['totalInNetStyle'] = ''
            else:
                if (standing['totalInNet'] == lowestTotalInNet):
                    standing['totalInNetStyle'] = 'background-color:#ccc'
                else:
                    standing['totalInNetStyle'] = ''

        for i in range(18):
            lowestGross = 1000
            lowestNet = 1000
            lowestGrossCount = 0
            lowestNetCount = 0
            for standing in updatedTournamentStandings:

                if (standing['grossScores'][i] == lowestGross):
                    lowestGrossCount += 1
                if (standing['grossScores'][i] < lowestGross):
                    lowestGrossCount = 1
                    lowestGross = standing['grossScores'][i]

                if (standing['netScores'][i] == lowestNet):
                    lowestNetCount += 1
                if (standing['netScores'][i] < lowestNet):
                    lowestNetCount = 1
                    lowestNet = standing['netScores'][i]

            for standing in updatedTournamentStandings:
                if (lowestGrossCount == 1):
                    if (standing['grossScores'][i] == lowestGross):
                        standing['grossStyles'].append('background-color:#eee;')
                        standing['grossSkins'].append(1)
                    else:
                        standing['grossStyles'].append('')
                        standing['grossSkins'].append(0)
                else:
                    if (standing['grossScores'][i] == lowestGross):
                        standing['grossStyles'].append('background-color:#ccc;')
                        standing['grossSkins'].append(0)
                    else:
                        standing['grossStyles'].append('')
                        standing['grossSkins'].append(0)

                if (lowestNetCount == 1):
                    if (standing['netScores'][i] == lowestNet):
                        standing['netStyles'].append('background-color:#eee;')
                        standing['netSkins'].append(1)
                    else:
                        standing['netStyles'].append('')
                        standing['netSkins'].append(0)
                else:
                    if (standing['netScores'][i] == lowestNet):
                        standing['netStyles'].append('background-color:#ccc;')
                        standing['netSkins'].append(0)
                    else:
                        standing['netStyles'].append('')
                        standing['netSkins'].append(0)

        super().updateTournament(updatedTournamentStandings)
        return True