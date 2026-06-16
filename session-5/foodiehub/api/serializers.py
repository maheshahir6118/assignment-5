from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    """
    Serializer to validate and format OpenWeatherMap response data.
    """
    city = serializers.CharField(max_length=255)
    temperature = serializers.FloatField(help_text="Temperature in Celsius.")
    description = serializers.CharField(max_length=255, help_text="Weather description.")


class GeocodingSerializer(serializers.Serializer):
    """
    Serializer to format Google Maps Geocoding response data.
    """
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class CountryInfoSerializer(serializers.Serializer):
    """
    Serializer to format REST Countries response data.
    """
    country = serializers.CharField(max_length=255)
    capital = serializers.CharField(max_length=255)
    population = serializers.IntegerField()


class GitHubReposSerializer(serializers.Serializer):
    """
    Serializer to format GitHub public repositories response data.
    """
    repositories = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of public repository names."
    )
