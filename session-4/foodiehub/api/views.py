from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Playlist, Order, CartItem, Ticket
from .serializers import PlaylistSerializer, OrderSerializer, CartItemSerializer, TicketSerializer
from .permissions import IsPremiumUser

# ==============================================================================
# VIEWSETS PROTECTED BY DIFFERENT AUTHENTICATION SCHEMES
# ==============================================================================

class PlaylistViewSet(ModelViewSet):
    """
    Playlist endpoint.
    Protected by: Basic Authentication (username/password in Headers).
    Permission: IsAuthenticated (Only logged-in users).
    """
    serializer_class = PlaylistSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Premium design: only returns playlists belonging to the active user
        return Playlist.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically bind owner to the logged-in user
        serializer.save(owner=self.request.user)


class OrderViewSet(ModelViewSet):
    """
    Order endpoint.
    Protected by: Token Authentication (Bearer/Token in Authorization Header).
    Permission: IsAuthenticated.
    """
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returns only orders made by the active authenticated user
        return Order.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class CartItemViewSet(ModelViewSet):
    """
    CartItem endpoint.
    Protected by: Session Authentication (Cookie/CSRF session state).
    Permission: IsAuthenticated.
    """
    serializer_class = CartItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returns only cart items belonging to the active session user
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(ModelViewSet):
    """
    Ticket endpoint.
    Protected by: Custom IsPremiumUser permission.
    Allowed auth schemes: Session, Token, or Basic (allows flexible premium access).
    """
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    
    # Custom premium permission enforcement
    permission_classes = [IsPremiumUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
