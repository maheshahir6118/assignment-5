from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant
from .serializers import RestaurantSerializer

# ==============================================================================
# PAGINATION CONFIGURATIONS
# ==============================================================================

class RestaurantPageNumberPagination(PageNumberPagination):
    """
    PageNumberPagination config:
    - 3 restaurants per page.
    - Query parameter for changing page is '?page='.
    """
    page_size = 3
    page_size_query_param = 'page_size'  # Allows client to override page size
    max_page_size = 100


class RestaurantLimitOffsetPagination(LimitOffsetPagination):
    """
    LimitOffsetPagination config:
    - Default limit is 2 (or 3, we'll set default to 2 to match custom query examples).
    - Query parameters are '?limit=' and '?offset='.
    """
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100


# ==============================================================================
# VIEWSETS IMPLEMENTATION
# ==============================================================================

class RestaurantViewSet(ModelViewSet):
    """
    ModelViewSet exposing CRUD endpoints for Restaurant.
    Uses PAGE NUMBER pagination (3 items per page).
    Supports:
    - Filtering by cuisine (?cuisine=Italian)
    - Ordering by name or cuisine (?ordering=name or ?ordering=-cuisine)
    """
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer
    pagination_class = RestaurantPageNumberPagination

    # Registers backends explicitly for this viewset (DjangoFilterBackend & OrderingFilter)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    # Fields allowed for exact filtering
    filterset_fields = ['cuisine']
    
    # Fields allowed for sorting
    ordering_fields = ['name', 'cuisine']
    
    # Default ordering applied if no parameter is provided
    ordering = ['id']


class RestaurantLimitOffsetViewSet(ModelViewSet):
    """
    ModelViewSet exposing CRUD endpoints for Restaurant.
    Uses LIMIT-OFFSET pagination.
    Supports:
    - Filtering by cuisine (?cuisine=Italian)
    - Ordering by name or cuisine (?ordering=name or ?ordering=-cuisine)
    """
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer
    pagination_class = RestaurantLimitOffsetPagination

    # Registers backends
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['cuisine']
    ordering_fields = ['name', 'cuisine']
    ordering = ['id']
