from ..abc_base import FormatBase
import json
import math

"""
    Class for calculating player gross and net scores in a skins and pins tournament.
    The handicaps for each hole for each course tee played are in a variable called course_handicaps
    The existing tournament standings are in a variable called tournament_standings
    In order to help calculate net_scores, call course_tee = super().getCourseTeeById(tee_id)
    You can use it or call updated_tournament_standings = super().mergePlayerResults(tournament_id, new_player_results_list)
        the new_player_results_list param in mergePlayers is [{club_member_number:club_member_number, tee_id:tee_id, gross_scores:[gross_scores], net_scores:[net_scores]}]
        the returned updated_tournament_standings will have the same format, but include all scored players so you can set the styles
    You also need to call super().updateTournament(tournament_id, updated_tournament_standings) in order to update the database
        updated_tournament_standings has the format:
        [{club_member_number:club_member_number, tee_id:tee_id, gross_scores:[gross_scores], gross_styles:[gross_styles], net_scores:[net_scores], net_styles:[net_styles]}]
        and will write the database so the tournament tables can be drawn with the background colors for low net/skins
"""
class SkinsAndPinsFormat(FormatBase):

    def __init__(self):
        pass

    def calculateScores(self, data):
        """
            Based on all scores from each player (on save from scorecard), what is the 'value' (store raw && net && cell style in the score table, assign score to player, round and scorecard)
            Retrieve players from the input (this saved scorecard) source and return an object.
            scores = '[{"clubMemberNumber":"12345","playerName":"Doe, John","hcpIndex":"25.7","teeId":7,"courseHCP":20,"hole0":4,"hole1":3,"hole2":3,"hole3":3,"hole4":4,"hole5":4,"hole6":3,"hole7":3,"hole8":3,"totalout":30,"hole9":3,"hole10":3,"hole11":3,"hole12":4,"hole13":4,"hole14":3,"hole15":4,"hole16":3,"hole17":3,"totalin":30,"total":60,"totalnet":40}]'
            tournamentId = '55'
        """
        new_player_results_list = []
        scores = json.loads(data['scores'])
        tournament_id = data['tournamentId']
        for player in scores:
            courseTee = super().getCourseTeeById(player['teeId'])
            totHcp = math.floor(player['courseHCP']/2)
            player['gross_scores'] = []
            player['net_scores'] = []
            tmp_net_scores = {}
            for i in range(0, 17):
                if (courseTee[i]['handicap'] <= totHcp):
                    tmp_net_scores['hole'+str(courseTee[i]['hole__number']-1)] = player['hole'+str(courseTee[i]['hole__number']-1)] - 1
                else:
                    tmp_net_scores['hole'+str(courseTee[i]['hole__number']-1)] = player['hole'+str(courseTee[i]['hole__number']-1)]
            for i in range(0, 17):
                player['gross_scores'].append(player['hole'+str(i)])
                player['net_scores'].append(tmp_net_scores['hole'+str(i)])
            new_player_results_list.append(player)
        updated_tournament_standings = super().mergePlayerResults(tournament_id, new_player_results_list)
        lowest_total_gross_count = 0
        lowest_total_net_count = 0
        lowest_total_out_count = 0
        lowest_total_out_net_count = 0
        lowest_total_in_count = 0
        lowest_total_in_net_count = 0
        for standing in updated_tournament_standings:
            standing['gross_styles'] = []
            standing['net_styles'] = []
            lowest_total_gross = 1000
            lowest_total_net = 1000
            lowest_total_out = 1000
            lowest_total_out_net = 1000
            lowest_total_in = 1000
            lowest_total_in_net = 1000
            standing['totaloutnet'] = math.ceil(standing['totalout'] - (standing['courseHCP']/2))
            standing['totalinnet'] = math.floor(standing['totalin'] - (standing['courseHCP']/2))
            if (standing['total'] < lowest_total_gross):
                lowest_total_gross_count += 1
                lowest_total_gross = standing['total']
            if (standing['totalnet'] < lowest_total_net):
                lowest_total_net_count += 1
                lowest_total_net = standing['totalnet']
            if (standing['totalout'] < lowest_total_out):
                lowest_total_out_count += 1
                lowest_total_out = standing['totalout']
            if (standing['totaloutnet'] < lowest_total_out_net):
                lowest_total_out_net_count += 1
                lowest_total_out_net = standing['totaloutnet']
            if (standing['totalin'] < lowest_total_in):
                lowest_total_in_count += 1
                lowest_total_in = standing['totalin']
            if (standing['totalinnet'] < lowest_total_in_net):
                lowest_total_in_net_count += 1
                lowest_total_in_net = standing['totalinnet']
        for standing in updated_tournament_standings:
            if (lowest_total_gross_count == 1):
                if (standing['total'] == lowest_total_gross):
                    standing['totalstyle'] = 'background-color:#eee'
                else:
                    standing['totalstyle'] = ''
            if (lowest_total_net_count == 1):
                if (standing['totalnet'] == lowest_total_gross):
                    standing['totalnetstyle'] = 'background-color:#eee'
                else:
                    standing['totalnetstyle'] = ''
            if (lowest_total_out_count == 1):
                if (standing['totalout'] == lowest_total_gross):
                    standing['totaloutstyle'] = 'background-color:#eee'
                else:
                    standing['totaloutstyle'] = ''
            if (lowest_total_out_net_count == 1):
                if (standing['totaloutnet'] == lowest_total_gross):
                    standing['totaloutnetstyle'] = 'background-color:#eee'
                else:
                    standing['totaloutnetstyle'] = ''
            if (lowest_total_in_count == 1):
                if (standing['totalin'] == lowest_total_gross):
                    standing['totalinstyle'] = 'background-color:#eee'
                else:
                    standing['total_style'] = ''
            if (lowest_total_in_net_count == 1):
                if (standing['totalinnet'] == lowest_total_gross):
                    standing['totalinnetstyle'] = 'background-color:#eee'
                else:
                    standing['totalinnetstyle'] = ''
        for i in range(0, 17):
            lowest_gross = 100
            lowest_net = 100
            lowest_gross_count = 0
            lowest_net_count = 0
            for standing in updated_tournament_standings:
                if (standing['gross_scores'][i] < lowest_gross):
                    lowest_gross_count += 1
                    lowest_gross = standing['gross_scores'][i]
                if (standing['net_scores'][i] < lowest_net):
                    lowest_net_count += 1
                    lowest_net = standing['net_scores'][i]
            for standing in updated_tournament_standings:
                if (lowest_gross_count == 1):
                    if (standing['gross_scores'][i] == lowest_gross):
                        standing['gross_styles'].append('background-color:#ccc;')
                    else:
                        standing['gross_styles'].append('')
                if (lowest_net_count == 1):
                    if (standing['net_scores'][i] == lowest_net):
                        standing['net_styles'].append('background-color:#ccc;')
                    else:
                        standing['net_styles'].append('')
        print (updated_tournament_standings)
        super().updateTournament(tournament_id, updated_tournament_standings)