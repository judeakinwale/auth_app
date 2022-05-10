from rest_framework import serializers
from django.contrib.auth import get_user_model
from company import models
from user.utils import UserSerializer


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


class MonthSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all(), allow_null=True, required=False)
  # client = serializers.PrimaryKeyRelatedField(queryset=models.Client.objects.all(), allow_null=True, required=False)
  
  class Meta:
    model = models.Month
    fields = [
      'id',
      'url',
      'company',
      # 'client',
      'month',
      'year',
      'index',
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
      'url': {'view_name': 'company:month-detail'},
    }


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
  
  client = serializers.PrimaryKeyRelatedField(queryset=models.Client.objects.all(), allow_null=True, required=False)
  month = serializers.PrimaryKeyRelatedField(queryset=models.Month.objects.all(), allow_null=True, required=False)
  
  class Meta:
    model = models.Schedule
    fields = [
      'id',
      'url',
      'client',
      'month',
      # 'year',
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
      'url': {'view_name': 'company:schedule-detail'},
    }


class WeekSerializer(serializers.HyperlinkedModelSerializer):
  
  client = serializers.PrimaryKeyRelatedField(queryset=models.Client.objects.all(), allow_null=True, required=False)
  
  class Meta:
    model = models.Week
    fields = [
      'id',
      'url',
      'client',
      'name',
      'start_date',
      'end_date',
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
      'url': {'view_name': 'company:week-detail'},
    }


class WeeklyReportSerializer(serializers.Serializer):
  
  weeks = serializers.ListField(
    child=serializers.IntegerField()
  )


class EmployeeHelperSerializer(serializers.Serializer):
  
  id = serializers.CharField()


class EmployeeSetupEmailSerializer(serializers.Serializer):

  email = serializers.CharField()
  link = serializers.CharField(read_only=True)
  
  # class Meta:
  #   model = models.EmailLink
  #   # fields = ['email']
  #   fields = "__all__"
  
  def create(self, validated_data):
    raise NotImplementedError()
  
  def update(self, instance, validated_data):
    raise NotImplementedError()


class CompanyBaseSerializer(serializers.HyperlinkedModelSerializer):
  
  phone_numbers = PhoneSerializer(many=True, allow_null=True, required=False)
  contact_person = serializers.PrimaryKeyRelatedField(queryset=models.Employee.objects.all(), allow_null=True, required=False)
  admin = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(is_staff=True), allow_null=True, required=False)
  
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
      'admin',
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


class EventSerializer(serializers.HyperlinkedModelSerializer):
  
  company = serializers.PrimaryKeyRelatedField(queryset=models.Company.objects.all())
  employee = serializers.PrimaryKeyRelatedField(queryset=models.Employee.objects.all(), allow_null=True, required=False)
  client = serializers.PrimaryKeyRelatedField(queryset=models.Client.objects.all(), allow_null=True, required=False)
  
  class Meta:
    model = models.Event
    # fields = "__all__"
    fields = [
      'id',
      'url',
      'company',
      'employee',
      'client',
      'name',
      'start_time',
      'end_time',
      'date',
      'note',
      'status',
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
      'url': {'view_name': 'company:event-detail'},
    }
    

# class MultipleEventSerializer(serializers.Serializer):

#   events = EventSerializer(many=True)

  
#   def create(self, validated_data):
#     raise NotImplementedError()
  
#   def update(self, instance, validated_data):
#     raise NotImplementedError()


class LocationSerializer(serializers.HyperlinkedModelSerializer):
  
  branch = serializers.PrimaryKeyRelatedField(queryset=models.Branch.objects.all())
  
  class Meta:
    model = models.Location
    fields = [
      'id',
      'url',
      'branch',
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
  # employees = EmployeeSerializer(many=True, read_only=True)
  employee = EmployeeHelperSerializer(write_only=True, allow_null=True, required=False)
  # employee = serializers.PrimaryKeyRelatedField(queryset=models.Employee.objects.all())
  
  class Meta:
    model = models.Client
    fields = [
      'id',
      'url',
      'company',
      # 'branch',
      # 'employees',
      'employee',
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
      'employee': {'write_only': True, 'required': False, 'allow_null': True},
    }
    depth = 1
    
  def create(self, validated_data):
    try:
      employee_data = validated_data.pop('employee')
      client =  super().create(validated_data)
      
      employee = models.Employee.objects.get(id=employee_data['id'])
      client.employees.add(employee)

    except Exception as e:
      client =  super().create(validated_data)

    return client

  def update(self, instance, validated_data):
    try:
      employee_data = validated_data.pop('employee')
      client =  super().update(instance, validated_data)
      
      employee = models.Employee.objects.get(id=employee_data['id'])
      if employee not in client.employees.all():
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
      user_data.update(is_employee=True)
      user = get_user_model().objects.create_user(**user_data)
      validated_data.update(user=user)
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
      user = nested_serializer.update(user_instance, user_data)
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
          phone_number = nested_serializer.update(nested_instance, nested_data) # Where nested serializer = PhoneSerializer
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
          phone_number = nested_serializer.update(nested_instance, nested_data) # Where nested serializer = PhoneSerializer
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
  
  branch = BranchSerializer(read_only=True)
  
  class Meta(LocationSerializer.Meta):
    depth = 0


class MonthResponseSerializer(MonthSerializer):

  company = CompanySerializer(read_only=True)
  # client = ClientSerializer(read_only=True)
  
  class Meta(MonthSerializer.Meta):
    depth = 0


class ScheduleResponseSerializer(ScheduleSerializer):
  
  client = ClientSerializer(read_only=True)
  month = MonthSerializer(read_only=True)
  
  class Meta(ScheduleSerializer.Meta):
    depth = 0


class WeekResponseSerializer(WeekSerializer):
  
  client = ClientSerializer(read_only=True)
  
  class Meta(WeekSerializer.Meta):
    depth = 0


class ClientResponseSerializer(ClientSerializer):
  
  employees = EmployeeSerializer(many=True, read_only=True)
  
  class Meta(ClientSerializer.Meta):
    additional_fields = ['employees']
    # unused_fields = ClientSerializer.Meta.fields.remove("employee")
    fields = ClientSerializer.Meta.fields + additional_fields
    depth = 0


class EmployeeResponseSerializer(EmployeeSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  branch = BranchSerializer(read_only=True)
  department = DepartmentSerializer(read_only=True)
  
  class Meta(EmployeeSerializer.Meta):
    depth = 0
    
    
class EventResponseSerializer(EventSerializer):
  
  company = CompanyBaseSerializer(read_only=True)
  employee = EmployeeSerializer(read_only=True)
  client = ClientSerializer(read_only=True)
  
  class Meta(EventSerializer.Meta):
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
 