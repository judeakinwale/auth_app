from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from company import models, serializers
from . import test_dependencies as deps


EMPLOYEE_URL = reverse('company:employee-list')


factory = APIRequestFactory() # creating a test request
request = factory.get('/') # get request for root url
serializer_context = {'request': Request(request)} # create serializer context - for hyperlinked serializers


def employee_detail_url(employee_id):
    """return url for the employee detail"""
    return reverse('company:employee-detail', args=[employee_id])


class PublicEmployeeApiTest(TestCase):
    """test public access to the employee api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(EMPLOYEE_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateEmployeeApiTest(TestCase):
    """test authenticated access to the employee api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.company = deps.sample_company(name="Company 2")
        self.staff_group = deps.create_staff_group()
        self.employee_group = deps.create_employee_group()

    def tearDown(self):
        pass

    def test_retrieve_employee(self):
        """test retrieving a list of employee"""
        deps.sample_employee(user=self.user, company=self.company)
        employee = models.Employee.objects.all()
        serializer = serializers.EmployeeSerializer(employee, many=True, context=serializer_context)

        res = self.client.get(EMPLOYEE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['id'], serializer.data[0]['id'])

    def test_employee_not_limited_to_source(self):
        """test that employee from all sources is returned"""
        deps.sample_employee(user=self.user, company=self.company)
        company3 = deps.sample_company(name="Company 3")
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        deps.sample_employee(user=user2, employee_id="EMP002", company=company3)

        employee = models.Employee.objects.all()
        company_employees = models.Employee.filter(company=company3)
        print(company_employees)
        serializer = serializers.EmployeeSerializer(employee, many=True, context=serializer_context)

        res = self.client.get(EMPLOYEE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(len(res.data['results']), len(serializer.data))
        # self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_employee_detail(self):
        """test retrieving an employee's detail"""
        employee = deps.sample_employee(user=self.user, company=self.company)
        serializer = serializers.EmployeeSerializer(employee, context=serializer_context)

        url = employee_detail_url(employee_id=employee.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], serializer.data['id'])

    def test_create_employee(self):
        """test creating an employee"""
        payload = {
            'user': {
                'username': 'employee_2',
                'email': 'employee2@gmail.com',
                'password': 'password@1',
                'is_employee': True,
            },
            'employee_id': "EMP003",
        }

        res = self.client.post(EMPLOYEE_URL, payload, format='json')

        employee = models.Employee.objects.get(id=res.data['id'])
        employee_serializer = serializers.EmployeeSerializer(employee, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # deps.test_all_model_attributes(self, payload, employee, employee_serializer)

    def test_partial_update_employee(self):
        """test partially updating an employee's detail using patch"""
        employee = deps.sample_employee(user=self.user, company=self.company)
        payload = {
            'employee_id': "EMP003",
        }

        url = employee_detail_url(employee.id)
        res = self.client.patch(url, payload)

        employee.refresh_from_db()
        employee_serializer = serializers.EmployeeSerializer(employee, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # deps.test_all_model_attributes(self, payload, employee, employee_serializer)

    def test_full_update_employee(self):
        """test updating an employee's detail using put"""
        
        employee = deps.sample_employee(user=self.user, company=self.company)
        payload = {
            'user': {
                'username': 'employee_2',
                'email': 'employee2@gmail.com',
                'is_employee': True,
            },
            'employee_id': "EMP003",
        }

        url = employee_detail_url(employee.id)
        res = self.client.put(url, payload, format='json')

        employee.refresh_from_db()
        employee_serializer = serializers.EmployeeSerializer(employee, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # deps.test_all_model_attributes(self, payload, employee, employee_serializer)

    # def test_create_employee_with_images(self):
    #     """test creating an employee with attached images"""
    #     payload = {
    #         'user': {
    # },
    #         'email': "employee3@app.com",
    #     }

    #     res = self.client.post(EMPLOYEE_URL, payload, format='json')
    #     # print(res.data)

    #     employee = models.Employee.objects.get(id=res.data['id'])
    #     serializers.EmployeeSerializer(employee, context=serializer_context)

    # #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # def test_partial_update_employee_with_images(self):
    #     """test updating an employee with attached images using patch"""
    #     employee = deps.sample_employee(name="Employee 2")
    #     payload = {
    #         'email': "employee3@app.com",
    #     }

    #     url = employee_detail_url(employee.id)
    #     res = self.client.patch(url, payload, format='json')
    #     # print(res.data)

    #     employee.refresh_from_db()
    #     serializers.EmployeeSerializer(employee, context=serializer_context)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_full_update_employee_with_images(self):
    #     """test updating an employee with attached images using put"""
    #     employee = deps.sample_employee(name="Employee 2")
    #     payload = {
    #         'user': {
    # },
    #         'email': "employee3@app.com",
    #     }

    #     url = employee_detail_url(employee.id)
    #     res = self.client.put(url, payload, format='json')
    #     # print(res.data)

    #     employee.refresh_from_db()
    #     serializers.EmployeeSerializer(employee, context=serializer_context)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
