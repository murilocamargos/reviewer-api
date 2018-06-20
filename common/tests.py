from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class CommonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='john')

    def test_user_register_creates_token(self):
        """
        Tests if a user creation fires the signal to creating their token too.
        """
        user = User.objects.create(username='murilo')
        token = Token.objects.filter(user=user)

        self.assertEqual(token.count(), 1)
        self.assertEqual(token.first().user, user)

    def test_api_auth_with_query_string(self):
        """
        Tests api authentication using the query parameter `token`.
        """
        token = Token.objects.filter(user=self.user).first()

        url = reverse('subscribers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse('subscribers-list') + '?token=' + token.key
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_auth_with_bearer_token(self):
        """
        Tests api authentication using token sent as http auth.
        """
        token = Token.objects.filter(user=self.user).first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('subscribers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
