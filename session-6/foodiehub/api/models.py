from django.db import models
from django.contrib.auth.models import User

class EmailLog(models.Model):
    """
    Log of sent emails via Mailgun.
    """
    email = models.EmailField()
    status = models.CharField(max_length=50, default="pending")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.email} ({self.status})"


class SMSLog(models.Model):
    """
    Log of sent SMS via Twilio.
    """
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=50, default="pending")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS to {self.phone} ({self.status})"


class PaymentLog(models.Model):
    """
    Log of Stripe Payment Transactions.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} {self.currency} (ID: {self.transaction_id})"
