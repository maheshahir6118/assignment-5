from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Restaurant

class RestaurantViewSetTests(APITestCase):
    """
    Test suite for Zomato-style Restaurant ViewSets.
    Verifies CRUD, Pagination, Filtering, and Sorting logic.
    """
    def setUp(self):
        # Create 5 dummy restaurants to test pagination (3 per page)
        self.r1 = Restaurant.objects.create(name="Trattoria", cuisine="Italian", location="Mumbai")
        self.r2 = Restaurant.objects.create(name="Zaffron", cuisine="Indian", location="Delhi")
        self.r3 = Restaurant.objects.create(name="Guzman", cuisine="Mexican", location="Bangalore")
        self.r4 = Restaurant.objects.create(name="Little Italy", cuisine="Italian", location="Pune")
        self.r5 = Restaurant.objects.create(name="Peshawri", cuisine="Indian", location="Chennai")

        # URL Endpoints
        self.list_url = reverse('restaurant-list')
        self.limit_list_url = reverse('limit_restaurant-list')

    # ==========================================================================
    # CRUD Tests
    # ==========================================================================
    def test_get_restaurant_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that page 1 has 3 items (since page_size=3)
        self.assertEqual(len(response.data['results']), 3)

    def test_create_restaurant(self):
        payload = {"name": "Wasabi", "cuisine": "Japanese", "location": "Mumbai"}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 6)

    def test_retrieve_restaurant(self):
        detail_url = reverse('restaurant-detail', kwargs={'pk': self.r1.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Trattoria")

    def test_update_restaurant(self):
        detail_url = reverse('restaurant-detail', kwargs={'pk': self.r1.id})
        payload = {"name": "Trattoria Milano", "cuisine": "Italian", "location": "Mumbai"}
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.r1.refresh_from_db()
        self.assertEqual(self.r1.name, "Trattoria Milano")

    def test_partial_update_restaurant(self):
        detail_url = reverse('restaurant-detail', kwargs={'pk': self.r1.id})
        payload = {"location": "Goa"}
        response = self.client.patch(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.r1.refresh_from_db()
        self.assertEqual(self.r1.location, "Goa")

    def test_delete_restaurant(self):
        detail_url = reverse('restaurant-detail', kwargs={'pk': self.r1.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 4)

    # ==========================================================================
    # Pagination Tests
    # ==========================================================================
    def test_page_number_pagination_page_1(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 3) # 3 per page

    def test_page_number_pagination_page_2(self):
        response = self.client.get(self.list_url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # remaining 2 items

    def test_limit_offset_pagination(self):
        # Limit = 2, Offset = 2 (Should return items 3 and 4, i.e. Guzman and Little Italy)
        response = self.client.get(self.limit_list_url, {'limit': 2, 'offset': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Guzman")

    # ==========================================================================
    # Filtering Tests
    # ==========================================================================
    def test_cuisine_filtering(self):
        response = self.client.get(self.list_url, {'cuisine': 'Italian'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: Pagination is active, but we only have 2 Italian items, so both should fit on Page 1.
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        for r in results:
            self.assertEqual(r['cuisine'], 'Italian')

    # ==========================================================================
    # Sorting / Ordering Tests
    # ==========================================================================
    def test_ordering_by_name_ascending(self):
        # Ordering alphabetically by name: Guzman (G), Little Italy (L), Peshawri (P), Trattoria (T), Zaffron (Z)
        response = self.client.get(self.list_url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['name'], "Guzman")
        self.assertEqual(results[1]['name'], "Little Italy")

    def test_ordering_by_cuisine_descending(self):
        # Ordering by cuisine descending: Mexican, Italian, Italian, Indian, Indian
        response = self.client.get(self.list_url, {'ordering': '-cuisine'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        # Mexican starts with M, Italian starts with I, Indian starts with I
        self.assertEqual(results[0]['cuisine'], "Mexican")
