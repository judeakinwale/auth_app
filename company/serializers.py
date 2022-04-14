from rest_framework import serializers
from django.contrib.auth import get_user_model
from company import models


class CompanySerializer(serializers.HyperlinkedModelSerializer):
  """serializer for the User model"""
  
  class Meta:
    model = models.Company
    fields = [
      'id',
      'url',
      'name',
      'email',
      'description',
      'address',
      'local_govt',
      'state',
      'country',
      'zip_code',
      'contact_person',
      'website',
      'logo',
      'created_at',
      'is_active',
    ]
    optional_fields = [
      'is_active',
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:company-detail'},
    }

  def create(self, validated_data):
    pass

  def update(self, instance, validated_data):
    pass
    