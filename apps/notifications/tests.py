from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='20201111', 
            password='testpassword123',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_register_device_token(self):
        url = reverse('mobile:notifications:register_token')
        data = {
            'token': 'fcm_token_12345',
            'platform': 'android'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], 'fcm_token_12345')

    def test_unregister_device_token(self):
        # Register first
        register_url = reverse('mobile:notifications:register_token')
        self.client.post(register_url, {'token': 'fcm_token_67890', 'platform': 'ios'}, format='json')

        # Unregister
        unregister_url = reverse('mobile:notifications:unregister_token')
        response = self.client.post(unregister_url, {'token': 'fcm_token_67890'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Unregister again
        response2 = self.client.post(unregister_url, {'token': 'fcm_token_67890'}, format='json')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
