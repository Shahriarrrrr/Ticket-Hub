# tickets/serializers.py
from rest_framework import serializers
from tickets.models import CachedBusSearch

class CachedBusSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachedBusSearch
        fields = '__all__'
