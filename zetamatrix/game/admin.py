from django.contrib import admin
from .models import GameSession, SolvedAddition, SolvedDivision, SolvedMultiplication, SolvedSubtraction, DailyChallenge
# Register your models here.
admin.site.register(GameSession)
admin.site.register(SolvedAddition)
admin.site.register(SolvedSubtraction)
admin.site.register(SolvedMultiplication)
admin.site.register(SolvedDivision)
admin.site.register(DailyChallenge)