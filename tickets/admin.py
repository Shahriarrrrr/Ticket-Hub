from django.contrib import admin
from .models import BusTicket, Seat, CachedBusSearch
# Register your models here.

admin.site.register(BusTicket)
admin.site.register(Seat)
admin.site.register(CachedBusSearch)