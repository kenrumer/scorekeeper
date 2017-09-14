from django.db import models

# Create your models here.

from django.urls import reverse

class Tournament(models.Model):
    """
    Model representing a Tournament
    """
    name = models.CharField(max_length=200, verbose_name='Name', help_text='Enter the name of the tournament (e.g. John Doe Memorial)')
    format = models.ForeignKey('Format', verbose_name='Format', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the tournament format')
    courses = models.ManyToManyField('Course', verbose_name='Courses', blank=True, help_text='Select the courses players are playing and set the default for the card')
    course_tees = models.ManyToManyField('CourseTee', verbose_name='Course and tee', blank=True, help_text='Select the courses and tees players are playing')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class TournamentDate(models.Model):
    """
    Model for the range of dates for a tournament.  Only used in the search date ranges
    """
    date = models.DateField(verbose_name='Date', null=True, blank=True, help_text='Select the date for this tournament')
    tournament = models.ForeignKey('Tournament', verbose_name='Tournament Played', on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the tournament(s) played this date')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.tournament.name

class Format(models.Model):
    """
    Model representing a Tournament Format
    """
    name = models.CharField(max_length=200, help_text='Enter the name of the format')
    priority = models.IntegerField(verbose_name='Priority', default=-1, help_text='Highest priority will be listed first in selecting format')
    class_package = models.CharField(max_length=200, null=True, blank=True, help_text='Name of the module (filename with the .py) containing the class of your plugin')
    class_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the class with the module')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class TournamentPayoutPlugin(models.Model):
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
    Model representing a Round
    """
    handicap_index = models.DecimalField(max_digits=3, verbose_name='Handicap Index', decimal_places=1, help_text='Enter the players handicap index at time of tournament')
    course_handicap = models.IntegerField(verbose_name='Course Handicap', help_text='Enter the course handicap at time of tournament')
    total_in = models.IntegerField(verbose_name='IN', help_text='Enter the score of the front 9 holes')
    total_out = models.IntegerField(verbose_name='OUT', help_text='Enter the score of the back 9 holes')
    total = models.IntegerField(verbose_name='Total', help_text='Enter the total score for the round')
    net = models.IntegerField(verbose_name='Course Handicap', help_text='Enter the net score for the round')
    player = models.ForeignKey('Player', verbose_name='Player Id')
    tournament = models.ForeignKey('Tournament', verbose_name='Tournament Id', on_delete=models.SET_NULL, null=True, blank=True)
    scorecard = models.ForeignKey('Scorecard', verbose_name='Scorecard')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.player.name

class Scorecard(models.Model):
    """
    Model representing a Scorecard is a ForeignKey to rounds
    """
    date = models.DateField(verbose_name='Date', null=True, blank=True, help_text='Enter the date for the scorecard')
    tee_time = models.DateField(verbose_name='Tee Time', null=True, blank=True, help_text='Enter the tee time for the scorecard')
    finish_time = models.DateField(verbose_name='Finish Time', null=True, blank=True, help_text='Enter the finish time for the scorecard')
    scorer = models.ForeignKey('Player', related_name='player_scorer', verbose_name='Scorer Player Id', null=True, blank=True, help_text='Enter the player that kept score')
    external_scorer = models.CharField(max_length=200, verbose_name='External Scorer Name', null=True, blank=True,  help_text='Enter the name of the scorer if it is not a player')
    attest = models.ForeignKey('Player', related_name='player_attest', verbose_name='Attest Player Id', null=True, blank=True, help_text='Enter the player that attests with the score')
    external_attest = models.CharField(max_length=200, verbose_name='External Attestation Name', null=True, blank=True, help_text='Enter the name of the attestation if it is not a player')

class Score(models.Model):
    """
    Model representing a single raw score. These values will be altered in a tournament
        when calibrated with a format, course, handicap, tee handicap
    """
    score = models.IntegerField(verbose_name='Score', help_text='Enter the score for the hole')
    hole_played = models.IntegerField(verbose_name='Hole Played', null=True, blank=True, help_text='Enter the hole number played (e.g. in shotgun start if this is hole 16, but the second hole played enter 2)')
    tee = models.ForeignKey('Tee', verbose_name='Hole and Tee Id')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.score

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
    course = models.ForeignKey('Course', default=113, verbose_name='Course Id')
    COLOR_CHOICES = (
        (0, 'None'),
        (1, 'Yellow'),
        (2, 'Green'),
        (3, 'Red'),
        (4, 'White'),
        (5, 'Blue'),
        (6, 'Black'),
        (7, 'Gold'),
    )
    color = models.IntegerField(choices=COLOR_CHOICES, verbose_name='Tee Color', help_text='Enter the number associated with the tee color (0:None,1:Yellow,2:Green,3:Red,4:White,5:Blue,6:Black,7:Gold)')
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
        return self.course_tee.name + " - " + str(self.hole__number)

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
    player_type = models.ForeignKey('PlayerType', blank=True, verbose_name='Player Type');
    club = models.ForeignKey('Club', null=True, blank=True, verbose_name='Club')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class PlayerType(models.Model):
    """
    Model representing a Player or group of players type
    """
    name = models.CharField(max_length=140, help_text='The type of player is likely person, 2-man, 4-man')
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
    class_package = models.CharField(max_length=200, null=True, blank=True, help_text='Name of the module (filename with the .py) containing the class of your plugin')
    class_name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter the name of the class with the module')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.class_package
