# Using signals, group and permissions
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save 
from user.models import User

# Sending emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from user import urls
from datetime import datetime, timezone


# Add different users to relevant groups
staff_group, is_created = Group.objects.get_or_create(name ='staff')
employee_group, is_created = Group.objects.get_or_create(name ='employee')

@receiver(post_save, sender=User)
def assign_group(sender, instance, created=False, **kwargs):
    if created and instance.is_staff:
        # add instance to the group (if is_staff is true and it is a new entry)
        staff_group.user_set.add(instance)
        
    if created and instance.is_employee:
        # add instance to the group (if is_employee is true and it is a new entry)
        employee_group.user_set.add(instance)


# For django-passwordreset
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    title = "App"
    urls_app_name = urls.app_name
    sender_email = f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>"
    frontend_url = "http://www.hrtechleft.com/forgotPassword/"  # "https://hrtechleft.herokuapp.com/resetPassword/"
    backend_url = instance.request.build_absolute_uri(reverse(f'{urls_app_name}:reset-password-confirm-list'))
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(
        'reset_password_url': "{}{}".format(
            frontend_url,
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset",
        # message:
        email_plaintext_message,
        # from:
        sender_email,  # "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    try:
        msg.send()
    except Exception as e:
        print(f"There was an error sending the mail: {e}")


def disable_trial_users():
    trial_users = User.objects.filter(is_trial=True)
    print("trial_users: ", trial_users)
    for user in trial_users:
        # check if time difference is greater than or equal to seven days
        time_difference  = datetime.now(timezone.utc) - user.timestamp
        if time_difference.days >= 7:
            user.is_active = False
            user.save()
            
disable_trial_users()
