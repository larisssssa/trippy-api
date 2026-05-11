from django.db import models
from .category import Category


class Attraction(models.Model):
    name = models.CharField()
    description = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    imageurl = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
