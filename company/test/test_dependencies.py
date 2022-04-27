from django.contrib.auth.models import Group
from company import models


def sample_phone(phone_number='010000001', **kwargs):
  """create and return a sample phone number"""
  defaults = {}.update(kwargs)
  return models.Phone.objects.create(phone_number=phone_number, **defaults)



def sample_company(name: str = "Company 1", email: str = "company1@app.com", **kwargs):
  """create and return sample company"""
  defaults = {
    'name': name,
    'email': email,
  }
  defaults.update(kwargs)
  return models.Company.objects.create(**defaults)

def sample_employee(user, employee_id: str = "EMP001", **kwargs):
  """create and return sample employee"""
  defaults = {
    'user': user,
    'employee_id': employee_id,
  }
  defaults.update(kwargs)
  return models.Employee.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
  """test model attributes against a payload, with instance being self in a testcase class """
  ignored_keys = ['image', 'logo']
  relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
  for key in relevant_keys:
    try:
      insance.assertEqual(payload[key], getattr(model, key))
    except Exception:
      insance.assertEqual(payload[key], serializer.data[key])


def create_staff_group():
  staff_group, is_created = Group.objects.get_or_create(name ='staff')
  return staff_group

def create_employee_group():
  employee_group, is_created = Group.objects.get_or_create(name ='employee')
  

# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from django.db.models.signals import post_save 
# from user.models import User


# Add different users to relevant groups
staff_group, is_created = Group.objects.get_or_create(name ='staff')
employee_group, is_created = Group.objects.get_or_create(name ='employee')

# @receiver(post_save, sender=User)
# def assign_group(sender, instance, created=False, **kwargs):
#   if created and instance.is_staff:
#     # add instance to the group (if is_staff is true and it is a new entry)
#     staff_group.user_set.add(instance)
      
#   if created and instance.is_employee:
#     # add instance to the group (if is_employee is true and it is a new entry)
#     employee_group.user_set.add(instance)
