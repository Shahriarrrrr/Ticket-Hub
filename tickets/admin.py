from django.contrib import admin
from .models import BusTicket, Seat
# Register your models here.

admin.site.register(BusTicket)
admin.site.register(Seat)