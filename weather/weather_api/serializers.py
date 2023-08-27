from rest_framework import serializers

from weather_api.models import Locations


class WeatherForecastSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
    description = serializers.CharField(max_length=200)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'  # Use specific fields if needed

class LocationWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['name'] 