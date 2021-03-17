from django.db import models
from apps.asset.models import Asset


class Documentation(models.Model):
    name = models.CharField(max_length=200)
    descripstion = models.TextField()
    url = models.URLField()
    doc_file = models.FileField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
