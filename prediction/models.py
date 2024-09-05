from django.db import models

# Create your models here.
# predictor/models.py
""" 
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    match_hour = models.TimeField()
    winner = models.ForeignKey(Team, related_name='won_matches', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team}"
 """