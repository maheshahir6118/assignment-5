from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that maps the Zomato-style Restaurant model fields
    (name and cuisine) into serialized JSON data and handles validation.
    """
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine']


