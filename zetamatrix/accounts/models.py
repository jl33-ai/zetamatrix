from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExtraInformation(models.Model):
    # Collect optional additional data about users such as: gender, age, industry, interests, ethnicity. 
    pass


class PlayerStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games_played = models.IntegerField()
    questions_answered = models.IntegerField()
    has_world_record = models.BooleanField()
    has_come_top_50_daily_challenge = models.BooleanField()