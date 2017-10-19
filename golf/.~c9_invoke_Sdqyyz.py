from django.db import models

# Create your models here.

from django.urls import reverse

class Tournament(models.Model):
    """
    Model representing a Tournament, a set of tournament rounds
    """
    name = models.CharField(max_length=200, verbose_name='Name', help_text='Enter the name of the tournament (e.g. John Doe Memorial)')
    format_plugin = models.ForeignKey('FormatPlugin', verbose_name='Format', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the tournament format')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class TournamentRound(models.Model):
    """
    name, form
    name, format and date_scheduled should be the uniqueness
    Editting these fields will be a pain!!!
    """
    name = models.CharField(max_length=200, verbose_name='Name', help_text='Enter the name of this round of the tournament')
    date_scheduled = models.DateField(verbose_name='Date Scheduled', null=True, blank=True, help_text='Date this round of the tournament was supposed to be played')
    date_started = models.DateField(verbose_name='Date Started', null=True, blank=True, help_text='Select the date started (rarely different than scheduled)for this tournament')
    date_finished = models.DateField(verbose_name='Date Finished', null=True, blank=True, help_text='Select the date finished (rarely different than scheduled)for this tournament')
    round_format_plugin = models.ForeignKey('RoundFormatPlugin', verbose_name='Format', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the tournament format')
    tournament = models.ForeignKey('Tournament', verbose_name='Tournament Played', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the tournament')

    courses = models.ManyToManyField('Course', verbose_name='Courses', blank=True, help_text='Select the courses players are playing and set the default for the card')
    course_tees = models.ManyToManyField('CourseTee', verbose_name='Course and tee', blank=True, help_text='Select the courses and tees players are playing')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class FormatPlugin(models.Model):
    """
    Model representing a Format Plugin
    """
    name = models.CharField(max_length=200, help_text='Enter the name of the tournament format')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Highest priority will be listed first in selecting a tournament format')
    class_package = models.CharField(max_length=200, null=True, blank=True, help_text='Name of the module (filename without the .py) containing the class of your plugin')
    class_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the class with the module')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Scorecard(models.Model):
    """
    Model representing a Scorecard is a ForeignKey to rounds
    """
    tee_time = models.TimeField(verbose_name='Tee Time', null=True, blank=True, help_text='Enter the tee time for the scorecard')
    finish_time = models.TimeField(verbose_name='Finish Time', null=True, blank=True, help_text='Enter the finish time for the scorecard')
    external_scorer = models.CharField(max_length=200, verbose_name='External Scorer Name', null=True, blank=True,  help_text='Enter the name of the scorer if it is not a player')
    external_attest = models.CharField(max_length=200, verbose_name='External Attestation Name', null=True, blank=True, help_text='Enter the name of the attestation if it is not a player')
    scorer = models.ForeignKey('Player', related_name='player_scorer', verbose_name='Scorer Player Id', null=True, blank=True, help_text='Enter the player that kept score')
    attest = models.ForeignKey('Player', related_name='player_attest', verbose_name='Attest Player Id', null=True, blank=True, help_text='Enter the player that attests with the score')
    tournament_round = models.ForeignKey('TournamentRound', verbose_name='Tournament Round', on_delete=models.SET_NULL, null=True, blank=True, help_text='map to tournament round')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        retStr = ''
        try:
            dateStr = 'Date: '+self.tournament_round.date.strftime('%m/%d/%Y') + ', '
        except:
            dateStr = ''
        try:
            teeTime = 'Tee Time: '+self.tee_time.strftime('%H:%M') + ', '
        except:
            teeTime = ''
        try:
            finishTime = 'Finish time: '+self.finish_time.strftime('%H:%M')
        except:
            finishTime = ''
        
        return dateStr+teeTime+finishTime

class PayoutPlugin(models.Model):
    """
    Model representing the plugins that will calculate payout for the overall tournament
    Payout plugin gets a ton of data each time a scorecard is submitted
    This plugin needs to return players that are paid (overall tournament and per round) for net scores, gross scores, skins, values for pins, number of drawings, others (magic holes, hole in one)
    """
    name = models.CharField(max_length=200, help_text="Enter the name of the plugin")
    class_package = models.CharField(max_length=200, help_text="Name of the module (filename with the .py) containing the class of your plugin")
    class_name = models.CharField(max_length=200, help_text="Enter the name of the class with the module")
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.class_package

class Round(models.Model):
    """
    Model representing a Round. This with scores creates a single page of the tournament view
    Each player has a round in a tournament, a little ambigous, it'll make sense some day
    Each round has many scores
    """
    handicap_index = models.DecimalField(max_digits=3, verbose_name='Handicap Index', decimal_places=1, help_text='Enter the players handicap index at time of tournament')
    course_handicap = models.IntegerField(verbose_name='Course Handicap', help_text='Enter the course handicap at time of tournament')
    total_out = models.IntegerField(verbose_name='OUT', null=True, blank=True, help_text='Enter the score of the front 9 holes')
    total_out_style = models.CharField(max_length=200, verbose_name='Style for total out gross style', null=True, blank=True,  help_text='Enter the background-color for the cell in gross view')
    total_out_net = models.IntegerField(verbose_name='Front 9 Net', null=True, blank=True, help_text='Enter the net score for the front nine')
    total_out_net_style = models.CharField(max_length=200, verbose_name='Style for total out net style', null=True, blank=True,  help_text='Enter the background-color for the cell in net view')
    total_in = models.IntegerField(verbose_name='IN', null=True, blank=True, help_text='Enter the score of the back 9 holes')
    total_in_style = models.CharField(max_length=200, verbose_name='Style for total in gross style', null=True, blank=True,  help_text='Enter the background-color for the cell in gross view')
    total_in_net = models.IntegerField(verbose_name='Back 9 Net', null=True, blank=True, help_text='Enter the net score for the back 9')
    total_in_net_style = models.CharField(max_length=200, verbose_name='Style for total in net style', null=True, blank=True,  help_text='Enter the background-color for the cell in net view')
    total = models.IntegerField(verbose_name='Total', null=True, blank=True, help_text='Enter the total score for the round')
    total_style = models.CharField(max_length=200, verbose_name='Style for total gross style', null=True, blank=True,  help_text='Enter the background-color for the cell in gross view')
    net = models.IntegerField(verbose_name='Course Handicap', null=True, blank=True, help_text='Enter the net score for the round')
    net_style = models.CharField(max_length=200, verbose_name='Style for total net style', null=True, blank=True,  help_text='Enter the background-color for the cell in net view')
    player = models.ForeignKey('Player', verbose_name='Player Id')
    date_started = models.DateField(verbose_name='Date Started', null=True, blank=True, help_text='Select the date this round was started')
    date_finished = models.DateField(verbose_name='Date Finished', null=True, blank=True, help_text='Select the date this round was finished')
    tournament_round = models.ForeignKey('TournamentRound', verbose_name='Tournament Round', on_delete=models.SET_NULL, null=True, blank=True, help_text='map to tournament round')
    scorecard = models.ForeignKey('Scorecard', verbose_name='Scorecard')
    course_tee = models.ForeignKey('CourseTee', verbose_name='Course and Tee', null=True, blank=True, help_text='Course and Tee This Round was Played on')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.player.name + ' - ' + self.tournament_round.date.strftime('%m/%d/%Y')

class Score(models.Model):
    """
    Model representing a single raw score. These values will be altered in a tournament
        when calibrated with a format, course, handicap, tee handicap
    """
    score = models.IntegerField(verbose_name='Score', help_text='Enter the score for the hole')
    score_style = models.CharField(max_length=200, verbose_name='Style Applied to the Cell', null=True, blank=True,  help_text='Enter the background-color for the cell in gross view')
    score_net = models.IntegerField(verbose_name='Score Net', null=True, blank=True, help_text='Enter the net score for the hole')
    score_net_style = models.CharField(max_length=200, verbose_name='External Scorer Name', null=True, blank=True,  help_text='Enter the background-color for the cell in net view')
    hole_played = models.IntegerField(verbose_name='Hole Played', null=True, blank=True, help_text='Enter the hole number played (e.g. in shotgun start if this is hole 16, but the second hole played enter 2)')
    tee = models.ForeignKey('Tee', verbose_name='Hole and Tee Id')
    round = models.ForeignKey('Round', null=True, blank=True, verbose_name='Round for this score')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        #return str(self.score)
        #try:
        #    td = TournamentRound.objects.get(tournament=self.round.tournament.id)
        #except TournamentRound.DoesNotExist:
        #    return str(self.score)
        #return td.date.strftime('%m/%d/%Y') + ': ' + self.tee.hole.course.name + ' #' + str(self.tee.hole.number) + ' "' + str(self.score) + '" - ' + self.round.player.name
        return str(self.score)

class RoundFormatPlugin(models.Model):
    """
    Model representing a Tournament Format
    """
    name = models.CharField(max_length=200, help_text='Enter the name of the format')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Highest priority will be listed first in selecting format')
    class_package = models.CharField(max_length=200, null=True, blank=True, help_text='Name of the module (filename without the .py) containing the class of your plugin')
    class_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the class with the module')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Course(models.Model):
    """
    Model representing a course this is the sum of all course tees
    """
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the Course (e.g. Callaway Gardens)')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Lowest number greater than 0 will be listed first in selecting format')
    default = models.BooleanField(verbose_name='Default', default=False, help_text='Set a default for faster starts to putting scores in')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class CourseTee(models.Model):
    """
    Model representing a single Tee for a course
    """
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the Course and Tee box (e.g. Callaway Gardens - White)')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Highest priority will be listed first in selecting format')
    default = models.BooleanField(verbose_name='Default', default=False, help_text='Set a default for faster starts to putting scores in')
    slope = models.IntegerField(verbose_name='Slope', help_text='Enter the slope for this course and tee')
    color = models.CharField(max_length=200, verbose_name='Tee Color', help_text='Enter the number associated with the tee color')
    course = models.ForeignKey('Course', default=113, verbose_name='Course Id')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.course.name+' - '+self.name

class Tee(models.Model):
    """
    Model representing a single Tee for a single hole for a course
    """
    yardage = models.IntegerField(verbose_name='Yardage', help_text='Enter the yardage for the tee')
    par = models.PositiveSmallIntegerField(verbose_name='Par', help_text='Enter the par for this tee')
    handicap = models.PositiveSmallIntegerField(verbose_name='Handicap', help_text='Enter the handicap for this tee')
    hole = models.ForeignKey('Hole', verbose_name='Hole Id', null=True, on_delete=models.SET_NULL)
    course_tee = models.ForeignKey('CourseTee', verbose_name='Course Tee Id')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.course_tee.name

class Hole(models.Model):
    """
    Model representing a single hole for a course
    """
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the hole')
    number = models.IntegerField(help_text='Enter the number of the hole')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Course this hole belongs to')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Activity(models.Model):
    """
    Model representing recent activity from the app
    """
    title = models.CharField(max_length=40, null=True, blank=True, help_text='Enter the title for this activity')
    notes = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the notes for this activity')
    date = models.DateField(verbose_name='Date', null=True, blank=True, help_text='Enter the date for the scorecard')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.title

class Club(models.Model):
    """
    Model representing the club probably a configuration item because there can only be 1
    """
    name = models.CharField(max_length=200, help_text='Enter the name of the club')
    logo = models.ImageField(max_length=200, null=True, blank=True, help_text='logo')
    default_tournament_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter default prefix for a tournament name')
    web_site = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the web site for the club')
    data = models.CharField(max_length=516, null=True, blank=True, help_text='Data such as username and password used to login to your clubs player data store (used by your plugin)')
    players_last_updated = models.DateTimeField(null=True, blank=True, help_text='Enter the date the players handicaps were last updated')
    player_plugin = models.ForeignKey('PlayerPlugin', null=True, blank=True, verbose_name='Player Plugin Id')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Player(models.Model):
    """
    Model representing a Player
    """
    club_member_number = models.IntegerField(verbose_name='Club Member Number', default=-1, help_text='Enter the players club member number (GHIN number)')
    name = models.CharField(max_length=200, help_text='Enter the name of the player')
    handicap_index = models.DecimalField(max_digits=3, verbose_name='Current Handicap Index', decimal_places=1, help_text='Enter the handicap index')
    high_handicap_index = models.DecimalField(max_digits=3, verbose_name='High Handicap Index', decimal_places=1, help_text='Enter the high handicap index')
    low_handicap_index = models.DecimalField(max_digits=3, verbose_name='Low Handicap Index', decimal_places=1, help_text='Enter the low handicap index')
    last_updated = models.DateTimeField(verbose_name='Last Updated', null=True, blank=True, help_text='Last time the player plugin was used to get this player')
    data = models.CharField(max_length=516, null=True, blank=True, help_text='Data such as address, phone number, age')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Highest priority will be listed first in selecting format')
    club = models.ForeignKey('Club', null=True, blank=True, verbose_name='Club')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class PlayerPlugin(models.Model):
    """
    Model representing the plugins that can communicate with external player stores
    """
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the plugin')
    class_package = models.CharField(max_length=200, null=True, blank=True, help_text='Name of the module (filename without the .py) containing the class of your plugin')
    class_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the class with the module')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.class_package