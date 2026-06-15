from django.db import models

class Restaurant(models.Model):
    """
    Model representing a Zomato-style Restaurant.
    """
    name = models.CharField(max_length=255, help_text="The name of the restaurant.")
    cuisine = models.CharField(max_length=255, help_text="The type of cuisine served (e.g., Italian, Chinese).")

    def __str__(self):
        return self.name
