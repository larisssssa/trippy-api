from django.db import models
from models import Category


class Attraction(models.Model):
    name = models.CharField()
    description = models.TextField()
    imageurl = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
