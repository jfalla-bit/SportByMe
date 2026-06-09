from django.db import models

class MatchModel(models.Model):
    home_team = models.ForeignKey('TeamModel', on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey('TeamModel', on_delete=models.CASCADE, related_name='away_matches')
    tournament = models.ForeignKey('TournamentModel', on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'