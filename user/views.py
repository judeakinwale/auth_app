from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from user import serializers, models, filters

from django_rest_passwordreset.signals import reset_password_token_created
from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.UserFilter

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            reciepients = [user.email]
            app_url =  self.request.get_full_path()
            app_name = "App" # Application Name
            context = {
                "user": user,
                "app_name": app_name,
                "login_url": f"{app_url}/api-auth/login/"
            }
            utils.send_account_creation_email(self.request, reciepients, context)
        except Exception as e:
            print(f"user creation email error: {e} \n")

        return user

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

# For django-passwordreset
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


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
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
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
