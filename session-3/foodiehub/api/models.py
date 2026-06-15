from django.db import models

class Restaurant(models.Model):
    """
    Model representing a Restaurant with name, cuisine, and location.
    """
    name = models.CharField(max_length=255, help_text="Name of the restaurant.")
    cuisine = models.CharField(max_length=255, help_text="Cuisine type served (e.g. Italian, Indian).")
    location = models.CharField(max_length=255, help_text="Location/City of the restaurant.")

    def __str__(self):
        return self.name
