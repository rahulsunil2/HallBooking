from django.db import models

class Faculty(models.Model):
    id = models.DecimalField(unique=True)
    name = models.CharField(max_length=60)
    dept =  models.CharField(max_length=60)
    auth_level = models.DecimalField(max_digits=1)

class Halls(models.Model):
    no = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=60)
    capacity = models.DecimalField(max_digits=3)
    inCharge = models.ForeignKey(Faculty, models.SET_NULL, null=True)

class Bookings(models.Model):
    bId = models.DecimalField(unique=True)
    sTime = models.DateTimeField('Start Time')
    eTime = models.DateTimeField('End Time')
    hallNo = models.ForeignKey(Halls, models.CASCADE)
    fId = models.ForeignKey(Faculty, models.SET_NULL, null=True)
    eventName = models.CharField(max_length=60)
    eventDetails = models.TextField('Event Details', blank=True)
