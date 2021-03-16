from django.db import models
from django.conf import settings
# Create your models here.


class HistoryEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    # asset = models.ForeignKey(
    #     settings.AUTH_ASSET_MODEL,
    #     on_delete=models.CASCADE,
    # )
    start_date = models.DateTimeField()  # DateTimeField
    end_date = models.DateTimeField()
    event_type = models.CharField(max_length=200),
    description = models.CharField(max_length=200)

    class EventType(models.TextChoices):
        LEND = 'LE', 'Lend'
        MAINTENANCE = 'MA',  'Maintenance'
        OTHER = 'OT', 'Other'

    event_type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.LEND,
    )

    def __str__(self):
        return self.name
