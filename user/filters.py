from django_filters import rest_framework as filters
from user import models


class UserFilter(filters.FilterSet):

    class Meta:
        model = models.User
        fields = {
            'first_name': ['icontains'],
            'middle_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
            'is_superuser': ['exact'],
        }
