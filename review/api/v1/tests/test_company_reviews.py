from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from review.models import Company, Review


class CompanyReviewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='john')
        self.client.force_authenticate(user=self.user)

        self.company = Company.objects.create(name='Olidata')
        self.company2 = Company.objects.create(name='Data')

        self.review1 = Review.objects.create(title='Title', rating=1,
            summary='Summary', ip_address='127.0.0.1', company=self.company,
            reviewer=self.user)
        self.review2 = Review.objects.create(title='Title', rating=1,
            summary='Summary', ip_address='127.0.0.1', company=self.company,
            reviewer=self.user)
        self.review3 = Review.objects.create(title='Title', rating=1,
            summary='Summary', ip_address='127.0.0.1', company=self.company2,
            reviewer=self.user)
    
    def test_review_list(self):
        """
        Check if review list endpoint is retrieving the user's reviews.
        """
        url = reverse('company-review-list', args=[self.company.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data['count'], 2)

    def test_review_add(self):
        """
        Check if review list endpoint can add a review.
        """
        url = reverse('company-review-list', args=[self.company2.id])

        data = {
            'title': 'Title2',
            'rating': 1,
            'summary': 'Summary',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data.get('reviewer'), self.user.id)
        self.assertEqual(response_data.get('company'), self.company2.id)

    def test_review_add_with_errors(self):
        """
        Check if review list endpoint will raise exceptions when adding
        problematic reviews.
        """
        url = reverse('company-review-list', args=[self.company2.id])

        data = {
            'title': 'Title2',
            'rating': 1,
            'summary': 'Summary',
        }

        # All fields are required, test removing one by one
        keys = list(data.keys())
        for key in keys:
            new_data = dict(data)
            new_data.pop(key)
            response = self.client.post(url, new_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_detail(self):
        """
        Check if review can be fetched by its unique id.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review1.id])

        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], self.review1.title)

    def test_review_detail_non_existing_id(self):
        """
        Check if non existing review id raises not found error.
        """
        url = reverse('company-review-detail', args=[self.company.id, 10])

        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_detail_other_company(self):
        """
        Check if other company's review will raise not found error.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review3.id])

        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_updating(self):
        """
        Try to edit the entire review object.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review1.id])

        data = {
            'title': 'Title3',
            'rating': 1,
            'summary': 'Summary',
            'company': self.company.id,
        }
        response = self.client.put(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], 'Title3')

    def test_review_updating_patches(self):
        """
        Try to edit the a piece of review object.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review1.id])

        data = {
            'title': 'Title2',
        }
        response = self.client.patch(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], 'Title2')
        self.assertNotEqual(response_data['title'], self.review1.title)

    def test_review_updating_with_error(self):
        """
        Check if a review's can be edited with a score outside 1-5.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review1.id])

        data = {
            'rating': 0,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'rating': 6,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_review_other_company(self):
        """
        Check if a other company's review can be edited.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review3.id])

        data = {
            'rating': 2,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_delete(self):
        """
        Tests if a review will be deleted.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review1.id])

        response = self.client.delete(url)
        review = Review.objects.filter(id=self.review1.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(review.count(), 0)
    
    def test_review_delete_other_company(self):
        """
        Tests if other company's review will be deleted.
        """
        url = reverse('company-review-detail', args=[self.company.id, self.review3.id])

        response = self.client.delete(url)
        review = Review.objects.filter(id=self.review2.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)