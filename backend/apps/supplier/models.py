from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name
