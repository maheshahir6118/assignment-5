from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# Set up routers
router = DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'cart', views.CartItemViewSet, basename='cart')
router.register(r'tickets', views.TicketViewSet, basename='ticket')

urlpatterns = [
    # Automated CRUD endpoints
    path('', include(router.urls)),
    
    # Endpoint to generate/retrieve auth token using POST (username and password)
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
