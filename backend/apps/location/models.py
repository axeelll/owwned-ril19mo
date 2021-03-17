from django.db import models


class Building(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s %s' % (self.name, self.address)


class Floor(models.Model):
    batiment = models.ForeignKey(
        Building, related_name="floors", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    def __str__(self):
        return self.name


class Room(models.Model):
    floor = models.ForeignKey(
        Floor, related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
