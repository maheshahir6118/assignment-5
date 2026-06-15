from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a DefaultRouter instance to automatically configure endpoints
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')
router.register(r'limit-restaurants', views.RestaurantLimitOffsetViewSet, basename='limit_restaurant')

urlpatterns = [
    path('', include(router.urls)),
]
