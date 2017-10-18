from django.contrib import admin

# Register your models here.

from .models import Tournament, TournamentRound, FormatPlugin, Player, Round, Score, Scorecard, Course, CourseTee, Tee, Hole, Club, Activity, PlayerPlugin


admin.site.register(Tournament)
admin.site.register(TournamentRound)
admin.site.register(FormatPlugin)
admin.site.register(Player)
admin.site.register(Round)
admin.site.register(Scorecard)
admin.site.register(Score)
admin.site.register(Course)
admin.site.register(CourseTee)
admin.site.register(Tee)
admin.site.register(Hole)
admin.site.register(Club)
admin.site.register(Activity)
admin.site.register(PlayerPlugin)
