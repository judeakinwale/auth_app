from django.conf import settings
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from rest_framework import status
from rest_framework_simplejwt.views import (
  TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from user import serializers, models, filters, utils

from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import (
    ResetPasswordValidateTokenViewSet, 
    ResetPasswordConfirmViewSet,
    ResetPasswordRequestTokenViewSet
)
from drf_yasg.utils import no_body, swagger_auto_schema
# from util.utils import generate_swagger_overrides

# Using signals, group and permissions
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


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.UserFilter

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            reciepients = [user.email]
            url =  self.request.build_absolute_uri(reverse(f'user:token_obtain_pair')) 
            company = user.employee.company
            context = {
                "user": user,
                "company": company,
                "url": url
            }
            utils.send_account_creation_email(self.request, reciepients, context)
        except Exception as e:
            print(f"user creation email error: {e} \n")

        return user

    # generate_swagger_overrides("a", "user") # Attempt at simplifying swagger overriding
    @swagger_auto_schema(
        operation_description="create a user",
        operation_summary='create user'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all users",
        operation_summary='list users'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a user",
        operation_summary='retrieve user'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a user",
        operation_summary='update user'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a user",
        operation_summary='partial_update user'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a user",
        operation_summary='delete user'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class ManageUserApiView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.UserFilter

    def get_object(self):
        """retrieve and return the authenticated user"""
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="retrieve authenticated user details",
        operation_summary='retrieve authenticated user details (account)'
    )
    def get(self, request, *args, **kwargs):
        """get method docstring"""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update authenticated user details",
        operation_summary='update authenticated user details (account)'
    )
    def put(self, request, *args, **kwargs):
        """put method docstring"""
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial update authenticated user details",
        operation_summary='partial update authenticated user details (account)'
    )
    def patch(self, request, *args, **kwargs):
        """patch method docstring"""
        return super().patch(request, *args, **kwargs)
    

# Modified drf-simplejwt views
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description='login',
        operation_summary='login',
        responses={
            status.HTTP_200_OK: serializers.TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description='generata access token using refresh token',
        operation_summary='generata access token using refresh token',
        responses={
            status.HTTP_200_OK: serializers.TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description='verify access token is still valid',
        operation_summary='verify access token is still valid',
        responses={
            status.HTTP_200_OK: serializers.TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Modified django-passwordreset views
class DecoratedResetPasswordValidateTokenViewSet(ResetPasswordValidateTokenViewSet):
    @swagger_auto_schema(
        operation_description='validate password reset token',
        operation_summary='validate password reset token',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class DecoratedResetPasswordConfirmViewSet(ResetPasswordConfirmViewSet):
    @swagger_auto_schema(
        operation_description='confirm password reset token',
        operation_summary='confirm password reset token',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class DecoratedResetPasswordRequestTokenViewSet(ResetPasswordRequestTokenViewSet):
    @swagger_auto_schema(
        operation_description='request password reset token',
        operation_summary='request password reset token',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)




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
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse(f'{urls_app_name}:reset-password-confirm-list')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset for {title}",
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,  # "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    try:
        msg.send()
    except Exception as e:
        print(f"There was an error sending the mail: {e}")
