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