from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    url(r'^$', home.homeView, name='home'),
    
    url(r'^editcourses/$', courses.editCourses, name='editcourses'),
    url(r'^getcourses/$', courses.getCourses, name='getcourses'),
    url(r'^updatecourse/(?P<courseId>\d+)$', csrf_exempt(courses.updateCourse), name='updatecourse'),
    url(r'^createcourse/$', csrf_exempt(courses.createCourse), name='createcourse'),
    url(r'^removecourse/(?P<courseId>\d+)$', csrf_exempt(courses.removeCourse), name='removecourse'),
    
    url(r'^editcoursetees/(?P<courseId>\d+)$', courses.editCourseTees, name='editcoursetees'),
    url(r'^getcoursetees/(?P<courseId>\d+)$', courses.getCourseTees, name='getcoursetees'),
    url(r'^updatecoursetee/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(courses.updateCourseTee), name='updatecoursetee'),
    url(r'^createcoursetee/(?P<courseId>\d+)$', csrf_exempt(courses.createCourseTee), name='createcoursetee'),
    url(r'^removecoursetee/(?P<courseTeeId>\d+)$', csrf_exempt(courses.removeCourseTee), name='removecoursetee'),
    
    url(r'^editcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', courses.editCourseTeeHoles, name='editcourseteeholes'),
    url(r'^getcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', courses.getCourseTeeHoles, name='getcourseteeholes'),
    url(r'^updatecourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)/(?P<teeId>\d+)$', csrf_exempt(courses.updateCourseTeeHole), name='updatecourseteehole'),
    url(r'^createcourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(courses.createCourseTeeHole), name='createcourseteehole'),
    url(r'^removecourseteehole/(?P<teeId>\d+)$', csrf_exempt(courses.removeCourseTeeHole), name='removecourseteehole'),
    
    url(r'^editplayers/$', players.editPlayers, name='editplayers'),
    url(r'^getplayers/$', csrf_exempt(players.getPlayers), name='getplayers'),
    url(r'^newplayer/$', players.newPlayer, name='newplayer'),
    url(r'^loadplayers/$', csrf_exempt(players.loadPlayers), name='loadplayers'),
    url(r'^printplayers/$', csrf_exempt(printables.printPlayers), name='printplayers'),
    url(r'^printsignupsheets/$', csrf_exempt(printables.printSignupSheets), name='printsignupsheets'),
    
    url(r'^editformats/$', tournaments.editFormats, name='editformats'),

    url(r'^checkfortournamentduplicate/$', csrf_exempt(tournaments.checkForTournamentDuplicate), name='checkfortournamentduplicate'),
    url(r'^newtournament/$', csrf_exempt(tournaments.newTournament), name='newtournament'),
    url(r'^edittournament/(?P<tournamentId>\d+)$', tournaments.editTournament, name='edittournament'),
    
    url(r'^calculatescores/$', csrf_exempt(tournaments.calculateScores), name='calculatescores'),
    url(r'^leaderboard/(?P<tournamentId>\d+)$', tournaments.editTournament, name='edittournament'),
    
    url(r'^newscorecard/$', scorecards.newScorecard, name='newscorecard'),
    url(r'^addplayertoscorecard/$', scorecards.addPlayerToScorecard, name='addplayertoscorecard'),
    url(r'^addscoretoscorecard/$', scorecards.addScoreToScorecard, name='addscoretoscorecard'),
    url(r'^addroundtoplayer/$', players.addRoundToPlayer, name='addroundtoplayer'),
    
    url(r'^storesettings/$', settings.storeSettings, name='storesettings'),
    
    url(r'^docs/$', documentation.docs, name='docs'),
    url(r'^docs/codestyle$', documentation.docscodestyle, name='docscodestyle'),
    url(r'^docs/install$', documentation.docsinstall, name='docsinstall'),
    url(r'^docs/editting$', documentation.docseditting, name='docseditting'),
]
