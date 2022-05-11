from django.conf import settings
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from rest_framework import status, views, response
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
from user.utils import EmployeeResponseSerializer

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
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    
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
        try:
            return super().update(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="partial_update a user",
        operation_summary='partial_update user'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        try:
            return super().partial_update(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

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
    # serializer_action_classes = {
    #     'get': EmployeeResponseSerializer,
    #     'put': EmployeeResponseSerializer,
    #     'patch': EmployeeResponseSerializer,
    # }
    permission_classes = [permissions.IsAuthenticated]
    # filterset_class = filters.UserFilter

    def get_object(self):
        """retrieve and return the authenticated user's account"""
        # try:
        #     return self.request.user.employee
        # except:
        #     return self.request.user
        return self.request.user
    
    def get_serializer_class(self):
        # try:
        #     print(request.method)
        #     if request.method == "GET":
        #         print("----GET----")
        #     # return EmployeeResponseSerializer
        #     return self.serializer_action_classes[self.action]
        # except:
        #     return super().get_serializer_class()
        return super().get_serializer_class()
    
    @swagger_auto_schema(
        operation_description="retrieve authenticated user details",
        operation_summary='retrieve authenticated user details (account)'
    )
    def get(self, request, *args, **kwargs):
        """get method docstring"""
        # self.serializer_class = EmployeeResponseSerializer
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
    

# Simple JWT integration with drf-yasg (views)
# Decorated drf-simplejwt views
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description='login',
        operation_summary='login',
        responses={
            status.HTTP_200_OK: serializers.TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description='generata access token using refresh token',
        operation_summary='generata access token using refresh token',
        responses={
            status.HTTP_200_OK: serializers.TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description='verify access token is still valid',
        operation_summary='verify access token is still valid',
        responses={
            status.HTTP_200_OK: serializers.TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


# django-passwordreset integration with drf-yasg (views)
# Decorated django-passwordreset views
class DecoratedResetPasswordValidateTokenViewSet(ResetPasswordValidateTokenViewSet):
    @swagger_auto_schema(
        operation_description='validate password reset token',
        operation_summary='validate password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    

class DecoratedResetPasswordConfirmViewSet(ResetPasswordConfirmViewSet):
    @swagger_auto_schema(
        operation_description='confirm password reset token',
        operation_summary='confirm password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    

class DecoratedResetPasswordRequestTokenViewSet(ResetPasswordRequestTokenViewSet):
    @swagger_auto_schema(
        operation_description='request password reset token',
        operation_summary='request password reset token',
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
            print(**kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
