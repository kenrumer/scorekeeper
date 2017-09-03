from django.contrib import admin

# Register your models here.

from .models import Tournament, TournamentDate, Format, Player, PlayerType, Round, Score, Course, CourseTee, Tee, Hole, Club, PlayerPlugin


admin.site.register(Tournament)
admin.site.register(TournamentDate)
admin.site.register(Format)
admin.site.register(Player)
admin.site.register(PlayerType)
admin.site.register(Round)
admin.site.register(Score)
admin.site.register(Course)
admin.site.register(CourseTee)
admin.site.register(Tee)
admin.site.register(Hole)
admin.site.register(Club)
admin.site.register(PlayerPlugin)
