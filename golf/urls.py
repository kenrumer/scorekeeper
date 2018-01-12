from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import *
from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

urlpatterns = [
    url(r'^director/$', group_required('Admins', 'Directors')(view_director.directorView), name='director'),
    url(r'^getallformatplugins/$', group_required('Directors')(view_director.getAllFormatPlugins), name='getallformatplugins'),
    url(r'^checkfortournamentduplicate/$', group_required('Directors')(view_director.checkForTournamentDuplicate), name='checkfortournamentduplicate'),
    url(r'^getalltournaments/$', group_required('Directors')(view_director.getAllTournaments), name='getalltournaments'),
    url(r'^getallplayers/$', group_required('Directors')(view_director.getAllPlayers), name='getallplayers'),
    url(r'^getallrecentactivities/$', group_required('Admins')(view_director.getAllRecentActivities), name='getallrecentactivities'),
    url(r'^getimportexportbackupdata/$', group_required('Admins')(view_director.getImportExportBackupData), name='getimportexportbackupdata'),
    
    url(r'^test/$', view_test.test, name='test'),
    url(r'^testview/$', view_test.testView, name='testview'),

    url(r'^importcourses/$', group_required('Admins')(view_import.courses), name='importcourses'),
    url(r'^importroundimportplugins/$', group_required('Admins')(view_import.importRoundImportPlugins), name='importroundimportplugins'),
    url(r'^importplayerplugins/$', group_required('Admins')(view_import.playerPlugins), name='importplayerplugins'),
    url(r'^importformatplugins/$', group_required('Admins')(view_import.formatPlugins), name='importformatplugins'),

    url(r'^getteesandholes/$', group_required('Admins','Directors')(view_export.getTeesAndHoles), name='getteesandholes'),
    url(r'^exportplayerplugin/(?P<playersPluginId>\d+)$', group_required('Admins')(view_export.playerPlugin), name='exportplayerplugin'),
    url(r'^exportformatplugin/(?P<formatPluginId>\d+)$', group_required('Admins')(view_export.formatPlugin), name='exportformatplugin'),
    url(r'^exportroundimportplugin/(?P<roundImportPluginId>\d+)$', group_required('Admins')(view_export.roundImportPlugin), name='exportroundimportplugin'),
    url(r'^exportdatabase/$', group_required('Admins')(view_export.database), name='exportdatabase'),

    url(r'^clubprintouts/$', group_required('Admins', 'Directors')(view_printout.clubPrintouts), name='clubprintouts'),
    url(r'^printplayers/$', group_required('Admins', 'Directors')(view_printout.printPlayers), name='printplayers'),
    url(r'^printsignupsheets/$', group_required('Admins', 'Directors')(view_printout.printSignupSheets), name='printsignupsheets'),
    
    url(r'^editcourses/$', group_required('Admins')(view_course.editCourses), name='editcourses'),
    url(r'^getcourses/$', group_required('Admins', 'Directors')(view_course.getCourses), name='getcourses'),
    url(r'^updatecourse/(?P<courseId>\d+)$', group_required('Admins')(view_course.updateCourse), name='updatecourse'),
    url(r'^createcourse/$', group_required('Admins')(view_course.createCourse), name='createcourse'),
    url(r'^removecourse/(?P<courseId>\d+)$', group_required('Admins')(view_course.removeCourse), name='removecourse'),
    
    url(r'^editcoursetees/(?P<courseId>\d+)$', group_required('Admins')(view_course.editCourseTees), name='editcoursetees'),
    url(r'^getcoursetees/(?P<courseId>\d+)$', group_required('Admins', 'Directors')(view_course.getCourseTees), name='getcoursetees'),
    url(r'^updatecoursetee/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', group_required('Admins')(view_course.updateCourseTee), name='updatecoursetee'),
    url(r'^createcoursetee/(?P<courseId>\d+)$', group_required('Admins')(view_course.createCourseTee), name='createcoursetee'),
    url(r'^removecoursetee/(?P<courseTeeId>\d+)$', group_required('Admins')(view_course.removeCourseTee), name='removecoursetee'),
    
    url(r'^editcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', group_required('Admins')(view_course.editCourseTeeHoles), name='editcourseteeholes'),
    url(r'^getcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', group_required('Admins', 'Directors')(view_course.getCourseTeeHoles), name='getcourseteeholes'),
    url(r'^updatecourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)/(?P<teeId>\d+)$', group_required('Admins')(view_course.updateCourseTeeHole), name='updatecourseteehole'),
    url(r'^createcourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', group_required('Admins')(view_course.createCourseTeeHole), name='createcourseteehole'),
    url(r'^removecourseteehole/(?P<teeId>\d+)$', group_required('Admins')(view_course.removeCourseTeeHole), name='removecourseteehole'),
    
    url(r'^editplayers/$', group_required('Admins')(view_player.editPlayers), name='editplayers'),
    url(r'^getplayers/$', group_required('Admins', 'Directors')(view_player.getPlayers), name='getplayers'),
    url(r'^newplayer/$', group_required('Admins')(view_player.newPlayer), name='newplayer'),
    url(r'^loadplayers/$', group_required('Admins', 'Directors')(view_player.loadPlayers), name='loadplayers'),
    
    url(r'^editformats/$', group_required('Admins')(view_tournament.editFormats), name='editformats'),

    url(r'^newtournament/$', group_required('Admins', 'Directors')(view_tournament.newTournament), name='newtournament'),
    url(r'^tournament/$', group_required('Admins', 'Directors')(csrf_exempt(view_tournament.tournament)), name='tournament'),
    url(r'^clearrounddata/$', group_required('Admins')(view_tournament.clearRoundData), name='clearrounddata'),
    url(r'^edittournament/(?P<tournamentId>\d+)$', group_required('Admins')(view_tournament.tournament), name='edittournament'),
    url(r'^getscores/$', group_required('Directors')(view_tournament.getScores), name='getscores'),
    url(r'^getpayout/$', group_required('Admins', 'Directors')(view_tournament.getPayout), name='getpayout'),
    
    url(r'^updatescores/$', group_required('Admins')(view_tournament.updateScores), name='updatescores'),
    url(r'^leaderboard/(?P<tournamentId>\d+)$', group_required('Admins', 'Directors')(view_tournament.editTournament), name='edittournament'),
    
    url(r'^newscorecard/$', group_required('Admins', 'Directors')(view_scorecard.newScorecard), name='newscorecard'),
    url(r'^addplayertoscorecard/$', group_required('Admins', 'Directors')(view_scorecard.addPlayerToScorecard), name='addplayertoscorecard'),
    url(r'^addscoretoscorecard/$', group_required('Admins', 'Directors')(view_scorecard.addScoreToScorecard), name='addscoretoscorecard'),
    url(r'^addroundtoplayer/$', group_required('Admins', 'Directors')(view_player.addRoundToPlayer), name='addroundtoplayer'),
    
    url(r'^storesettings/$', group_required('Admins', 'Directors')(view_settings.storeSettings), name='storesettings'),
    
    url(r'^docs/$', view_documentation.docs, name='docs'),
    url(r'^docs/codestyle$', view_documentation.docscodestyle, name='docscodestyle'),
    url(r'^docs/install$', view_documentation.docsinstall, name='docsinstall'),
    url(r'^docs/editting$', view_documentation.docseditting, name='docseditting'),
]
