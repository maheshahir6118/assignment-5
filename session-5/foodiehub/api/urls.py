from django.urls import path
from . import views

urlpatterns = [
    # 1. Music Weather API endpoint (Class-Based View)
    path('music-weather/<str:city>/', views.MusicWeatherAPIView.as_view(), name='music_weather'),
    
    # 2. Food Location API endpoint (Function-Based View)
    path('food-location/', views.food_location_view, name='food_location'),
    
    # 3. Country Info API endpoint (Class-Based View)
    path('country-info/<str:country_name>/', views.CountryInfoAPIView.as_view(), name='country_info'),
    
    # 4. GitHub Repositories API endpoint (Function-Based View)
    path('github-repos/<str:username>/', views.github_repos_view, name='github_repos'),
]
