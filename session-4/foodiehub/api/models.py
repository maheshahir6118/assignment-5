from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    UserProfile model extending the default Django User model.
    Stores the is_premium boolean flag for custom permissions.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_premium = models.BooleanField(default=False, help_text="Designates if this user has access to premium tickets.")

    def __str__(self):
        return f"{self.user.username} (Premium: {self.is_premium})"

# Signal to automatically create/update UserProfile when a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Playlist(models.Model):
    """
    Playlist model. Protected by Basic Authentication.
    """
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Order model. Protected by Token Authentication.
    """
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order #{self.id} for {self.product_name}"


class CartItem(models.Model):
    """
    CartItem model. Protected by Session Authentication.
    """
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"


class Ticket(models.Model):
    """
    Ticket model. Protected by custom IsPremiumUser permission class.
    """
    event_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_name
