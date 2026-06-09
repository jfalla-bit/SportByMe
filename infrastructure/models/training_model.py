from django.db import models

class TrainingModel(models.Model):
    team = models.ForeignKey('TeamModel', on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trainings'