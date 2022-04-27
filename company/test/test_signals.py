# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from django.db.models.signals import post_save 
# from user.models import User


# # Add different users to relevant groups
# staff_group, is_created = Group.objects.get_or_create(name ='staff')
# employee_group, is_created = Group.objects.get_or_create(name ='employee')

# @receiver(post_save, sender=User)
# def assign_group(sender, instance, created=False, **kwargs):
#   if created and instance.is_staff:
#     # add instance to the group (if is_staff is true and it is a new entry)
#     staff_group.user_set.add(instance)
      
#   if created and instance.is_employee:
#     # add instance to the group (if is_employee is true and it is a new entry)
#     employee_group.user_set.add(instance)