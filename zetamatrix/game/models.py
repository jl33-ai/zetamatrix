from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    length = models.IntegerField(help_text="Length of game in seconds")
    is_dailychallenge = models.BooleanField(default=False)

class SolvedAddition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    time_taken = models.IntegerField(help_text="Time taken in milliseconds")

class SolvedSubtraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    time_taken = models.IntegerField(help_text="Time taken in milliseconds")

class SolvedMultiplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    time_taken = models.IntegerField(help_text="Time taken in milliseconds")

class SolvedDivision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    time_taken = models.IntegerField(help_text="Time taken in milliseconds")

class DailyChallenge(models.Model):
    date = models.DateField(unique=True)
    questions = models.JSONField(help_text="JSON field to store daily questions")
