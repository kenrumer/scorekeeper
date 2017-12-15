from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    url(r'^$', view_home.homeView, name='home'),
    url(r'^getallformatplugins/$', csrf_exempt(view_home.getAllFormatPlugins), name='getallformatplugins'),
    url(r'^getallcourses/$', csrf_exempt(view_home.getAllCourses), name='getallcourses'),
    url(r'^getcoursetees/$', csrf_exempt(view_home.getCourseTees), name='getcoursetees'),
    url(r'^checkfortournamentduplicate/$', csrf_exempt(view_home.checkForTournamentDuplicate), name='checkfortournamentduplicate'),
    url(r'^getalltournaments/$', csrf_exempt(view_home.getAllTournaments), name='getalltournaments'),
    url(r'^getallplayers/$', csrf_exempt(view_home.getAllPlayers), name='getallplayers'),
    url(r'^getallrecentactivities/$', csrf_exempt(view_home.getAllRecentActivities), name='getallrecentactivities'),
    url(r'^getimportexportbackupdata/$', csrf_exempt(view_home.getImportExportBackupData), name='getimportexportbackupdata'),
    
    url(r'^test/$', view_test.test, name='test'),
    url(r'^testview/$', csrf_exempt(view_test.testView), name='testview'),

    url(r'^importcourses/$', csrf_exempt(view_import.courses), name='importcourses'),
    url(r'^exportcourse/(?P<courseId>\d+)$', csrf_exempt(view_export.courses), name='exportcourse'),
    url(r'^exportloadplayersplugin/(?P<loadPlayersPluginId>\d+)$', csrf_exempt(view_export.loadPlayersPlugin), name='exportloadplayersplugin'),
    url(r'^exporttournamentformatplugin/(?P<tournamentFormatPluginId>\d+)$', csrf_exempt(view_export.tournamentFormatPlugin), name='exporttournamentformatplugin'),
    url(r'^exporttournamentroundimportplugin/(?P<tournamentRoundImportPluginId>\d+)$', csrf_exempt(view_export.tournamentRoundImportPlugin), name='exporttournamentroundimportplugin'),
    url(r'^exportdatabase/$', csrf_exempt(view_export.database), name='exportdatabase'),

    url(r'^clubprintouts/$', csrf_exempt(view_printout.clubPrintouts), name='clubprintouts'),
    url(r'^printplayers/$', csrf_exempt(view_printout.printPlayers), name='printplayers'),
    url(r'^printsignupsheets/$', csrf_exempt(view_printout.printSignupSheets), name='printsignupsheets'),
    
    url(r'^editcourses/$', view_course.editCourses, name='editcourses'),
    url(r'^getcourses/$', view_course.getCourses, name='getcourses'),
    url(r'^updatecourse/(?P<courseId>\d+)$', csrf_exempt(view_course.updateCourse), name='updatecourse'),
    url(r'^createcourse/$', csrf_exempt(view_course.createCourse), name='createcourse'),
    url(r'^removecourse/(?P<courseId>\d+)$', csrf_exempt(view_course.removeCourse), name='removecourse'),
    
    url(r'^editcoursetees/(?P<courseId>\d+)$', view_course.editCourseTees, name='editcoursetees'),
    url(r'^getcoursetees/(?P<courseId>\d+)$', view_course.getCourseTees, name='getcoursetees'),
    url(r'^updatecoursetee/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(view_course.updateCourseTee), name='updatecoursetee'),
    url(r'^createcoursetee/(?P<courseId>\d+)$', csrf_exempt(view_course.createCourseTee), name='createcoursetee'),
    url(r'^removecoursetee/(?P<courseTeeId>\d+)$', csrf_exempt(view_course.removeCourseTee), name='removecoursetee'),
    
    url(r'^editcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', view_course.editCourseTeeHoles, name='editcourseteeholes'),
    url(r'^getcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', view_course.getCourseTeeHoles, name='getcourseteeholes'),
    url(r'^updatecourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)/(?P<teeId>\d+)$', csrf_exempt(view_course.updateCourseTeeHole), name='updatecourseteehole'),
    url(r'^createcourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(view_course.createCourseTeeHole), name='createcourseteehole'),
    url(r'^removecourseteehole/(?P<teeId>\d+)$', csrf_exempt(view_course.removeCourseTeeHole), name='removecourseteehole'),
    
    url(r'^editplayers/$', view_player.editPlayers, name='editplayers'),
    url(r'^getplayers/$', csrf_exempt(view_player.getPlayers), name='getplayers'),
    url(r'^newplayer/$', csrf_exempt(view_player.newPlayer), name='newplayer'),
    url(r'^loadplayers/$', csrf_exempt(view_player.loadPlayers), name='loadplayers'),
    
    url(r'^editformats/$', view_tournament.editFormats, name='editformats'),

    url(r'^newtournament/$', csrf_exempt(view_tournament.newTournament), name='newtournament'),
    url(r'^tournament/$', csrf_exempt(view_tournament.tournament), name='tournament'),
    url(r'^clearrounddata/$', csrf_exempt(view_tournament.clearRoundData), name='clearrounddata'),
    url(r'^edittournament/(?P<tournamentId>\d+)$', view_tournament.tournament, name='edittournament'),
    url(r'^getscores/$', csrf_exempt(view_tournament.getScores), name='getscores'),
    url(r'^getpayout/$', csrf_exempt(view_tournament.getPayout), name='getpayout'),
    
    url(r'^updatescores/$', csrf_exempt(view_tournament.updateScores), name='updatescores'),
    url(r'^leaderboard/(?P<tournamentId>\d+)$', view_tournament.editTournament, name='edittournament'),
    
    url(r'^newscorecard/$', view_scorecard.newScorecard, name='newscorecard'),
    url(r'^addplayertoscorecard/$', view_scorecard.addPlayerToScorecard, name='addplayertoscorecard'),
    url(r'^addscoretoscorecard/$', view_scorecard.addScoreToScorecard, name='addscoretoscorecard'),
    url(r'^addroundtoplayer/$', view_player.addRoundToPlayer, name='addroundtoplayer'),
    
    url(r'^storesettings/$', view_settings.storeSettings, name='storesettings'),
    
    url(r'^docs/$', view_documentation.docs, name='docs'),
    url(r'^docs/codestyle$', view_documentation.docscodestyle, name='docscodestyle'),
    url(r'^docs/install$', view_documentation.docsinstall, name='docsinstall'),
    url(r'^docs/editting$', view_documentation.docseditting, name='docseditting'),
]
