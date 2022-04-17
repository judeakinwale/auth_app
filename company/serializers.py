from rest_framework import serializers
from django.contrib.auth import get_user_model
from company import models
from user.serializers import UserSerializer


class PhoneSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all(), allow_null=True, required=False)
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all(), allow_null=True, required=False)
  
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


class EmployeeHelperSerializer(serializers.Serializer):
  
  id = serializers.CharField()


class CompanyBaseSerializer(serializers.HyperlinkedModelSerializer):
  
  phone_numbers = PhoneSerializer(many=True, allow_null=True, required=False)
  
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


class ClientSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all(), allow_null=True, required=False)
  # branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all(), allow_null=True, required=False)
  employees = EmployeeHelperSerializer(many=True, allow_null=True, required=False)
  # employee = serializers.PrimaryKeyRelatedField(queryset=models.Employee.objects.all())
  
  class Meta:
    model = models.Client
    fields = [
      'id',
      'url',
      'company',
      # 'branch',
      'employees',
      'name',
      'email',
      'phone',
      'address',
      'province',
      'state',
      'country',
      'postal_code',
      'image',
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
      'url': {'view_name': 'company:client-detail'},
    }
    depth = 1
    
  def create(self, validated_data):
    try:
      employees = validated_data.pop('employees')
      client =  super().create(validated_data)
      for data in employees:
        # TODO: Get and Update data in employees
        employee = models.Employee.objects.get(id=data['id'])
        client.employees.add(employee)
          
    except Exception:
      client =  super().create(validated_data)

    return client

  def update(self, instance, validated_data):
    try:
      employees = validated_data.pop('employees')
      client = super().update(instance, validated_data)
      client_employees = instance.employees.all()
      client_employee_list = []
      combined_employee_list = []
      
      for client_employee in client_employees:
        combined_employee_list += int(client_employee.id)
        client_employee_list += int(client_employee.id)
        
      for employee in employees:
        combined_employee_list += int(employee['id'])
        
      # TODO: Retain only unique items in 'combined_employee_list'
      # combined_employee_list = 
      
      for data in employees:
        
        # TODO: Get and Update data in employeest
        if int(data['id']) in client_employee_list:
          pass
        if int(data['id']) not in client_employee_list:
          employee = models.Employee.objects.get(id=data['id'])
          client.employees.add(employee)
        
        
    except  Exception as e:
        client = super().update(instance, validated_data)

    return client


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
  
  user = UserSerializer()
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all(), allow_null=True, required=False)
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all(), allow_null=True, required=False)
  department = serializers.PrimaryKeyRelatedField(queryset=models.Department.objects.all(), allow_null=True, required=False)
  
  class Meta:
    model = models.Employee
    fields = [
      'id',
      'url',
      'user',
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
    
  def create(self, validated_data):
    try:
      user_data = validated_data.pop('user')
      user_data.update(employee_id=validated_data['employee_id'])
      user = get_user_model().objects.create(**user_data)
      validated_data.update(user=user.id)
      employee =  super().create(validated_data)
    except Exception:
      employee =  super().create(validated_data)

    return employee

  def update(self, instance, validated_data):
    try:
      user_data = validated_data.pop('user')
      if 'employee_id' in validated_data:
        user_data.update(employee_id=validated_data['employee_id'])
      user_instance = get_user_model().objects.get(employee__id=instance.id)
      nested_serializer = self.fields['user']
      user = nested_serializer.update(self, user_instance, user_data)
      employee = super().update(instance, validated_data)
    except  Exception as e:
        print(f"There was an exception: {e}")
        employee = super().update(instance, validated_data)

    return employee


class BranchSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  phone_numbers = PhoneSerializer(many=True, allow_null=True, required=False)
  
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
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all(), allow_null=True, required=False)
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all(), allow_null=True, required=False)
  
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


class ClientResponseSerializer(ClientSerializer):
  
  employees = EmployeeSerializer(many=True, read_only=True)
  
  class Meta(ClientSerializer.Meta):
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
 