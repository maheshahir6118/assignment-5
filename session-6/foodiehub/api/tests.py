from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class APIEndpointsTestCase(APITestCase):
    """
    Test cases for Session 6: Advanced Features and Deployment.
    Ensures correct functionality of versioned emails, SMS, Stripe Payments, 
    Google OAuth JWT generation, and standardized error formatting.
    """

    def test_email_sending_v1(self):
        url = reverse('send_email_versioned', kwargs={'version': 'v1'})
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('Welcome email sent successfully', response.data['message'])
        self.assertEqual(response.data['data']['recipient'], 'testuser@example.com')

    def test_email_sending_v2(self):
        url = reverse('send_email_versioned', kwargs={'version': 'v2'})
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('Welcome email sent successfully', response.data['message'])
        self.assertEqual(response.data['data']['recipient'], 'testuser@example.com')
        self.assertEqual(response.data['data']['version'], 'v2')
        self.assertEqual(response.data['data']['status'], 'queued')

    def test_email_sending_validation_error(self):
        url = reverse('send_email_versioned', kwargs={'version': 'v1'})
        data = {'email': 'not-an-email'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Validation failed')
        self.assertIn('email', response.data['data'])

    def test_sms_sending_success(self):
        url = reverse('send_sms')
        data = {
            'phone': '+911234567890',
            'message': 'Welcome to our platform'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('Welcome SMS sent successfully', response.data['message'])
        self.assertEqual(response.data['data']['phone'], '+911234567890')

    def test_sms_sending_validation_error(self):
        url = reverse('send_sms')
        data = {
            'phone': '',
            'message': 'Welcome'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Validation failed')
        self.assertIn('phone', response.data['data'])

    def test_stripe_payment_success(self):
        url = reverse('stripe_pay')
        data = {
            'amount': 100.00,
            'currency': 'usd'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('transaction_id', response.data['data'])
        self.assertEqual(float(response.data['data']['amount']), 100.00)

    def test_stripe_payment_invalid_amount(self):
        url = reverse('stripe_pay')
        data = {
            'amount': 0.10,  # Below min_value 0.50 Decimal
            'currency': 'usd'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Validation failed')
        self.assertIn('amount', response.data['data'])

    def test_google_login_success(self):
        url = reverse('google_auth')
        data = {
            'id_token': 'mock_token_google_user_unique_123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], 'user_google_user_unique_123@example.com')
        
        # Verify SocialAccount was created and linked correctly via django-allauth
        social_exists = SocialAccount.objects.filter(provider='google', uid='google_user_unique_123').exists()
        self.assertTrue(social_exists)
