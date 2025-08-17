from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Count, Q
# Create your models here.

class BaseTicket(models.Model):

    class TypeChoices(models.TextChoices):
        # Travel
        BUS = "BUS", "Bus"
        PLANE = "PLANE", "Plane"
        TRAIN = "TRAIN", "Train"
        FERRY = "FERRY", "Ferry"
        SUBWAY = "SUBWAY", "Subway"
        TRAM = "TRAM", "Tram"
        TAXI = "TAXI", "Taxi"
        SHUTTLE = "SHUTTLE", "Shuttle"
        RIDE_SHARE = "RIDE_SHARE", "Ride Share"
        # Cinema/Movies
        MOVIE = "MOVIE", "Movie"
        IMAX = "IMAX", "IMAX Movie"
        CINEMA_3D = "CINEMA_3D", "3D Cinema"
        CINEMA_4DX = "CINEMA_4DX", "4DX Cinema"
        DRIVE_IN = "DRIVE_IN", "Drive-in Movie"
        SHORT_FILM = "SHORT_FILM", "Short Film Screening"
        DOCUMENTARY = "DOCUMENTARY", "Documentary Screening"
        # Events / Concerts
        CONCERT = "CONCERT", "Concert"
        MUSIC_FESTIVAL = "MUSIC_FESTIVAL", "Music Festival"
        ART_EXHIBITION = "ART_EXHIBITION", "Art Exhibition"
        THEATER = "THEATER", "Theater Play"
        OPERA = "OPERA", "Opera"
        BALLET = "BALLET", "Ballet"
        STANDUP = "STANDUP", "Stand-up Comedy"
        WORKSHOP = "WORKSHOP", "Workshop"
        CONFERENCE = "CONFERENCE", "Conference"
        SEMINAR = "SEMINAR", "Seminar"
        MEETUP = "MEETUP", "Meetup Event"
        SPORT_MATCH = "SPORT_MATCH", "Sport Match"
        TOURNAMENT = "TOURNAMENT", "Tournament"
        # Attractions / Leisure
        AMUSEMENT_PARK = "AMUSEMENT_PARK", "Amusement Park"
        WATER_PARK = "WATER_PARK", "Water Park"
        ZOO = "ZOO", "Zoo"
        AQUARIUM = "AQUARIUM", "Aquarium"
        MUSEUM = "MUSEUM", "Museum"
        PLANETARIUM = "PLANETARIUM", "Planetarium"
        CINEMA_PASS = "CINEMA_PASS", "Cinema Pass"
        # Tours / Travel experiences
        CITY_TOUR = "CITY_TOUR", "City Tour"
        SIGHTSEEING = "SIGHTSEEING", "Sightseeing"
        CRUISE = "CRUISE", "Cruise"
        SAFARI = "SAFARI", "Safari"
        HIKING = "HIKING", "Hiking"
        ADVENTURE_TRIP = "ADVENTURE_TRIP", "Adventure Trip"
        MOUNTAIN_EXPEDITION = "MOUNTAIN_EXPEDITION", "Mountain Expedition"
        # Education / Classes
        ONLINE_COURSE = "ONLINE_COURSE", "Online Course"
        OFFLINE_COURSE = "OFFLINE_COURSE", "Offline Course"
        TRAINING = "TRAINING", "Training"
        CERTIFICATION = "CERTIFICATION", "Certification Program"
        # Fairs / Markets
        TRADE_FAIR = "TRADE_FAIR", "Trade Fair"
        FARMERS_MARKET = "FARMERS_MARKET", "Farmers Market"
        ART_CRAFT_FAIR = "ART_CRAFT_FAIR", "Art & Craft Fair"
        BOOK_FAIR = "BOOK_FAIR", "Book Fair"
        FOOD_FESTIVAL = "FOOD_FESTIVAL", "Food Festival"
        WINE_TASTING = "WINE_TASTING", "Wine Tasting"
        # Charity / Fundraising
        CHARITY_EVENT = "CHARITY_EVENT", "Charity Event"
        FUNDRAISER = "FUNDRAISER", "Fundraiser"
        AUCTION = "AUCTION", "Auction Event"
        # Fitness / Sports
        MARATHON = "MARATHON", "Marathon"
        FUN_RUN = "FUN_RUN", "Fun Run"
        CYCLING_EVENT = "CYCLING_EVENT", "Cycling Event"
        YOGA_CLASS = "YOGA_CLASS", "Yoga Class"
        FITNESS_CLASS = "FITNESS_CLASS", "Fitness Class"
        BOOTCAMP = "BOOTCAMP", "Bootcamp"
        # Miscellaneous
        VIRTUAL_EVENT = "VIRTUAL_EVENT", "Virtual Event"
        ONLINE_WEBINAR = "ONLINE_WEBINAR", "Webinar"
        KIDS_ACTIVITY = "KIDS_ACTIVITY", "Kids Activity"
        FAMILY_EVENT = "FAMILY_EVENT", "Family Event"
        PET_SHOW = "PET_SHOW", "Pet Show"
        FASHION_SHOW = "FASHION_SHOW", "Fashion Show"
        COMEDY_SHOW = "COMEDY_SHOW", "Comedy Show"
        GAMING_EVENT = "GAMING_EVENT", "Gaming Event"
        ESPORTS = "ESPORTS", "Esports Tournament"
        # Add more until 100+
        CARNIVAL = "CARNIVAL", "Carnival"
        PARADE = "PARADE", "Parade"
        WORKSHOP_KIDS = "WORKSHOP_KIDS", "Kids Workshop"
        TALK_SHOW = "TALK_SHOW", "Talk Show"
        CULTURAL_EVENT = "CULTURAL_EVENT", "Cultural Event"
        HISTORICAL_TOUR = "HISTORICAL_TOUR", "Historical Tour"
        CRUISE_DINNER = "CRUISE_DINNER", "Cruise Dinner"
        FOOD_COOKING_CLASS = "FOOD_COOKING_CLASS", "Cooking Class"
        PHOTO_EXHIBITION = "PHOTO_EXHIBITION", "Photo Exhibition"
        FILM_FESTIVAL = "FILM_FESTIVAL", "Film Festival"
        BOAT_RIDE = "BOAT_RIDE", "Boat Ride"
        HELICOPTER_RIDE = "HELICOPTER_RIDE", "Helicopter Ride"
        HOT_AIR_BALLOON = "HOT_AIR_BALLOON", "Hot Air Balloon Ride"
        SCUBA_DIVING = "SCUBA_DIVING", "Scuba Diving"
        SKYDIVING = "SKYDIVING", "Skydiving"
        PARAGLIDING = "PARAGLIDING", "Paragliding"
        WINTER_SPORTS = "WINTER_SPORTS", "Winter Sports"
        SKIING = "SKIING", "Skiing"
        SNOWBOARDING = "SNOWBOARDING", "Snowboarding"
        CAMPING = "CAMPING", "Camping"
        SURFING = "SURFING", "Surfing"
        MUSIC_CLASS = "MUSIC_CLASS", "Music Class"
        DANCE_CLASS = "DANCE_CLASS", "Dance Class"
        LANGUAGE_CLASS = "LANGUAGE_CLASS", "Language Class"
        ART_CLASS = "ART_CLASS", "Art Class"
        PHOTOGRAPHY_CLASS = "PHOTOGRAPHY_CLASS", "Photography Class"
        HACKATHON = "HACKATHON", "Hackathon"
        TECH_TALK = "TECH_TALK", "Tech Talk"
        STARTUP_EVENT = "STARTUP_EVENT", "Startup Event"
        BUSINESS_SEMINAR = "BUSINESS_SEMINAR", "Business Seminar"
        CAREER_FAIR = "CAREER_FAIR", "Career Fair"

    ticket_id = models.UUIDField(default=uuid.uuid4, unique=True, editable= False)
    name = models.CharField(max_length=255)
    ticket_type = models.CharField(max_length=50, choices=TypeChoices.choices, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=10, default="BDT")
    #available_seats = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    

    class Meta:
        abstract = True
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["ticket_type"]),
            models.Index(fields=["start_time"]),
        ]    
    def __str__(self):
        return f"{self.get_ticket_type_display()} - {self.name} ({self.price} {self.currency})"    


class Seat(models.Model):
    seat_number  = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    ticket = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.seat_number} - {'Booked' if self.is_booked else 'Available'}"


class BusTicket(BaseTicket):
    bus_name = models.CharField(max_length=255)
    bus_type = models.CharField(max_length=255)
    departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    bus_number = models.CharField(max_length=255)
    operator = models.CharField(max_length=255) #Driver needed as Foreign Key
    seats = GenericRelation(Seat)
    

    def available_seat_count(self):
        return self.seats.filter(is_booked = False).count()
    

class CachedBusSearch(models.Model):
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    date_of_journey = models.DateField()
    results = models.JSONField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['from_city', "to_city", 'date_of_journey'])
        ]
    def __str__(self):
        return f"{self.from_city} → {self.to_city} ({self.date_of_journey})"    