from django.db import models

class Restaurant(models.Model):
    """
    Restaurant model representing a Zomato-style restaurant.
    """
    name = models.CharField(max_length=255, help_text="Name of the restaurant.")
    cuisine = models.CharField(max_length=255, help_text="Cuisine type served.")
    rating = models.FloatField(help_text="Rating from 0.0 to 5.0.")

    def __str__(self):
        return self.name
