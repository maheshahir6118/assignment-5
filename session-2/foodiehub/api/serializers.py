from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for mapping the Restaurant database model.
    Inherits fields name, cuisine, and rating automatically.
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'rating']
