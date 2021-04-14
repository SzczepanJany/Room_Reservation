from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField()

