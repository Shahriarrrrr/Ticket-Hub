# tickethub/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- include is needed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tickets.api.urls')),  # all tickets app routes under /api/
]
