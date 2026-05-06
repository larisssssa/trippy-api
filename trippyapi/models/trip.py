"""Trip model"""

from django.db import models
from django.conf import settings


class Trip(models.Model):
    name = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    return_date = models.DateField(default="0000-00-00")
    imageurl = models.CharField()
    creatorId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
