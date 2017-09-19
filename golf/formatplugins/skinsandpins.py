from ..abc_base import FormatBase

"""
    Class for calculating player gross and net scores in a skins and pins tournament.
    The handicaps for each hole for each course tee played are in a variable called course_handicaps
    The existing tournament standings are in a variable called tournament_standings
    You can use it or call updated_tournament_standings = super().mergePlayerResults(new_player_results_list)
        the new_player_results_list param in mergePlayers is [{club_member_number:club_member_number, gross_scores:[gross_scores], net_scores:[net_scores]}]
        the returned updated_tournament_standings will have the same format, but include all scored players so you can set the styles
    You also need to call super().updateTournament(current_tournament_results) in order to update the database
        current_tournament_results has the format:
        [{club_member_number:club_member_number, gross_scores:[gross_scores], gross_styles:[gross_styles], net_scores:[net_scores], net_styles:[net_styles]}]
        and will write the database so the tournament tables can be drawn with the background colors for low net/skins
"""
class SkinsAndPinsFormat(FormatBase):

    def __init__(self):
        pass

    def calculateScores(self, players):
        """
            Based on all scores from each player (on save from scorecard), what is the 'value' (store raw && net && cell style in the score table, assign score to player, round and scorecard)
            Retrieve players from the input (this saved scorecard) source and return an object.
            [{
                clubMemberNumber:"701505",
                courseHCP:14,
                hcpIndex:"18.9",
                hole0:4,
                hole1:3,
                hole2:3,
                hole3:3,
                hole4:4,
                hole5:4,
                hole6:3,
                hole7:3,
                hole8:3,
                hole9:3,
                hole10:3,
                hole11:3,
                hole12:4,
                hole13:4,
                hole14:3,
                hole15:4,
                hole16:3,
                hole17:3,
                playerName:"Doe, John",
                slope:84,
                teeColor:"Red",
                total:60,
                totalin:30,
                totalnet:46,
                totalout:30
            }]
        """
        new_player_results_list = []
        for player in players:
            print (player)
            player_results = {}
            player_results['clubMemberNumber'] = player['clubMemberNumber']
            player_results['gross_scores'] = [player['hole0'], player['hole1'], player['hole2'], player['hole3'], player['hole4'], player['hole5'], player['hole6'], player['hole7'], player['hole8'], player['hole9'], player['hole10'], player['hole11'], player['hole12'], player['hole13'], player['hole14'], player['hole15'], player['hole16'], player['hole17'] ]
            new_player_results_list.append(player_results)
        #super().mergePlayerResults(new_player_results_list)