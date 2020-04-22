from django.db import models
from django.contrib.auth.models import User

class Hall(models.Model):
    no = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=60)
    capacity = models.DecimalField(max_digits=3, decimal_places=0)
    inCharge = models.ForeignKey(User, models.PROTECT)
    class Meta:
        verbose_name_plural = "Halls"

class Booking(models.Model):
    bId = models.DecimalField(
        primary_key=True, decimal_places=0, max_digits=10)
    sTime = models.DateTimeField('Start Time')
    eTime = models.DateTimeField('End Time')
    hallNo = models.ForeignKey(Hall, models.CASCADE)
    fId = models.ForeignKey(User, models.SET_NULL, null=True)
    eventName = models.CharField(max_length=60)
    eventDetails = models.TextField('Event Details', blank=True)

    class Meta:
        verbose_name_plural = "Bookings"
