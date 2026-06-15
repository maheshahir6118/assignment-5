from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """
    Admin registration for the Restaurant model.
    Exposes ID, Name, Cuisine, and Rating in the list view.
    """
    list_display = ('id', 'name', 'cuisine', 'rating')
    search_fields = ('name', 'cuisine')
    list_filter = ('cuisine', 'rating')
