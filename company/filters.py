from django_filters import rest_framework as filters
from company import models


# TODO: Update filter fields for all models
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
            'user__first_name': ['icontains'],
            'user__email': ['icontains'],
            'is_active': ['exact'],
        }


class LocationFilter(filters.FilterSet):

    class Meta:
        model = models.Location
        fields = {
            'branch__name': ['icontains'],
        }
        
        
class ClientFilter(filters.FilterSet):

    class Meta:
        model = models.Client
        fields = {
            'name': ['icontains'],
        }


class EventFilter(filters.FilterSet):

    class Meta:
        model = models.Event
        fields = {
            'name': ['icontains'],
        }