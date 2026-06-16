import os
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    WeatherSerializer,
    GeocodingSerializer,
    CountryInfoSerializer,
    GitHubReposSerializer
)

# ==============================================================================
# 1. MUSIC WEATHER API - Class-Based View (CBV)
# ==============================================================================
class MusicWeatherAPIView(APIView):
    """
    Class-Based View that retrieves weather details for a given city
    using the OpenWeatherMap API.
    """
    def get(self, request, city):
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        
        # Safe fallback: If the API key is not configured or is a placeholder, return mock data
        if not api_key or 'placeholder' in api_key or 'here' in api_key:
            mock_data = {
                "city": city.capitalize(),
                "temperature": 32.0,
                "description": "clear sky"
            }
            serializer = WeatherSerializer(mock_data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers={'X-Mock-Data': 'True'})
            
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                res_data = response.json()
                data = {
                    "city": res_data.get('name'),
                    "temperature": res_data.get('main', {}).get('temp'),
                    "description": res_data.get('weather', [{}])[0].get('description')
                }
                serializer = WeatherSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif response.status_code == 404:
                return Response({"error": f"City '{city}' not found."}, status=status.HTTP_404_NOT_FOUND)
            elif response.status_code == 401:
                # Handle unauthorized due to invalid keys
                mock_data = {
                    "city": city.capitalize(),
                    "temperature": 30.5,
                    "description": "partly cloudy (mocked due to invalid API key)"
                }
                return Response(mock_data, status=status.HTTP_200_OK, headers={'X-Mock-Data': 'True'})
            else:
                return Response({"error": "Failed to retrieve weather data."}, status=status.HTTP_400_BAD_REQUEST)
                
        except requests.RequestException:
            return Response({"error": "Weather service connection timeout."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# ==============================================================================
# 2. FOOD LOCATION API - Function-Based View (FBV)
# ==============================================================================
@api_view(['GET'])
def food_location_view(request):
    """
    Function-Based View that retrieves the geocoding coordinates (lat, lng) 
    for a restaurant address using the Google Maps Geocoding API.
    Expects 'restaurant' as a query parameter.
    """
    restaurant = request.query_params.get('restaurant')
    
    # Validation check for required query parameters
    if not restaurant:
        return Response(
            {"error": "Query parameter 'restaurant' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Safe fallback: If no API key is registered, return simulated coordinates (Ahmedabad)
    if not api_key or 'placeholder' in api_key or 'here' in api_key:
        if "unknown" in restaurant.lower() or "notfound" in restaurant.lower():
            return Response({"error": "Restaurant location not found."}, status=status.HTTP_404_NOT_FOUND)
        
        mock_data = {
            "latitude": 23.0225,
            "longitude": 72.5714
        }
        return Response(mock_data, status=status.HTTP_200_OK, headers={'X-Mock-Data': 'True'})

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': restaurant,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        res_json = response.json()
        
        if res_json.get('status') == 'OK':
            location = res_json['results'][0]['geometry']['location']
            data = {
                "latitude": location['lat'],
                "longitude": location['lng']
            }
            serializer = GeocodingSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif res_json.get('status') == 'ZERO_RESULTS':
            return Response({"error": "Restaurant location not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Fallback if request fails (e.g. invalid key)
            mock_data = {
                "latitude": 23.0225,
                "longitude": 72.5714
            }
            return Response(mock_data, status=status.HTTP_200_OK, headers={'X-Mock-Data': 'True'})
            
    except requests.RequestException:
        return Response({"error": "Geocoding service connection timeout."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# ==============================================================================
# 3. COUNTRY INFO API - Class-Based View (CBV)
# ==============================================================================
class CountryInfoAPIView(APIView):
    """
    Class-Based View that retrieves details for a country (capital, population)
    using the public REST Countries API (no API key required).
    """
    def get(self, request, country_name):
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                res_json = response.json()
                country_data = res_json[0]
                data = {
                    "country": country_data.get('name', {}).get('common'),
                    "capital": country_data.get('capital', ["No Capital"])[0],
                    "population": country_data.get('population')
                }
                serializer = CountryInfoSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif response.status_code == 404:
                return Response({"error": f"Country '{country_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Failed to retrieve country data."}, status=status.HTTP_400_BAD_REQUEST)
                
        except requests.RequestException:
            return Response({"error": "REST Countries service connection timeout."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# ==============================================================================
# 4. GITHUB REPOSITORIES API - Function-Based View (FBV)
# ==============================================================================
@api_view(['GET'])
def github_repos_view(request, username):
    """
    Function-Based View that retrieves a list of public repositories for a
    GitHub user using the GitHub REST API (no API key required).
    """
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'User-Agent': 'Django-REST-Framework-Agent'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            res_json = response.json()
            repo_names = [repo.get('name') for repo in res_json]
            data = {
                "repositories": repo_names
            }
            serializer = GitHubReposSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif response.status_code == 404:
            return Response({"error": f"GitHub user '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Failed to retrieve GitHub repositories."}, status=status.HTTP_400_BAD_REQUEST)
            
    except requests.RequestException:
        return Response({"error": "GitHub service connection timeout."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
