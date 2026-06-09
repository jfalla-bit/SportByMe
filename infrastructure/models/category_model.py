from django.db import models

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'