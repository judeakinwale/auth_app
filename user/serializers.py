from rest_framework import serializers
from django.contrib.auth import get_user_model
from user import models, setup
from util import utils as utility

# For JWT and drf-yasg integration
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.validators import UniqueValidator
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
      'employee_id',
      'password',
      'is_active',
      'is_staff',
      'is_employee',
      'is_trial',
      'is_superuser',
    ]
    optional_fields = [
      'is_trial',
      'is_active',
    ]
    read_only_fields = [
      'is_superuser',
      'employee_id',
    ]
    extra_kwargs = {
      'url': {'view_name': 'user:user-detail'},
      'password': {'write_only': True, 'min_length': 5, 'required': False, 'allow_null': True},
      # "email": {
      #   "validators": [
      #     UniqueValidator(queryset=get_user_model().objects.all(),message="This email already exists!")
      #   ]
      # },
      # "username": {
      #   "validators": [
      #     UniqueValidator(queryset=get_user_model().objects.all(),message="This username already exists!")
      #   ]
      # },
      # "employee_id": {
      #   "validators": [
      #     UniqueValidator(queryset=get_user_model().objects.all(),message="This employee_id already exists!")
      #   ]
      # },
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
  
  
class TrialSerializer(serializers.HyperlinkedModelSerializer):
  """serializer for the Trial model"""
  
  class Meta:
    model = models.Trial
    fields = [
      'id',
      'url',
      'user',
      'number',
      'location',
      'industry',
      'is_active',
      'is_completed',
      'timestamp',
    ]
    optional_fields = [
      'number',
      'is_active',
    ]
    extra_kwargs = {
      'url': {'view_name': 'user:trial-detail'},
    }
  

class TrialResponseSerializer(TrialSerializer):
  """response serializer for the Trial model"""
  user = UserSerializer(read_only=True)
  

class TrialUserSerializer(serializers.HyperlinkedModelSerializer):
  """serializer for creating the Trial User"""
  
  first_name = serializers.CharField()
  middle_name = serializers.CharField(allow_null=True, required=False)
  last_name = serializers.CharField()
  email = serializers.CharField()
  
  class Meta:
    model = models.Trial
    fields = [
      'id',
      'url',
      'first_name',
      'middle_name',
      'last_name',
      'lastrial',
      'email',
      'user',
      'number',
      'lastrial',
      'numtrial',
      'location',
      'industry',
      'is_active',
      'numtrial',
      'is_completed',
      'timestamp',
    ]
    optional_fields = [
      'first_name',
      'middle_name',
      'last_name',
      'email',
      'user',
      'number',
      'is_active',
    ]
    extra_kwargs = {
      'url': {'view_name': 'user:trial-user-detail'},
      'user': {'required': False, 'allow_null': True},
    }

  def create(self, validated_data):
    payload = {
      'first_name': validated_data.get('first_name', None),
      'middle_name': validated_data.get('middle_name', None),
      'last_name': validated_data.get('last_name', None),
      'email': validated_data.get('email', None),
    }
    removed_data = []
    for key, value in payload.items():
      item = validated_data.pop(key) if key in validated_data else None
      removed_data.append(item)
    
    if 'user' not in validated_data:
      payload['password'] = utility.code_generator(6)
      payload['is_staff'] = True
      payload['is_trial'] = True
      
      user = get_user_model().objects.create_user(**payload)
      validated_data['user'] = user
      try:
        url = "https://www.hrtechleft.com/login"
        company = {"name": "TechLeft"}
        context = {
          "user": user,
          "company": company,
          "url": url
        }
        setup.send_account_creation_email(self.request, reciepients, context, True)
      except Exception as e:
        print(f"trial user creation email error: {e} \n")
    
    return super().create(validated_data)


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
