from django.urls import path
from . import views

urlpatterns = [
    # 1. Versioned welcome email API endpoints (URLPathVersioning)
    # URL equivalent: /api/v1/send-email/ and /api/v2/send-email/
    path('<str:version>/send-email/', views.EmailSendAPIView.as_view(), name='send_email_versioned'),
    
    # 2. SMS welcome dispatch endpoint
    # URL: /api/send-sms/
    path('send-sms/', views.SMSSendAPIView.as_view(), name='send_sms'),
    
    # 3. Stripe payment intent gateway endpoint
    # URL: /api/pay/
    path('pay/', views.StripePaymentAPIView.as_view(), name='stripe_pay'),
    
    # 4. Google OAuth exchange login endpoint (returns simplejwt access/refresh keys)
    # URL: /api/auth/google/
    path('auth/google/', views.GoogleLoginAPIView.as_view(), name='google_auth'),
]
