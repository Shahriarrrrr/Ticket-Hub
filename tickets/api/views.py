from rest_framework.decorators import api_view
from rest_framework.response import Response
from scraping.scrapers.buses import scrape_shohoz_buses
from django.core.cache import cache
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('from_city', openapi.IN_QUERY, description="Departure city", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('to_city', openapi.IN_QUERY, description="Destination city", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('date_of_journey', openapi.IN_QUERY, description="Date of journey in format dd-MMM-yyyy (e.g., 28-Aug-2025)", type=openapi.TYPE_STRING, required=True),
    ]
)
@api_view(['GET'])
def search_buses(request):
    from_city = request.GET.get("from_city")
    to_city = request.GET.get("to_city")
    date_str = request.GET.get("date_of_journey")

    if not from_city or not to_city or not date_str:
        return Response({"error": "from_city, to_city, and date_of_journey are required"}, status=400)

    date_str = date_str.strip('"')
    try:
        date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use dd-MMM-yyyy, e.g., 28-Aug-2025"}, status=400)

    # Redis key: unique per from_city, to_city, date
    cache_key = f"buses:{from_city.lower()}:{to_city.lower()}:{date_str}"

    # Try getting data from Redis first
    buses = cache.get(cache_key)
    if buses:
        print("Cache hit")
        return Response(buses)

    # Cache miss → fetch fresh data
    buses = scrape_shohoz_buses(from_city, to_city, date_str)

    # Save to Redis for 10 minutes
    if buses:
        cache.set(cache_key, buses, timeout=600)  # timeout in seconds

    return Response(buses)