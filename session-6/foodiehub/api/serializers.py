from rest_framework import serializers
from .models import EmailLog, SMSLog, PaymentLog

class EmailSerializer(serializers.Serializer):
    """
    Validates email sending requests.
    """
    email = serializers.EmailField()


class SMSSerializer(serializers.Serializer):
    """
    Validates SMS sending requests.
    """
    phone = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=160)


from decimal import Decimal

class PaymentSerializer(serializers.Serializer):
    """
    Validates payment intent creation requests.
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.50'))
    currency = serializers.CharField(max_length=10, default="usd")


class GoogleAuthSerializer(serializers.Serializer):
    """
    Validates incoming Google ID token exchanges.
    """
    id_token = serializers.CharField(help_text="Google ID token retrieved from Google Sign-In SDK.")


# Model serializing schemas
class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'


class SMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLog
        fields = '__all__'


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = '__all__'
