from django.db import models
from ..team.models import Team
from ..location.models import Room
from ..supplier.models import Supplier
# Create your models here.


class Asset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    picture = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=16, decimal_places=2)
    # supplier = models.ForeignKey()
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
