from rest_framework import serializers
from django.contrib.auth import get_user_model
from company import models


class PhoneSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all())
  
  class Meta:
    model = models.Phone
    fields = [
      'id',
      'url',
      'company',
      'branch',
      'phone_number',
      'is_active',
      'created_at',
      'updated_at',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'created_at',
      'updated_at',
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:phone-detail'},
    }



class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all())
  department = serializers.PrimaryKeyRelatedField(queryset=models.Department.objects.all())
  
  class Meta:
    model = models.Employee
    fields = [
      'id',
      'url',
      "first_name",
      "middle_name",
      "last_name",
      "email",
      "phone",
      "company",
      "branch",
      "department",
      "role",
      "date_of_birth",
      "address",
      "local_govt",
      "state",
      "country",
      "zip_code",
      "image",
      'is_active',
      'created_at',
      'updated_at',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'created_at',
      'updated_at',
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:employee-detail'},
    }


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
      'created_at',
      'updated_at',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'created_at',
      'updated_at',
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
      'created_at',
      'updated_at',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'created_at',
      'updated_at',
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:department-detail'},
    }


class CompanySerializer(serializers.HyperlinkedModelSerializer):
  
  phone_numbers = PhoneSerializer(many=True)
  branches = BranchSerializer(many=True, read_only=True)
  departments = DepartmentSerializer(many=True, read_only=True)
  employees = EmployeeSerializer(many=True, read_only=True)
  
  class Meta:
    model = models.Company
    fields = [
      'id',
      'url',
      'name',
      'email',
      'description',
      'phone_numbers',
      'branches',
      'departments',
      'employees',
      'address',
      'local_govt',
      'state',
      'country',
      'zip_code',
      'contact_person',
      'website',
      'logo',
      'is_active',
      'created_at',
      'updated_at',
    ]
    optional_fields = [
      'is_active',
    ]
    read_only_fields = [
      'created_at',
      'updated_at',
    ]
    extra_kwargs = {
      'url': {'view_name': 'company:company-detail'},
    }
    depth = 0

  # def create(self, validated_data):
  #   pass

  # def update(self, instance, validated_data):
  #   pass
  

class BranchResponseSerializer(BranchSerializer):
  
  company = CompanySerializer(read_only=True)
  
  class Meta(BranchSerializer.Meta):
    depth = 0
    