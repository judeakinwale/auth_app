from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets, permissions
from rest_framework import status
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
        operation_description="list all companys",
        operation_summary='list companys'
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

