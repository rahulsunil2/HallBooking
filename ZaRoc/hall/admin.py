from django.contrib import admin
from .models import Booking, Hall

# admin.site.register(Booking)
# admin.site.register(Hall)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'capacity', 'inCharge']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['bId', 'sTime', 'eTime', 'hallNo', 'fId', 'eventName', 'eventDetails','status']