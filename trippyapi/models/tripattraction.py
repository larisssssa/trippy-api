from django.db import models
from .trip import Trip
from .attraction import Attraction
from django.conf import settings


class TripAttraction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("attraction", "trip")
