from rest_framework import serializers
from django.contrib.auth import get_user_model
from company import models


class CompanySerializer(serializers.HyperlinkedModelSerializer):
  
  class Meta:
    model = models.Company
    fields = [
      'id',
      'url',
      'name',
      'email',
      'description',
      'phone_numbers',
      'address',
      'local_govt',
      'state',
      'country',
      'zip_code',
      'contact_person',
      'website',
      'logo',
      'is_active',
      'timestamp',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'timestamp'
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:company-detail'},
    }

  # def create(self, validated_data):
  #   pass

  # def update(self, instance, validated_data):
  #   pass
  

class BranchSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  
  class Meta:
    model = models.Branch
    fields = [
      'id',
      'url',
      'company',
      'name',
      'email',
      'description',
      'phone_numbers',
      'address',
      'local_govt',
      'state',
      'country',
      'zip_code',
      'contact_person',
      'is_active',
      'timestamp',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'timestamp'
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:branch-detail'},
    }
    
    
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  
  class Meta:
    model = models.Department
    fields = [
      'id',
      'url',
      'company',
      'name',
      'email',
      'description',
      'is_active',
      'timestamp',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'timestamp'
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:department-detail'},
    }
    