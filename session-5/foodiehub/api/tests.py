from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ThirdPartyAPITests(APITestCase):
    """
    Test suite for third-party API integration views.
    Uses patching to mock external HTTP requests.
    """
    def setUp(self):
        self.weather_url = reverse('music_weather', kwargs={'city': 'ahmedabad'})
        self.location_url = reverse('food_location')
        self.country_url = reverse('country_info', kwargs={'country_name': 'india'})
        self.github_url = reverse('github_repos', kwargs={'username': 'octocat'})

    # ==========================================================================
    # 1. Music Weather API tests
    # ==========================================================================
    def test_music_weather_fallback_execution(self):
        # By default, since the API key is not configured, it triggers the fallback mock data
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'Ahmedabad')
        self.assertIn('temperature', response.data)
        self.assertIn('description', response.data)
        self.assertEqual(response.headers.get('X-Mock-Data'), 'True')

    # ==========================================================================
    # 2. Food Location API tests
    # ==========================================================================
    def test_food_location_fallback_execution(self):
        # Triggers fallback mock geocode data
        response = self.client.get(self.location_url, {'restaurant': 'McDonalds'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('latitude', response.data)
        self.assertIn('longitude', response.data)
        self.assertEqual(response.headers.get('X-Mock-Data'), 'True')

    def test_food_location_missing_parameter_fails(self):
        # Missing query parameter 'restaurant' should return 400 Bad Request
        response = self.client.get(self.location_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_food_location_not_found_fallback(self):
        # Triggers a 404 for unknown search keywords under fallback rules
        response = self.client.get(self.location_url, {'restaurant': 'unknown-restaurant'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==========================================================================
    # 3. Country Info API tests
    # ==========================================================================
    @patch('requests.get')
    def test_country_info_success(self, mock_get):
        # Mock REST Countries response payload
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'name': {'common': 'India'},
            'capital': ['New Delhi'],
            'population': 1400000000
        }]
        
        response = self.client.get(self.country_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country'], 'India')
        self.assertEqual(response.data['capital'], 'New Delhi')
        self.assertEqual(response.data['population'], 1400000000)

    @patch('requests.get')
    def test_country_info_not_found(self, mock_get):
        # Mock 404 returned from external API
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        
        url = reverse('country_info', kwargs={'country_name': 'invalidcountry'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    # ==========================================================================
    # 4. GitHub Repositories API tests
    # ==========================================================================
    @patch('requests.get')
    def test_github_repos_success(self, mock_get):
        # Mock GitHub API response payload
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'react'},
            {'name': 'react-native'}
        ]
        
        response = self.client.get(self.github_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['repositories'], ['react', 'react-native'])

    @patch('requests.get')
    def test_github_repos_user_not_found(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        
        url = reverse('github_repos', kwargs={'username': 'invaliduser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
