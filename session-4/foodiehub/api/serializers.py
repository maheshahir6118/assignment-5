from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Playlist, Order, CartItem, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PlaylistSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'owner']


class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product_name', 'price', 'buyer']


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'item_name', 'quantity', 'user']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event_name', 'price']
