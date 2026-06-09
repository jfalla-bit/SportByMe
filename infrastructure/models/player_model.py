from django.db import models

class PlayerModel(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    position = models.CharField(max_length=50)
    team = models.ForeignKey('TeamModel', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'players'