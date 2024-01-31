from django.contrib import admin
from .models import GameSession, SolvedAddition, SolvedDivision, SolvedMultiplication, SolvedSubtraction, DailyChallenge
from accounts.models import PlayerStats
# Register your models here.
admin.site.register(GameSession)
admin.site.register(SolvedAddition)
admin.site.register(SolvedSubtraction)
admin.site.register(SolvedMultiplication)
admin.site.register(SolvedDivision)
admin.site.register(DailyChallenge)
admin.site.register(PlayerStats)