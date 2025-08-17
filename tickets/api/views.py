from rest_framework.decorators import api_view
from rest_framework.response import Response
from tickets.models import CachedBusSearch
from scraping.scrapers.buses import scrape_shohoz_buses
from django.utils import timezone
from datetime import timedelta, datetime

@api_view(['GET'])
def search_buses(request):
    # 1. Get query params
    from_city = request.GET.get("from_city")
    to_city = request.GET.get("to_city")
    date_str = request.GET.get("date_of_journey")  # e.g., '28-Aug-2025'
    
    if not from_city or not to_city or not date_str:
        return Response({"error": "from_city, to_city, and date_of_journey are required"}, status=400)

    # Remove surrounding quotes if present
    date_str = date_str.strip('"')
    
    try:
        # Convert to datetime.date object
        date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use dd-MMM-yyyy, e.g., 28-Aug-2025"}, status=400)

    # 2. Check cache (valid for 15 minutes)
    cache_duration = timedelta(minutes=10)
    cache = CachedBusSearch.objects.filter(
        from_city__iexact=from_city,
        to_city__iexact=to_city,
        date_of_journey=date_obj
    ).order_by('-fetched_at').first()

    if cache and cache.fetched_at + cache_duration > timezone.now():
        print("Time not up")
        return Response(cache.results)

    # 3. Fetch fresh data from Shohoz
    date_for_api = date_obj.strftime("%Y-%m-%d")  # format Shohoz expects
    print(f"IN{date_str}")
    buses = scrape_shohoz_buses(from_city, to_city, date_str)

    # 4. Save to cache
    if buses:  # only cache if we got results
        CachedBusSearch.objects.create(
            from_city=from_city,
            to_city=to_city,
            date_of_journey=date_obj,
            results=buses
        )

    return Response(buses)
