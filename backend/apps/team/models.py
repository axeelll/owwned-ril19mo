from django.db import models
from django.conf import settings

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null = True, blank= True)
    def __str__(self):
        return self.name