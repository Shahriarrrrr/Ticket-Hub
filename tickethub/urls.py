# tickethub/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- include is needed
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version="1.0.0",
        description="Api documentation of App"
    )
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tickets.api.urls')),  # all tickets app routes under /api/
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout = 0), name = "swagger-schema")
]
