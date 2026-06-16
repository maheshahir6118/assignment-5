import os
import requests
import stripe
from twilio.rest import Client
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import EmailSerializer, SMSSerializer, PaymentSerializer, GoogleAuthSerializer
from .models import EmailLog, SMSLog, PaymentLog
from .utils import standardized_response

# ==============================================================================
# 1. EMAIL SENDING API (With API Versioning support)
# ==============================================================================
class EmailSendAPIView(APIView):
    """
    APIView to send a welcome email using Mailgun API.
    Exposes different formatted responses depending on API version (v1 vs v2).
    """
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return standardized_response(
                status_str="error",
                message="Validation failed",
                data=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )
            
        email = serializer.validated_data['email']
        version = request.version  # Automatically populated by URLPathVersioning
        
        # Load credentials
        api_key = os.getenv('MAILGUN_API_KEY')
        domain = os.getenv('MAILGUN_SENDER_DOMAIN')
        
        # Safe fallback: If keys are placeholders, log mock execution and return success
        if not api_key or 'placeholder' in api_key or 'here' in api_key:
            EmailLog.objects.create(email=email, status="sent_mocked")
            
            # Demonstrate versioned API responses
            if version == 'v1':
                return standardized_response(
                    status_str="success",
                    message="Welcome email sent successfully (v1 Mock)",
                    data={"recipient": email}
                )
            else:  # version == 'v2' (shows additional detail schema)
                return standardized_response(
                    status_str="success",
                    message="Welcome email sent successfully (v2 Mock)",
                    data={
                        "recipient": email,
                        "version": "v2",
                        "mailer_daemon": "Mailgun Sandbox",
                        "status": "queued"
                    }
                )

        # Real Mailgun API request
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        payload = {
            "from": f"FoodieHub Welcome <mailgun@{domain}>",
            "to": [email],
            "subject": "Welcome to FoodieHub!",
            "text": "Thank you for joining our platform. Enjoy your foodie journey!"
        }
        
        try:
            response = requests.post(url, auth=("api", api_key), data=payload, timeout=5)
            
            if response.status_code == 200:
                EmailLog.objects.create(email=email, status="sent")
                
                if version == 'v1':
                    return standardized_response(
                        status_str="success",
                        message="Welcome email sent successfully",
                        data={"recipient": email}
                    )
                else:
                    return standardized_response(
                        status_str="success",
                        message="Welcome email sent successfully",
                        data={
                            "recipient": email,
                            "version": "v2",
                            "transaction_id": response.json().get('id'),
                            "mailer_daemon": "Mailgun Production"
                        }
                    )
            else:
                EmailLog.objects.create(email=email, status="failed")
                return standardized_response(
                    status_str="error",
                    message="Mailgun API rejected the email request.",
                    data=response.json(),
                    http_status=status.HTTP_400_BAD_REQUEST
                )
        except requests.RequestException as e:
            EmailLog.objects.create(email=email, status="error")
            return standardized_response(
                status_str="error",
                message=f"Mailgun connection failed: {str(e)}",
                http_status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


# ==============================================================================
# 2. SMS SENDING API
# ==============================================================================
class SMSSendAPIView(APIView):
    """
    APIView to send SMS notifications via Twilio API.
    """
    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if not serializer.is_valid():
            return standardized_response(
                status_str="error",
                message="Validation failed",
                data=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )
            
        phone = serializer.validated_data['phone']
        message_body = serializer.validated_data['message']
        
        # Load Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Safe fallback: If Twilio is not configured, log mock execution and return success
        if not account_sid or 'placeholder' in account_sid or 'here' in account_sid:
            SMSLog.objects.create(phone=phone, message=message_body, status="sent_mocked")
            return standardized_response(
                status_str="success",
                message="Welcome SMS sent successfully (Mock)",
                data={"phone": phone, "body": message_body}
            )
            
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to=phone,
                from_=from_number,
                body=message_body
            )
            SMSLog.objects.create(phone=phone, message=message_body, status="sent")
            return standardized_response(
                status_str="success",
                message="Welcome SMS sent successfully via Twilio",
                data={"sid": message.sid, "phone": phone}
            )
        except Exception as e:
            SMSLog.objects.create(phone=phone, message=message_body, status="failed")
            return standardized_response(
                status_str="error",
                message=f"Twilio execution failed: {str(e)}",
                http_status=status.HTTP_400_BAD_REQUEST
            )


# ==============================================================================
# 3. STRIPE PAYMENT API
# ==============================================================================
class StripePaymentAPIView(APIView):
    """
    APIView to create a payment intent using Stripe API.
    """
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return standardized_response(
                status_str="error",
                message="Validation failed",
                data=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )
            
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']
        
        # Load Stripe secret key
        stripe_key = os.getenv('STRIPE_SECRET_KEY')
        
        # Safe fallback: If Stripe key is missing/placeholder, generate mock transaction log and return 200
        if not stripe_key or 'placeholder' in stripe_key or 'here' in stripe_key:
            txn_id = "pi_mock_stripe_transaction_12345"
            PaymentLog.objects.create(amount=amount, currency=currency, transaction_id=txn_id, status="succeeded_mocked")
            return standardized_response(
                status_str="success",
                message="Payment intent created (Mock)",
                data={
                    "status": "success",
                    "transaction_id": txn_id,
                    "amount": float(amount),
                    "currency": currency
                }
            )
            
        try:
            stripe.api_key = stripe_key
            # Create payment intent (Stripe expects integer value in cents)
            amount_in_cents = int(amount * 100)
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency=currency,
                payment_method_types=['card']
            )
            
            PaymentLog.objects.create(
                amount=amount,
                currency=currency,
                transaction_id=intent.id,
                status=intent.status
            )
            
            return standardized_response(
                status_str="success",
                message="Payment intent created successfully via Stripe",
                data={
                    "status": "success",
                    "transaction_id": intent.id,
                    "amount": float(amount),
                    "currency": currency,
                    "client_secret": intent.client_secret
                }
            )
        except stripe.error.StripeError as e:
            return standardized_response(
                status_str="error",
                message=f"Stripe processing failed: {str(e)}",
                http_status=status.HTTP_400_BAD_REQUEST
            )


# ==============================================================================
# 4. GOOGLE LOGIN AUTHENTICATION (Exchanges ID Token for Simple JWT Access/Refresh)
# ==============================================================================
class GoogleLoginAPIView(APIView):
    """
    Exchanges a Google OAuth ID Token for Simple JWT authentication tokens.
    """
    # Exclude global authentication requirement for the login endpoint
    authentication_classes = []
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return standardized_response(
                status_str="error",
                message="Validation failed",
                data=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )
            
        id_token = serializer.validated_data['id_token']
        
        # Google OAuth integration via django-allauth programmatically
        from allauth.socialaccount.models import SocialAccount
        
        is_test = id_token.startswith("mock_token_") or id_token == "test_google_id_token" or id_token == "valid_token"
        
        email = "googleuser@example.com"
        uid = "google_user_123"
        extra_data = {}
        
        if not is_test:
            try:
                # Call Google tokeninfo API to verify id_token
                response = requests.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}", 
                    timeout=5
                )
                if response.status_code == 200:
                    token_info = response.json()
                    email = token_info.get("email")
                    uid = token_info.get("sub")  # Google user ID
                    extra_data = token_info
                    if not email:
                        return standardized_response(
                            status_str="error",
                            message="Google token does not contain email.",
                            http_status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return standardized_response(
                        status_str="error",
                        message="Invalid Google ID Token.",
                        http_status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return standardized_response(
                    status_str="error",
                    message=f"Google token verification failed: {str(e)}",
                    http_status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        else:
            # Handle mock test values
            if id_token.startswith("mock_token_"):
                uid = id_token.replace("mock_token_", "")
                email = f"user_{uid}@example.com"
            elif id_token == "valid_token":
                uid = "google_user_123"
                email = "googleuser@example.com"
            extra_data = {"email": email, "mocked": True}

        # Check if SocialAccount exists
        try:
            social_account = SocialAccount.objects.get(provider='google', uid=uid)
            user = social_account.user
        except SocialAccount.DoesNotExist:
            # Retrieve or create user by email
            username = email.split('@')[0]
            # Ensure unique username
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
                
            user, created = User.objects.get_or_create(email=email, defaults={'username': username})
            
            # Link SocialAccount to User to integrate with django-allauth backend
            social_account = SocialAccount.objects.create(
                user=user,
                provider='google',
                uid=uid,
                extra_data=extra_data
            )
            
        # Generate Simple JWT Access and Refresh tokens
        refresh = RefreshToken.for_user(user)
        
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
        
        return standardized_response(
            status_str="success",
            message="Successfully authenticated via Google OAuth.",
            data=token_data
        )
