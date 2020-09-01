from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Version)
admin.site.register(Map)
admin.site.register(MapPool)
admin.site.register(BombSpot)
admin.site.register(Operator)
admin.site.register(League)
admin.site.register(LeagueGroup)
admin.site.register(Season)


class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Team, TeamAdmin)
admin.site.register(Sponsor)
admin.site.register(MatchState)
admin.site.register(Match)
admin.site.register(MapBan)
admin.site.register(MapPlayOrder)
admin.site.register(MapWins)
admin.site.register(MapSettings)
admin.site.register(OperatorBans)
admin.site.register(WinType)
admin.site.register(Round)
