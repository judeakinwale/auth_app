from rest_framework import status, views, response
from drf_yasg.utils import no_body, swagger_auto_schema
from datetime import datetime
import string
import random


def usable_time(time: str) -> datetime.time:
    time = datetime.strptime(time, "%I:%M %p")
    return time


def hourly_time_difference(start: datetime, end: datetime):
    difference = (end - start).total_seconds()
    hours = divmod(difference, 3600)[0]
    return hours


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def code_generator(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))


def auth_user_company(request):
    try:
        if request.user.is_staff:
            return request.user.company
        return request.user.employee.company
    except:
        raise Exception("Company not found")


def company_filtered_queryset(request, model, filter_param=None):
    try:
        if filter_param == "id":
            return model.objects.filter(name=auth_user_company(request).name)
        return model.objects.filter(company=auth_user_company(request))
    except Exception:
        return model.objects.none()


def base_viewset_error_handler(fn):
    """
    For Edge Case Error Handling in Viewset:
    
    Replaces code of the form:
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    """
    try:
        return fn
    except Exception as e:
        error_resp = {'detail': f"{e}"}
        # raise Exception(f"{error_resp}")
        return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class BaseSwaggerDocumentationMixin(object):
    """Generic Swagger Documentation Mixin"""
    
    def __init__(self, subject:str, article:str, plural:str=None):
        self.subject = subject or "instance"
        self.article = article or "a"
        self.plural = plural or f"{doc_subject}s"

    def get_subject(self):
        return self.subject

    def get_article(self):
        return self.article

    def get_plural(self):
        return self.plural  
    
    doc_subject:str = lambda self : self.subject
    doc_article:str = lambda self : self.article
    doc_plural:str = lambda self : self.plural

    @swagger_auto_schema(
        operation_description=f"create {doc_article} {doc_subject}",
        operation_summary=f'create {doc_subject}'
    )
    def create(self, request, *args, **kwargs):
        """create method docstring"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description=f"list all {doc_plural}",
        operation_summary=f'list {doc_plural}'
    )
    def list(self, request, *args, **kwargs):
        """list method docstring"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=f"retrieve {doc_article} {doc_subject}",
        operation_summary=f'retrieve {doc_subject}'
    )
    def retrieve(self, request, *args, **kwargs):
        """retrieve method docstring"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=f"update {doc_article} {doc_subject}",
        operation_summary=f'update {doc_subject}'
    )
    def update(self, request, *args, **kwargs):
        """update method docstring"""
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description=f"partial_update {doc_article} {doc_subject}",
        operation_summary=f'partial_update {doc_subject}'
    )
    def partial_update(self, request, *args, **kwargs):
        """partial_update method docstring"""
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description=f"delete {doc_article} {doc_subject}",
        operation_summary=f'delete {doc_subject}'
    )
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            error_resp = {'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    
def swagger_documentation_factory(
    doc_subject = "instance",
    doc_article = "a",
    doc_plural = None,
    ):
    """Return A Swagger Documentation Mixin, built using the 
    class keyword"""
    
    # generate a default plural if none is provided
    doc_plural = f"{doc_subject}s" if doc_plural is None else doc_plural


    class BaseSwaggerDocumentationMixin:
        
        @swagger_auto_schema(
            operation_description=f"create {doc_article} {doc_subject}",
            operation_summary=f'create {doc_subject}'
        )
        def create(self, request, *args, **kwargs):
            """create method docstring"""
            return base_viewset_error_handler(super().create(request, *args, **kwargs))
        
        @swagger_auto_schema(
            operation_description=f"list all {doc_plural}",
            operation_summary=f'list {doc_plural}'
        )
        def list(self, request, *args, **kwargs):
            """list method docstring"""
            return super().list(request, *args, **kwargs)

        @swagger_auto_schema(
            operation_description=f"retrieve {doc_article} {doc_subject}",
            operation_summary=f'retrieve {doc_subject}'
        )
        def retrieve(self, request, *args, **kwargs):
            """retrieve method docstring"""
            return super().retrieve(request, *args, **kwargs)

        @swagger_auto_schema(
            operation_description=f"update {doc_article} {doc_subject}",
            operation_summary=f'update {doc_subject}'
        )
        def update(self, request, *args, **kwargs):
            """update method docstring"""
            return base_viewset_error_handler(super().update(request, *args, **kwargs))

        @swagger_auto_schema(
            operation_description=f"partial_update {doc_article} {doc_subject}",
            operation_summary=f'partial_update {doc_subject}'
        )
        def partial_update(self, request, *args, **kwargs):
            """partial_update method docstring"""
            return base_viewset_error_handler(super().partial_update(request, *args, **kwargs))

        @swagger_auto_schema(
            operation_description=f"delete {doc_article} {doc_subject}",
            operation_summary=f'delete {doc_subject}'
        )
        def destroy(self, request, *args, **kwargs):
            """destroy method docstring"""
            return base_viewset_error_handler(super().destroy(request, *args, **kwargs))
    
    return BaseSwaggerDocumentationMixin

