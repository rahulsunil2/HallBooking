from django.contrib import admin
from .models import Booking, Hall, Staff

# admin.site.register(Booking)
# admin.site.register(Hall)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'capacity', 'inCharge']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['bId','hallNo', 'fId', 'sTime', 'eTime', 'eventName', 'eventDetails','status']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['sId', 'name', 'email', 'hod']