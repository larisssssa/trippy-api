from django.db import models
from django.conf import settings
from .trip import Trip


class TripUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "trip")
