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
