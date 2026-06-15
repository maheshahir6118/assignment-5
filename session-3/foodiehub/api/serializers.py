from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for the Restaurant model.
    Maps fields: id, name, cuisine, and location.
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'location']
