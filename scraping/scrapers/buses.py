# import requests
# import json
# from tickets.models import BusTicket, Seat

# def scrape_buses_all_bd_tickets():
#     url = "https://api.bdtickets.com:20102/v1/coaches/search"

#     payload = {
#         "date": "2025-08-28",
#         "identifier": "dhaka-to-chittagong",
#         "structureType": "BUS"
#     }

#     headers = {
#         "Content-Type": "application/json",
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code != 200:
#         print(f"Failed to fetch data: {response.status_code}")
#         return

#     data = response.json()

#     # 1️⃣ Save full JSON to file
#     with open("buses.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
#     print("Full JSON saved to buses.json")

#     # 2️⃣ Generate a readable table summary
#     coaches = data.get("coaches", [])
#     if not coaches:
#         print("No bus data found.")
#         return

#     with open("buses_summary.txt", "w", encoding="utf-8") as f:
#         f.write(f"{'Bus Name':30} {'Departure':10} {'Arrival':10} {'Price (BDT)':10}\n")
#         f.write("="*70 + "\n")
#         for bus in coaches:
#             name = bus.get("name", "N/A")
#             dep = bus.get("departureTime", "N/A")
#             arr = bus.get("arrivalTime", "N/A")
#             price = bus.get("price", "N/A")
#             line = f"{name:30} {dep:10} {arr:10} {price:10}\n"
#             f.write(line)
    
#     print("Bus summary saved to buses_summary.txt")
#     print(f"Total buses fetched: {len(coaches)}")


#     url = "https://api.bdtickets.com:20102/v1/coaches/search"

#     payload = {
#         "from_city": "Dhaka",
#         "to_city": "Chittagong",
#         "date_of_journey": "28-Aug-2025"
#     }

#     headers = {
#         "Content-Type": "application/json",
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code != 200:
#         print(f"Failed to fetch data: {response.status_code}")
#         return

#     data = response.json()

#     # 1️⃣ Save full JSON to file
#     with open("buses.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
#     print("Full JSON saved to buses.json")

#     # 2️⃣ Generate a readable table summary
#     coaches = data.get("coaches", [])
#     if not coaches:
#         print("No bus data found.")
#         return

#     with open("buses_summary.txt", "w", encoding="utf-8") as f:
#         f.write(f"{'Bus Name':30} {'Departure':10} {'Arrival':10} {'Price (BDT)':10}\n")
#         f.write("="*70 + "\n")
#         for bus in coaches:
#             name = bus.get("name", "N/A")
#             dep = bus.get("departureTime", "N/A")
#             arr = bus.get("arrivalTime", "N/A")
#             price = bus.get("price", "N/A")
#             line = f"{name:30} {dep:10} {arr:10} {price:10}\n"
#             f.write(line)
    
#     print("Bus summary saved to buses_summary.txt")
#     print(f"Total buses fetched: {len(coaches)}")

# def scrape_shohoz_buses():
#     url = "https://webapi.shohoz.com/v1.0/web/booking/bus/search-trips"

#     # Query string parameters
#     params = {
#         "from_city": "Dhaka",
#         "to_city": "Chittagong",
#         "date_of_journey": "28-Aug-2025",
#         "dor": ""  # optional, just pass empty if not needed
#     }

#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         # Save full JSON to file
#         with open("shohoz_buses.json", "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)
#         print("Full JSON saved to shohoz_buses.json")

#         # Optional: print summary of buses
#         trips = data.get("trips", [])
#         if trips:
#             print(f"{'Bus Name':30} {'Departure':10} {'Arrival':10} {'Price (BDT)':10}")
#             print("="*70)
#             for bus in trips:
#                 name = bus.get("service_name", "N/A")
#                 dep = bus.get("departure_time", "N/A")
#                 arr = bus.get("arrival_time", "N/A")
#                 price = bus.get("ticket_price", {}).get("total_fare", "N/A")
#                 print(f"{name:30} {dep:10} {arr:10} {price:10}")
#         else:
#             print("No bus data found.")
#     else:
#         print(f"Failed to fetch data: {response.status_code}")

# # Run the scraper
# scrape_shohoz_buses()
# # Run the scraper



import os
print("DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tickethub.settings")
print("DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"))
django.setup()  # must come before any Django imports

import requests
from datetime import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from tickets.models import BusTicket, Seat










def scrape_shohoz_buses(from_city, to_city, date_of_journey):
    print("Hitting")
    url = "https://webapi.shohoz.com/v1.0/web/booking/bus/search-trips"
    params = {
        "from_city": from_city,
        "to_city": to_city,
        "date_of_journey": date_of_journey,
        "dor": ""
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    data = response.json()
    trips = data.get("data", {}).get("trips", {}).get("list", [])

    if not trips:
        print("No bus data found.")
        return []

    buses_list = []  # <- create a list to return
    bus_ct = ContentType.objects.get_for_model(BusTicket)  # Needed for GenericForeignKey

    for trip in trips:
        try:
            start_time = datetime.strptime(
                f"{trip['departure_date']} {trip['departure_time']}", "%Y-%m-%d %H:%M:%S"
            )
            end_time = datetime.strptime(
                f"{trip['arrival_date']} {trip['arrival_time']}", "%Y-%m-%d %H:%M:%S"
            )

            ticket, created = BusTicket.objects.update_or_create(
                bus_number=trip['trip_number'],
                defaults={
                    "bus_name": trip['company_name'],
                    "bus_type": trip.get('bus_desc', ''),
                    "departure": trip['origin_city_name'].title(),
                    "destination": trip['destination_city_name'].title(),
                    "operator": trip['company_name'],
                    "start_time": start_time,
                    "end_time": end_time,
                    "price": Decimal(trip['economy_class_fare']),
                    "ticket_type": "BUS",
                    "currency": "BDT"
                }
            )

            # Remove old seats and create fresh
            ticket.seats.all().delete()
            no_of_seats = int(trip.get('noOfSeatsAvailable', 0))
            for seat_num in range(1, no_of_seats + 1):
                Seat.objects.create(
                    seat_number=str(seat_num),
                    is_booked=False,
                    content_type=bus_ct,
                    object_id=ticket.id
                )

            # Append data to list
            buses_list.append({
                "bus_name": ticket.bus_name,
                "departure": start_time.strftime("%H:%M"),
                "arrival": end_time.strftime("%H:%M"),
                "price": float(ticket.price)
            })

        except Exception as e:
            print(f"Error processing bus {trip.get('trip_number')}: {e}")

    return buses_list  # <- return the list

if __name__ == "__main__":
    from_city = input("Enter origin city: ")
    to_city = input("Enter destination city: ")
    date_of_journey = input("Enter journey date (dd-MMM-yyyy, e.g. 28-Aug-2025): ")
    
    scrape_shohoz_buses(from_city, to_city, date_of_journey)
