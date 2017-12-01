from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    url(r'^$', home.homeView, name='home'),
    url(r'^getallformatplugins/$', csrf_exempt(home.getAllFormatPlugins), name='getallformatplugins'),
    url(r'^getallcourses/$', csrf_exempt(home.getAllCourses), name='getallcourses'),
    url(r'^getcoursetees/$', csrf_exempt(home.getCourseTees), name='getcoursetees'),
    url(r'^checkfortournamentduplicate/$', csrf_exempt(home.checkForTournamentDuplicate), name='checkfortournamentduplicate'),
    url(r'^getalltournaments/$', csrf_exempt(home.getAllTournaments), name='getalltournaments'),
    url(r'^getallplayers/$', csrf_exempt(home.getAllPlayers), name='getallplayers'),
    url(r'^getallrecentactivities/$', csrf_exempt(home.getAllRecentActivities), name='getallrecentactivities'),
    url(r'^getimportexportbackupdata/$', csrf_exempt(home.getImportExportBackupData), name='getimportexportbackupdata'),

    url(r'^exportcourse/(?P<courseId>\d+)$', csrf_exempt(exports.course), name='exportcourse'),
    url(r'^exportloadplayersplugin/(?P<loadPlayersPluginId>\d+)$', csrf_exempt(exports.loadPlayersPlugin), name='exportloadplayersplugin'),
    url(r'^clubprintouts/$', csrf_exempt(exports.clubPrintouts), name='clubprintouts'),
    
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
    url(r'^newplayer/$', csrf_exempt(players.newPlayer), name='newplayer'),
    url(r'^loadplayers/$', csrf_exempt(players.loadPlayers), name='loadplayers'),
    url(r'^printplayers/$', csrf_exempt(exports.printPlayers), name='printplayers'),
    url(r'^printsignupsheets/$', csrf_exempt(exports.printSignupSheets), name='printsignupsheets'),
    
    url(r'^editformats/$', tournaments.editFormats, name='editformats'),

    url(r'^newtournament/$', csrf_exempt(tournaments.newTournament), name='newtournament'),
    url(r'^tournament/$', csrf_exempt(tournaments.tournament), name='tournament'),
    url(r'^clearrounddata/$', csrf_exempt(tournaments.clearRoundData), name='clearrounddata'),
    url(r'^edittournament/(?P<tournamentId>\d+)$', tournaments.tournament, name='edittournament'),
    url(r'^getscores/$', csrf_exempt(tournaments.getScores), name='getscores'),
    url(r'^getpayout/$', csrf_exempt(tournaments.getPayout), name='getpayout'),
    
    url(r'^updatescores/$', csrf_exempt(tournaments.updateScores), name='updatescores'),
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
