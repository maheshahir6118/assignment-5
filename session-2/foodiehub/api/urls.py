from django.urls import path
from . import views

urlpatterns = [
    # 1. APIView CRUD Implementation Routes (Primary assignment URLs)
    path('restaurants/', views.RestaurantListAPIView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailAPIView.as_view(), name='restaurant_detail'),

    # 2. GenericAPIView & Mixins CRUD Implementation Routes (Refactored assignment URLs)
    path('mixins/restaurants/', views.RestaurantListMixinView.as_view(), name='mixin_restaurant_list'),
    path('mixins/restaurants/<int:pk>/', views.RestaurantDetailMixinView.as_view(), name='mixin_restaurant_detail'),
]
