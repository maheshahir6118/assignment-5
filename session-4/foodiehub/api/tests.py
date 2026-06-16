import base64
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Playlist, Order, CartItem, Ticket

class AuthenticationPermissionsTests(APITestCase):
    """
    Test suite verifying security, authentication schemes,
    and custom premium permissions.
    """
    def setUp(self):
        # Create users: normal user, premium user
        self.normal_user = User.objects.create_user(
            username="normaluser", password="normalpassword"
        )
        self.premium_user = User.objects.create_user(
            username="premiumuser", password="premiumpassword"
        )
        # Set premium flag
        self.premium_user.profile.is_premium = True
        self.premium_user.profile.save()

        # Create dummy playlists, orders, carts, tickets
        self.playlist = Playlist.objects.create(name="Workout Chill", owner=self.normal_user)
        self.order = Order.objects.create(product_name="Pizza", price=450.00, buyer=self.normal_user)
        self.cart_item = CartItem.objects.create(item_name="Biryani", quantity=2, user=self.normal_user)
        self.ticket = Ticket.objects.create(event_name="Coldplay VIP", price=5000.00)

        # Generate tokens
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.premium_token = Token.objects.create(user=self.premium_user)

        # View URLs
        self.playlist_list_url = reverse('playlist-list')
        self.order_list_url = reverse('order-list')
        self.cart_list_url = reverse('cart-list')
        self.ticket_list_url = reverse('ticket-list')

    # ==========================================================================
    # 1. Basic Authentication Tests (Playlist Endpoint)
    # ==========================================================================
    def test_playlist_without_auth_fails(self):
        response = self.client.get(self.playlist_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_playlist_with_basic_auth_success(self):
        # Encode Basic auth credentials: normaluser:normalpassword
        credentials = "normaluser:normalpassword"
        encoded_creds = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {encoded_creds}')
        
        response = self.client.get(self.playlist_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ==========================================================================
    # 2. Token Authentication Tests (Order Endpoint)
    # ==========================================================================
    def test_orders_without_token_fails(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_with_invalid_token_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_with_valid_token_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.normal_token.key}')
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], "Pizza")

    # ==========================================================================
    # 3. Session Authentication Tests (Cart Endpoint)
    # ==========================================================================
    def test_cart_without_session_fails(self):
        response = self.client.get(self.cart_list_url)
        # Session authentication without login returns 403 Forbidden for authenticated permissions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cart_with_session_login_success(self):
        # Authenticate session
        self.client.force_login(self.normal_user)
        response = self.client.get(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ==========================================================================
    # 4. Custom IsPremiumUser Permission Tests (Ticket Endpoint)
    # ==========================================================================
    def test_ticket_without_premium_user_fails(self):
        # Authenticate as normal user (non-premium)
        self.client.force_login(self.normal_user)
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_with_premium_user_success(self):
        # Authenticate as premium user
        self.client.force_login(self.premium_user)
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event_name'], "Coldplay VIP")
