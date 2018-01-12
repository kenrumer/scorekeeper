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
                else:
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

    def showPayout(self):
        formatData = json.loads(super().getFormatData())['data']
        print(formatData)
        playerData = json.loads(super().getPlayerData())
        playerCount = len(playerData['netPlayers'])
        html = ''
        html += '<div class="row">'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutPlayerCount">'
        html += '      Player Count'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <input type="number" min="0" max="1000" id="payoutBuyIn" value="'+str(playerCount)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutBuyIn">'
        html += '      BuyIn'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutBuyIn = int(formatData['payoutBuyIn'])
        html += '    <input type="number" min="0" max="1000" id="payoutBuyIn" value="'+str(payoutBuyIn)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutTotal">'
        html += '      Payout Total'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutTotal = payoutBuyIn*playerCount
        html += '    <input type="number" min="0" max="1000" id="payoutTotal" value="'+str(payoutTotal)+'" />'
        html += '  </div>'
        html += '</div>'
        html += '<div class="row">'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutClubDuesPercent">'
        html += '      Club Dues Percent'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutClubDuesPercent = int(formatData['payoutClubDuesPercent'])
        html += '    <input type="number" min="0" max="100" id="payoutClubDuesPercent" value="'+str(payoutClubDuesPercent)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutClubDues">'
        html += '      Club Dues'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutClubDues = int(payoutTotal * payoutClubDuesPercent / 100)
        html += '    <input type="number" min="0" max="1000" id="payoutClubDues" value="'+str(payoutClubDues)+'" disabled />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutProximityTotal">'
        html += '      Proximity Total'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutProximityTotal = int(formatData['payoutProximityTotal'])
        payoutProximityCount = int(formatData['payoutProximityCount'])
        payoutProximityPerTotal = int(payoutProximityTotal / payoutProximityCount)
        payoutProximityTotal = int(payoutProximityPerTotal * payoutProximityCount)
        html += '    <input type="number" min="0" max="1000" id="payoutProximityTotal" value="'+str(payoutProximityTotal)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutProximityCount">'
        html += '      Proximity Count'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <input type="number" min="0" max="1000" id="payoutProximityCount" value="'+str(payoutProximityCount)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutProximityPerTotal">'
        html += '      Proximity Per Total'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <input type="number" min="0" max="1000" id="payoutProximityPerTotal" value="'+str(payoutProximityPerTotal)+'" disabled/>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutSkinsAndSweepsTotal">'
        html += '      Skins and Sweeps'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutSkinsAndSweepsTotal = payoutTotal - payoutClubDues - payoutProximityTotal
        html += '    <input type="number" min="0" max="1000" id="payoutSkinsAndSweepsTotal" value="'+str(payoutSkinsAndSweepsTotal)+'" disabled />'
        html += '  </div>'
        html += '</div>'
        html += '<div class="row">'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutSkinsTotalPercent">'
        html += '      Skins Total Percent'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutSkinsTotalPercent = int(formatData['payoutSkinsTotalPercent'])
        html += '    <input type="number" min="0" max="100" id="payoutSkinsTotalPercent" value="'+str(payoutSkinsTotalPercent)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutSkinsTotal">'
        html += '      Skins Total'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutSkinsTotal = int(payoutSkinsAndSweepsTotal * payoutSkinsTotalPercent / 100)
        html += '    <input type="number" min="0" max="1000" id="payoutSkinsTotal" value="'+str(payoutSkinsTotal)+'" disabled />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutSweepsTotalPercent">'
        html += '      Sweeps Total Percent'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutSweepsTotalPercent = 100 - payoutSkinsTotalPercent
        html += '    <input type="number" min="0" max="100" id="payoutSweepsTotalPercent" value="'+str(payoutSweepsTotalPercent)+'" disabled />'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        html += '    <label for="payoutSweepsTotal">'
        html += '      Sweeps Total'
        html += '    </label>'
        html += '  </div>'
        html += '  <div class="col-sm-2">'
        payoutSweepsTotal = payoutSkinsAndSweepsTotal - payoutSkinsTotal
        html += '    <input type="number" min="0" max="1000" id="payoutSweepsTotal" value="'+str(payoutSweepsTotal)+'" />'
        html += '  </div>'
        html += '  <div class="col-sm-4"></div>'
        html += '</div>'
        payoutPercents = json.loads(super().getPayoutPercents(playerCount, 20, 0))
        paidTotal = payoutSweepsTotal
        for i in range(payoutPercents['payoutCount']):
            html += '<div class="row">'
            html += '  <div class="col-sm-2">'
            html += '    '+payoutPercents['payoutTextList'][i]
            html += '  </div>'
            html += '  <div class="col-sm-2">'
            html += '    <input type="text" id="player'+str(i)+'" value="'+playerData['netPlayers'][i]['name']+'" disabled />'
            html += '  </div>'
            html += '  <div class="col-sm-2">'
            thisPositionPayout = int(payoutSweepsTotal*payoutPercents['payoutList'][i]/100)
            #Give the last row the remaining money to remove any rounding errors.
            if (i == payoutPercents['payoutCount'] - 1):
                html += '    <input type="number" min="0" max="1000" id="player'+str(i)+'" value="'+str(paidTotal)+'" disabled />'
            else:
                html += '    <input type="number" min="0" max="1000" id="player'+str(i)+'" value="'+str(thisPositionPayout)+'" disabled />'
            paidTotal -= thisPositionPayout
            html += '  </div>'
            html += '  <div class="col-sm-4"></div>'
            html += '</div>'
        # for i in range(18):
        #     html += '<div class="row">'
        #     html += '  <div class="col-sm-2">'
        #     html += '    '+payoutPercents['payoutTextList'][i]
        #     html += '  </div>'
        #     html += '  <div class="col-sm-2">'
        #     html += '    <input type="text" id="player'+str(i)+'" value="'+playerData['netPlayers'][i]['name']+'" disabled />'
        #     html += '  </div>'
        #     html += '  <div class="col-sm-2">'
        #     thisPositionPayout = int(payoutSweepsTotal*payoutPercents['payoutList'][i]/100)
        #     #Give the last row the remaining money to remove any rounding errors.
        #     if (i == payoutPercents['payoutCount'] - 1):
        #         html += '    <input type="number" min="0" max="1000" id="player'+str(i)+'" value="'+str(paidTotal)+'" disabled />'
        #     else:
        #         html += '    <input type="number" min="0" max="1000" id="player'+str(i)+'" value="'+str(thisPositionPayout)+'" disabled />'
        #     paidTotal -= thisPositionPayout
        #     html += '  </div>'
        #     html += '  <div class="col-sm-4"></div>'
        #     html += '</div>'
            
        print (html)
        return html