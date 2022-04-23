from rest_framework import serializers
from django.contrib.auth import get_user_model
from user import models

# For JWT and drf-yasg integration
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
  TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
  """serializer for the User model"""
  
  class Meta:
    model = get_user_model()
    fields = [
      'id',
      'url',
      'first_name',
      'middle_name',
      'last_name',
      'full_name',
      'email',
      'username',
      'password',
      'is_active',
      'is_staff',
      'is_employee',
      'is_superuser',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'is_superuser',
    ]
    extra_kwargs = {
      'url': {'view_name': 'user:user-detail'},
      'password': {'write_only': True, 'min_length': 5, 'required': False, 'allow_null': True},
    }

  def create(self, validated_data):
          
    user = get_user_model().objects.create_user(**validated_data)
    return user

  def update(self, instance, validated_data):
    """update a user, correctly setting the password and return it"""

    password = validated_data.pop('password') if 'password' in validated_data else False
    user = super().update(instance, validated_data)
    
    if password:
      user.set_password(password)
      user.save()
            
    return user


# Simple JWT integration with drf-yasg (serializers)
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
