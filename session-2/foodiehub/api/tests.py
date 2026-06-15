from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Restaurant

class RestaurantAPITests(APITestCase):
    """
    Test suite verifying CRUD operations for both the APIView
    and GenericAPIView/Mixins implementations.
    """
    def setUp(self):
        # Create a sample restaurant for detail endpoint tests
        self.restaurant = Restaurant.objects.create(
            name="Zaffron Kitchen",
            cuisine="Indian",
            rating=4.2
        )
        # Define API URLs for raw APIView
        self.list_url = reverse('restaurant_list')
        self.detail_url = reverse('restaurant_detail', kwargs={'pk': self.restaurant.id})

        # Define API URLs for Mixins
        self.mixin_list_url = reverse('mixin_restaurant_list')
        self.mixin_detail_url = reverse('mixin_restaurant_detail', kwargs={'pk': self.restaurant.id})

    # ==========================================================================
    # APIView Tests
    # ==========================================================================
    def test_apiview_list_restaurants(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Zaffron Kitchen")

    def test_apiview_create_restaurant_success(self):
        payload = {"name": "Din Tai Fung", "cuisine": "Taiwanese", "rating": 4.7}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(response.data['name'], "Din Tai Fung")

    def test_apiview_create_restaurant_invalid_data(self):
        # Missing name field (should return bad request)
        payload = {"cuisine": "Taiwanese", "rating": 4.7}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apiview_retrieve_restaurant_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Zaffron Kitchen")

    def test_apiview_retrieve_restaurant_not_found(self):
        url = reverse('restaurant_detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apiview_update_restaurant(self):
        payload = {"name": "Zaffron Bistro", "cuisine": "Indian-Western Fusion", "rating": 4.3}
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Zaffron Bistro")
        self.assertEqual(self.restaurant.rating, 4.3)

    def test_apiview_partial_update_restaurant(self):
        payload = {"rating": 4.5}
        response = self.client.patch(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.rating, 4.5)
        self.assertEqual(self.restaurant.name, "Zaffron Kitchen") # unchanged

    def test_apiview_delete_restaurant(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 0)

    # ==========================================================================
    # GenericAPIView + Mixins Tests
    # ==========================================================================
    def test_mixin_list_restaurants(self):
        response = self.client.get(self.mixin_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mixin_create_restaurant(self):
        payload = {"name": "Tim Ho Wan", "cuisine": "Cantonese", "rating": 4.1}
        response = self.client.post(self.mixin_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mixin_retrieve_restaurant(self):
        response = self.client.get(self.mixin_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Zaffron Kitchen")

    def test_mixin_update_restaurant(self):
        payload = {"name": "Zaffron Modern", "cuisine": "Indian", "rating": 4.4}
        response = self.client.put(self.mixin_detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mixin_delete_restaurant(self):
        response = self.client.delete(self.mixin_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # standard destroy mixin status code
        self.assertEqual(Restaurant.objects.count(), 0)
