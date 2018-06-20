from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from review.models import Company


class CompaniesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='john')
        self.client.force_authenticate(user=self.user)

        self.company = Company.objects.create(name='Olidata')

    def test_company_list(self):
        """
        Check if company list endpoint is retrieving all company.
        """
        company = Company.objects.create(name='Olidata')

        url = reverse('company-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data['count'], 2)
        self.assertIn({'id': company.id, 'name': 'Olidata'},
                      response_data['results'])

    def test_company_add(self):
        """
        A company can't be added via API, only from admin.
        """
        url = reverse('company-list')

        data = {'name': 'Olidata'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_company_detail(self):
        """
        Check if company can be fetched by its unique id.
        """
        url = reverse('company-detail', args=[self.company.id])

        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_data['name'], self.company.name)

    def test_company_detail_non_existing_id(self):
        """
        Check if non existing company id raises not found error.
        """
        url = reverse('company-detail', args=[10])

        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_company_updating(self):
        """
        A company can't be updated via API, only from admin.
        """
        company = Company.objects.create(name='Olidata')
        url = reverse('company-detail', args=[company.id])

        response = self.client.patch(url, {}, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_company_delete(self):
        """
        A company can't be deleted via API, only from admin.
        """
        url = reverse('company-detail', args=[self.company.id])

        response = self.client.delete(url)
        company = Company.objects.filter(id=self.company.id)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Company.objects.count(), 1)
