# tickets/urls.py
from django.urls import path
from .views import search_buses

urlpatterns = [
    path('search-buses/', search_buses, name='search-buses'),
]
