from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^editcourses/$', views.editCourses, name='editcourses'),
    url(r'^getcourses/$', views.getCourses, name='getcourses'),
    url(r'^updatecourse/(?P<courseId>\d+)$', csrf_exempt(views.updateCourse), name='updatecourse'),
    url(r'^createcourse/$', csrf_exempt(views.createCourse), name='createcourse'),
    url(r'^removecourse/(?P<courseId>\d+)$', csrf_exempt(views.removeCourse), name='removecourse'),
    url(r'^editcoursetees/(?P<courseId>\d+)$', views.editCourseTees, name='editcoursetees'),
    url(r'^getcoursetees/(?P<courseId>\d+)$', views.getCourseTees, name='getcoursetees'),
    url(r'^updatecoursetee/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(views.updateCourseTee), name='updatecoursetee'),
    url(r'^createcoursetee/(?P<courseId>\d+)$', csrf_exempt(views.createCourseTee), name='createcoursetee'),
    url(r'^removecoursetee/(?P<courseTeeId>\d+)$', csrf_exempt(views.removeCourseTee), name='removecoursetee'),
    url(r'^editcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', views.editCourseTeeHoles, name='editcourseteeholes'),
    url(r'^getcourseteeholes/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', views.getCourseTeeHoles, name='getcourseteeholes'),
    url(r'^updatecourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)/(?P<teeId>\d+)$', csrf_exempt(views.updateCourseTeeHole), name='updatecourseteehole'),
    url(r'^createcourseteehole/(?P<courseId>\d+)/(?P<courseTeeId>\d+)$', csrf_exempt(views.createCourseTeeHole), name='createcourseteehole'),
    url(r'^removecourseteehole/(?P<teeId>\d+)$', csrf_exempt(views.removeCourseTeeHole), name='removecourseteehole'),
    url(r'^editplayers/$', views.editPlayers, name='editplayers'),
    url(r'^getplayers/$', csrf_exempt(views.getPlayers), name='getplayers'),
    url(r'^newplayer/$', views.newPlayer, name='newplayer'),
    url(r'^loadplayers/$', csrf_exempt(views.loadPlayers), name='loadplayers'),
    url(r'^printplayers/$', csrf_exempt(views.printPlayers), name='printplayers'),
    url(r'^printsignupsheets/$', csrf_exempt(views.printSignupSheets), name='printsignupsheets'),
    url(r'^editformats/$', views.editFormats, name='editformats'),
    url(r'^newtournament/$', csrf_exempt(views.newTournament), name='newtournament'),
    url(r'^edittournament/(?P<tournamentId>\d+)$', views.editTournament, name='edittournament'),
    url(r'^leaderboard/(?P<tournamentId>\d+)$', views.editTournament, name='edittournament'),
    url(r'^newscorecard/$', views.newScorecard, name='newscorecard'),
    url(r'^addplayertoscorecard/$', views.addPlayerToScorecard, name='addplayertoscorecard'),
    url(r'^addscoretoscorecard/$', views.addScoreToScorecard, name='addscoretoscorecard'),
    url(r'^addroundtoplayer/$', views.addRoundToPlayer, name='addroundtoplayer'),
]
