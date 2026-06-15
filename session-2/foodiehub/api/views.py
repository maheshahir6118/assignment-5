from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from .models import Restaurant
from .serializers import RestaurantSerializer

# ==============================================================================
# IMPLEMENTATION 1: CRUD APIs using raw APIView (Manual Control)
# ==============================================================================

class RestaurantListAPIView(APIView):
    """
    Handles listing all restaurants (GET) and creating a new restaurant (POST)
    using raw APIView.
    """
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailAPIView(APIView):
    """
    Handles retrieving (GET), updating (PUT/PATCH), and deleting (DELETE)
    a specific restaurant instance by id using raw APIView.
    """
    def get_object(self, pk):
        # Automatically triggers 404 response if object is not found
        return get_object_or_404(Restaurant, pk=pk)

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        # Returns HTTP 200 OK as requested by the status code instructions,
        # with a success confirmation body.
        return Response(
            {"message": "Restaurant deleted successfully."},
            status=status.HTTP_200_OK
        )


# ==============================================================================
# IMPLEMENTATION 2: Refactored CRUD APIs using GenericAPIView and Mixins
# ==============================================================================

class RestaurantListMixinView(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    Refactored version of the List/Create endpoint using GenericAPIView
    and DRF's list and create mixins.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RestaurantDetailMixinView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """
    Refactored version of the Retrieve/Update/Destroy endpoint using
    GenericAPIView and DRF's retrieve, update, and destroy mixins.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
