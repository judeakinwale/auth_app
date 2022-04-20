from django.conf import settings
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from rest_framework import status, views, response
from company import serializers, models, filters

from drf_yasg.utils import no_body, swagger_auto_schema

# Create your views here.


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.CompanyFilter

    def perform_create(self, serializer):
        return serializer.save()

    @swagger_auto_schema(
        operation_description="create a company",
        operation_summary='create company'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all companies",
        operation_summary='list companies'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a company",
        operation_summary='retrieve company'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a company",
        operation_summary='update company'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a company",
        operation_summary='partial_update company'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a company",
        operation_summary='delete company'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class BranchViewSet(viewsets.ModelViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    serializer_action_classes = {
        'list': serializers.BranchResponseSerializer,
        'retrieve': serializers.BranchResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.BranchFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create a company branch",
        operation_summary='create company branch'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all company branches",
        operation_summary='list company branches'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a company branch",
        operation_summary='retrieve company branch'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a company branch",
        operation_summary='update company branch'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a company branch",
        operation_summary='partial_update company branch'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a company branch",
        operation_summary='delete company branch'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    serializer_action_classes = {
        'list': serializers.DepartmentResponseSerializer,
        'retrieve': serializers.DepartmentResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.DepartmentFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create a company department",
        operation_summary='create company department'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all company departments",
        operation_summary='list company departments'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a company department",
        operation_summary='retrieve company department'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a company department",
        operation_summary='update company department'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a company department",
        operation_summary='partial_update company department'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a company department",
        operation_summary='delete company department'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    serializer_action_classes = {
        'list': serializers.EmployeeResponseSerializer,
        'retrieve': serializers.EmployeeResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.EmployeeFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create an employee",
        operation_summary='create employee'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all employees",
        operation_summary='list employees'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve an employee",
        operation_summary='retrieve employee'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update an employee",
        operation_summary='update employee'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update an employee",
        operation_summary='partial_update employee'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete an employee",
        operation_summary='delete employee'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)
    

class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    serializer_action_classes = {
        'list': serializers.LocationResponseSerializer,
        'retrieve': serializers.LocationResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.LocationFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create a company location",
        operation_summary='create company location'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all company locations",
        operation_summary='list company locations'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a company location",
        operation_summary='retrieve company location'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a company location",
        operation_summary='update company location'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a company location",
        operation_summary='partial_update company location'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a company location",
        operation_summary='delete company location'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    serializer_action_classes = {
        'list': serializers.ClientResponseSerializer,
        'retrieve': serializers.ClientResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.ClientFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create a client",
        operation_summary='create client'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all clients",
        operation_summary='list clients'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve a client",
        operation_summary='retrieve client'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update a client",
        operation_summary='update client'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update a client",
        operation_summary='partial_update client'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete a client",
        operation_summary='delete client'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)



class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    serializer_action_classes = {
        'list': serializers.EventResponseSerializer,
        'retrieve': serializers.EventResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.EventFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="create an event",
        operation_summary='create event'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="list all events",
        operation_summary='list events'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="retrieve an event",
        operation_summary='retrieve event'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="update an event",
        operation_summary='update event'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="partial_update an event",
        operation_summary='partial_update event'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete an event",
        operation_summary='delete event'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        return super().destroy(request, *args, **kwargs)



class EmployeeSetupEmailView(generics.GenericAPIView):
    
    # queryset = models.EmailLink.objects.all()
    serializer_class = serializers.EmployeeSetupEmailSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # serializer = serializers.EmployeeSetupEmailSerializer
    
    @swagger_auto_schema(
        operation_description="Create and Send Company Link to an email",
        operation_summary='Create and Send Company Link to email'
    )
    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def create(self, request, *args, **kwargs):
    #     """create method docstring"""
    #     return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data['link'] = f"link for {serializer.validated_data['email']}"
        print(serializer.validated_data)

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)
