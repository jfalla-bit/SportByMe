from django.db import models

class TeamModel(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE)
    coach = models.ForeignKey('CoachModel', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'