from django.db import models
from datetime import date

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField()

class Room_Reservation(models.Model):
    res_date = models.DateField(default=date.today())
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()
    class Meta:
        unique_together = ('res_date', 'room',)