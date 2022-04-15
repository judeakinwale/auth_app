from django_filters import rest_framework as filters
from company import models


class CompanyFilter(filters.FilterSet):

    class Meta:
        model = models.Company
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
        }


class BranchFilter(filters.FilterSet):

    class Meta:
        model = models.Branch
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
        }


class DepartmentFilter(filters.FilterSet):

    class Meta:
        model = models.Department
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
        }


class EmployeeFilter(filters.FilterSet):

    class Meta:
        model = models.Employee
        fields = {
            'first_name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
        }
