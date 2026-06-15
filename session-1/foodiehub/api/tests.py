from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Restaurant
from .serializers import RestaurantSerializer

class SpotifyApiViewTests(APITestCase):
    """
    Unit tests for the hello_spotify API view.
    """
    def test_hello_spotify_url_resolves_and_returns_correct_message(self):
        url = reverse('hello_spotify')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {"message": "Hello, Spotify Fans!"}
        self.assertEqual(response.data, expected_data)

class RestaurantSerializerTests(TestCase):
    """
    Unit tests for the RestaurantSerializer.
    """
    def test_serializer_contains_expected_fields(self):
        restaurant = Restaurant(name="Punjab Grill", cuisine="North Indian")
        serializer = RestaurantSerializer(instance=restaurant)
        self.assertEqual(serializer.data['name'], "Punjab Grill")
        self.assertEqual(serializer.data['cuisine'], "North Indian")
        
    def test_serializer_validation(self):
        valid_data = {"name": "Barbeque Nation", "cuisine": "Buffet"}
        serializer = RestaurantSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        invalid_data = {"cuisine": "Buffet"}
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
