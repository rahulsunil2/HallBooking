from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date


class Hall(models.Model):
    no = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=60)
    capacity = models.DecimalField(max_digits=3, decimal_places=0)
    inCharge = models.ForeignKey(User, models.PROTECT, default=1234)
    class Meta:
        verbose_name_plural = "Halls"

class Booking(models.Model):
    bId = models.AutoField(primary_key=True)
    sTime = models.DateTimeField(null=True, blank=True)
    eTime = models.DateTimeField(null=True, blank=True)
    hallNo = models.ForeignKey(Hall, models.CASCADE)
    fId = models.ForeignKey(User, models.SET_NULL, null=True)
    eventName = models.CharField(max_length=60)
    eventDetails = models.TextField('Event Details', blank=True)

    class Meta:
        verbose_name_plural = "Bookings"
