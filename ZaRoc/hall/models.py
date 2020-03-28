from django.db import models

class Faculty(models.Model):
    id = models.DecimalField(primary_key=True, decimal_places=0, max_digits=10)
    name = models.CharField(max_length=60)
    dept =  models.CharField(max_length=60)
    auth_level = models.DecimalField(max_digits=1, decimal_places=0)

    class Meta:
        verbose_name_plural = "Faculties"

class Hall(models.Model):
    no = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=60)
    capacity = models.DecimalField(max_digits=3, decimal_places=0)
    inCharge = models.ForeignKey(Faculty, models.PROTECT, default=1234)

    class Meta:
        verbose_name_plural = "Halls"

class Booking(models.Model):
    bId = models.DecimalField(
        primary_key=True, decimal_places=0, max_digits=10)
    sTime = models.DateTimeField('Start Time')
    eTime = models.DateTimeField('End Time')
    hallNo = models.ForeignKey(Hall, models.CASCADE)
    fId = models.ForeignKey(Faculty, models.SET_NULL, null=True)
    eventName = models.CharField(max_length=60)
    eventDetails = models.TextField('Event Details', blank=True)

    class Meta:
        verbose_name_plural = "Bookings"
