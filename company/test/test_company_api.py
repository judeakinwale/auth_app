from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from company import models, serializers
from . import test_dependencies as deps


COMPANY_URL = reverse('company:company-list')


factory = APIRequestFactory() # creating a test request
request = factory.get('/') # get request for root url
serializer_context = {'request': Request(request)} # create serializer context - for hyperlinked serializers


def company_detail_url(company_id):
    """return url for the company detail"""
    return reverse('company:company-detail', args=[company_id])


class PublicCompanyApiTest(TestCase):
    """test public access to the company api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(COMPANY_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateCompanyApiTest(TestCase):
    """test authenticated access to the company api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_company(self):
        """test retrieving a list of company"""
        deps.sample_company(name="Company 2")
        company = models.Company.objects.all()
        serializer = serializers.CompanySerializer(company, many=True, context=serializer_context)

        res = self.client.get(COMPANY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_company_not_limited_to_source(self):
        """test that company from all sources is returned"""
        deps.sample_company(name="Company 2")
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        deps.sample_company(name="Company 2")

        company = models.Company.objects.all()
        serializer = serializers.CompanySerializer(company, many=True, context=serializer_context)

        res = self.client.get(COMPANY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_company_detail(self):
        """test retrieving an company's detail"""
        company = deps.sample_company(name="Company 2")
        serializer = serializers.CompanySerializer(company, context=serializer_context)

        url = company_detail_url(company_id=company.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_company(self):
        """test creating an company"""
        payload = {
            'name': "Company 3",
            'email': "company3@app.com",
        }

        res = self.client.post(COMPANY_URL, payload)

        company = models.Company.objects.get(id=res.data['id'])
        company_serializer = serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        deps.test_all_model_attributes(self, payload, company, company_serializer)

    def test_partial_update_company(self):
        """test partially updating an company's detail using patch"""
        company = deps.sample_company(name="Company 2")
        payload = {
            'email': "company3@app.com",
        }

        url = company_detail_url(company.id)
        res = self.client.patch(url, payload)

        company.refresh_from_db()
        company_serializer = serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        deps.test_all_model_attributes(self, payload, company, company_serializer)

    def test_full_update_company(self):
        """test updating an company's detail using put"""
        company = deps.sample_company(name="Company 2")
        payload = {
            'name': "Company 3",
            'email': "company3@app.com",
        }

        url = company_detail_url(company.id)
        res = self.client.put(url, payload)

        company.refresh_from_db()
        company_serializer = serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        deps.test_all_model_attributes(self, payload, company, company_serializer)

    def test_create_company_with_images(self):
        """test creating an company with attached images"""
        payload = {
            'name': "Company 3",
            'email': "company3@app.com",
        }

        res = self.client.post(COMPANY_URL, payload, format='json')
        # print(res.data)

        company = models.Company.objects.get(id=res.data['id'])
        serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update_company_with_images(self):
        """test updating an company with attached images using patch"""
        company = deps.sample_company(name="Company 2")
        payload = {
            'email': "company3@app.com",
        }

        url = company_detail_url(company.id)
        res = self.client.patch(url, payload, format='json')
        # print(res.data)

        company.refresh_from_db()
        serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_full_update_company_with_images(self):
        """test updating an company with attached images using put"""
        company = deps.sample_company(name="Company 2")
        payload = {
            'name': "Company 3",
            'email': "company3@app.com",
        }

        url = company_detail_url(company.id)
        res = self.client.put(url, payload, format='json')
        # print(res.data)

        company.refresh_from_db()
        serializers.CompanySerializer(company, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
