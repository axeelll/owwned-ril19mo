from django.db import models
from django.conf import settings
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # team = models.ForeignKey(

    #     on_delete=models.SET_NULL,
    # )
