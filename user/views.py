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
    # permission_classes = [permissions.IsAuthenticated]
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
    # permission_classes = [permissions.IsAuthenticated]
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
