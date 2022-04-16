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


class CompanyBaseSerializer(serializers.HyperlinkedModelSerializer):
  
  phone_numbers = PhoneSerializer(many=True)
  
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
      'province',
      'state',
      'country',
      'postal_code',
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


class LocationSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  
  class Meta:
    model = models.Location
    fields = [
      'id',
      'url',
      'company',
      'longitude',
      'latitude',
      # 'point',
      'accuracy',
      'altitude',
      'max_radius',
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
      'url': {'view_name': 'company:location-detail'},
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
      'first_name',
      'middle_name',
      'last_name',
      'email',
      'phone',
      'company',
      'branch',
      'department',
      'employee_id',
      'role',
      'date_of_birth',
      'address',
      'province',
      'state',
      'country',
      'postal_code',
      'image',
      'hobbies',
      'join_date',
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
  phone_numbers = PhoneSerializer(many=True)
  
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
      'province',
      'state',
      'country',
      'postal_code',
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
  
  def create(self, validated_data):
    try:
      phone_numbers = validated_data.pop('phone_numbers')
      branch =  super().create(validated_data)
      for data in phone_numbers:
        data['branch'] = branch
        phone_number = models.Phone.objects.create(**data)

        # # Check if branch phone number in company phone_numbers 
        # if not models.Company.phone_numbers.filter(id=phone_number.id, phone_number=phone_number.phone_number).exists():
        #   # Check if branch phone number to company phone_numbers
        #   models.Company.phone_numbers.add(phone_number)
          
    except Exception:
      branch =  super().create(validated_data)

    return branch

  def update(self, instance, validated_data):
    try:
      phone_numbers = validated_data.pop('phone_numbers')
      branch = super().update(instance, validated_data)
      nested_serializer = self.fields['phone_numbers']        
      
      n = 0
      for nested_data in phone_numbers:            
        try:
          nested_instance = instance.phone_numbers.all()[n]
          phone_number = nested_serializer.update(self, nested_instance, nested_data) # Where nested serializer = PhoneSerializer
        except Exception as e:
          nested_data.update(branch=branch)
          phone_number = models.Phone.objects.create(**nested_data)

        # # Check if branch phone number in company phone_numbers 
        # if not models.Company.phone_numbers.filter(id=phone_number.id, phone_number=phone_number.phone_number).exists():
        #   # Check if branch phone number to company phone_numbers
        #   models.Company.phone_numbers.add(phone_number)
        
        n += 1
    except  Exception as e:
        branch = super().update(instance, validated_data)
    return branch


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all())
  
  class Meta:
    model = models.Department
    fields = [
      'id',
      'url',
      'company',
      'branch',
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


class CompanySerializer(CompanyBaseSerializer):
  
  branches = BranchSerializer(many=True, read_only=True)
  departments = DepartmentSerializer(many=True, read_only=True)
  employees = EmployeeSerializer(many=True, read_only=True)
  
  class Meta(CompanyBaseSerializer.Meta):
    additional_fields = [
      'branches',
      'departments',
      'employees',
    ]
    fields = CompanyBaseSerializer.Meta.fields + additional_fields
    depth = 0

  def create(self, validated_data):
    try:
      phone_numbers = validated_data.pop('phone_numbers')
      company =  super().create(validated_data)
      for data in phone_numbers:
        data['company'] = company
        models.Phone.objects.create(**data)
    except Exception:
      company =  super().create(validated_data)

    return company

  def update(self, instance, validated_data):
    try:
      phone_numbers = validated_data.pop('phone_numbers')
      company = super().update(instance, validated_data)
      nested_serializer = self.fields['phone_numbers']        
      
      n = 0
      for nested_data in phone_numbers:            
        try:
          # print(f'continued, n is {n}')
          nested_instance = instance.phone_numbers.all()[n]
          # print("nested phone_number exists")
          phone_number = nested_serializer.update(self, nested_instance, nested_data) # Where nested serializer = PhoneSerializer
          # print("phone_number created")
        except Exception as e:
          # print(f"There was an exception: {e}")
          nested_data.update(company=company)
          phone_number = models.Phone.objects.create(**nested_data)
          # print("new phone_number created instead")
          
        n += 1
    except  Exception as e:
        company = super().update(instance, validated_data)

    return company


# Response Serializers
class LocationResponseSerializer(LocationSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  
  class Meta(LocationSerializer.Meta):
    depth = 0


class EmployeeResponseSerializer(EmployeeSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  branch = BranchSerializer(read_only=True)
  department = DepartmentSerializer(read_only=True)
  
  class Meta(EmployeeSerializer.Meta):
    depth = 0


class BranchResponseSerializer(BranchSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  
  class Meta(BranchSerializer.Meta):
    depth = 0


class DepartmentResponseSerializer(DepartmentSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  branch = BranchSerializer(read_only=True)
  
  class Meta(DepartmentSerializer.Meta):
    depth = 0
 