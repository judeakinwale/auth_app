from django.conf import settings
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.db.models import Q
from datetime import datetime, date, time

from rest_framework import generics, viewsets, permissions
from rest_framework import status, views, response
from company import serializers, models, filters, utils
# from company.models import Company
from util import utils as utility

from drf_yasg.utils import no_body, swagger_auto_schema

# Using signals, group and permissions
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save 

import calendar # For get weekly report weeks

# Create your views here.

request_user = ""


class CompanyViewSet(utility.swagger_documentation_factory("company", "a", "companies"), viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.CompanyFilter

    def perform_create(self, serializer):
        if models.Company.objects.filter(admin=request.user):
            raise Exception("You've created another company")
        
        if not self.request.user.is_superuser:
            serializer.validated_data['admin'] = self.request.user
        return super().perform_create(serializer)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return utility.company_filtered_queryset(self.request, models.Company, "id")


class BranchViewSet(utility.swagger_documentation_factory("branch", "a", "branches"), viewsets.ModelViewSet):
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
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return utility.company_filtered_queryset(self.request, models.Branch)


class DepartmentViewSet(utility.swagger_documentation_factory("company department"), viewsets.ModelViewSet):
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
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Department.objects.filter(company=self.request.user.company)    
            return models.Department.objects.filter(company=self.request.user.employee.company)
        except Exception:
            return models.Department.objects.none()


class EmployeeViewSet(utility.swagger_documentation_factory("Employee", "an"), viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    serializer_action_classes = {
        'list': serializers.EmployeeResponseSerializer,
        'retrieve': serializers.EmployeeResponseSerializer,
    }
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.EmployeeFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Employee.objects.filter(company=self.request.user.company)    
            return models.Employee.objects.filter(company=self.request.user.employee.company)
        except Exception:
            return models.Employee.objects.none()
        
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        try:
            employee = self.get_object()
            user = employee.user
            user.delete()
        except Exception as e:
            error_resp = {"detail": f"Error Deleting user: {e}"}
            return response.Response(error_resp, status=status.HTTP_404_NOT_FOUND)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        


class LocationViewSet(utility.swagger_documentation_factory("location"), viewsets.ModelViewSet):
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
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Location.objects.filter(company=self.request.user.company)    
            return models.Location.objects.filter(company=self.request.user.employee.company)
        except Exception:
            return models.Location.objects.none()


class ClientViewSet(utility.swagger_documentation_factory("client"), viewsets.ModelViewSet):
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
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Client.objects.filter(company=self.request.user.company)    
            return models.Client.objects.filter(company=self.request.user.employee.company)
        except Exception:
            return models.Client.objects.none()


class EventViewSet(utility.swagger_documentation_factory("event", "an"), viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    serializer_action_classes = {
        'list': serializers.EventResponseSerializer,
        'retrieve': serializers.EventResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = filters.EventFilter

    def perform_create(self, serializer):
        event = ''
        if "date" in serializer.validated_data and "end_date" not in serializer.validated_data:
            event = serializer.save(end_date=serializer.validated_data["date"])
        else:
            event = serializer.save()
            
        try:
            client = event.client
            employee = event.employee
            event_ids = [event.id,]
            active_month = utils.get_month_dates(self.request)
            # if active_month is not None and event.date <= active_month.end_timestamp and event.date >= active_month.start_timestamp:
            if active_month is not None and active_month.start_timestamp <= event.date <= active_month.end_timestamp:
                utils.send_employee_event_email(self.request, employee, event_ids)
                utils.send_client_event_email(self.request, client, event_ids)
        except Exception as e:
            print(e)
            print('An exception occurred while sending mails to client and employee')
        return event
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
       
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(EventViewSet, self).get_serializer(*args, **kwargs)
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Event.objects.filter(company=self.request.user.company)    
            return models.Event.objects.filter(company=self.request.user.employee.company)
        except Exception:
            
            return models.Event.objects.none()
    
    
class MonthViewSet(utility.swagger_documentation_factory("month"), viewsets.ModelViewSet):
    queryset = models.Month.objects.all()
    serializer_class = serializers.MonthSerializer
    serializer_action_classes = {
        'list': serializers.MonthResponseSerializer,
        'retrieve': serializers.MonthResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filterset_class = filters.MonthFilter

    def perform_create(self, serializer):
        try: 
            # month = models.Month.objects.get(month=serializer.validated_data['month'], year=serializer.validated_data['year'])
            # if month:
            #     # error_resp = {'detail': "Month already exists"}
            #     # return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
            #     raise Exception("Month already exists!")
            
            if "company" not in serializer.validated_data:
                if self.request.user.is_staff:
                    return serializer.save(company=self.request.user.company)
                return serializer.save(company=self.request.user.employee.branch.company)
        except Exception as e:
            return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Month.objects.filter(company=self.request.user.company)    
            return models.Month.objects.filter(company=self.request.user.employee.company)
        except Exception:
            return models.Month.objects.none()


class ScheduleViewSet(utility.swagger_documentation_factory("schedule"), viewsets.ModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
    serializer_action_classes = {
        'list': serializers.ScheduleResponseSerializer,
        'retrieve': serializers.ScheduleResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filterset_class = filters.ScheduleFilter

    def perform_create(self, serializer):
        # schedule = models.Schedule.objects.get(month=serializer.validated_data['month'], client=serializer.validated_data['client'])
        # if schedule:
        #     # error_resp = {'detail': "Schedule already exists"}
        #     # return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        #     raise Exception("Schedule already exists!")
        
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        
        try:
            if self.request.user.is_staff:
                return models.Schedule.objects.filter(client__company=self.request.user.company)    
            return models.Schedule.objects.filter(client__company=self.request.user.employee.company)
        except Exception:
            return models.Schedule.objects.none()
        
    def destroy(self, request, *args, **kwargs):
        """destroy method docstring"""
        try:
            schedule = self.get_object()
            month = schedule.month
        except Exception as e:
            error_resp = {"detail": f"Month not found: {e}"}
            return response.Response(error_resp, status=status.HTTP_404_NOT_FOUND)
        try:
            month = utils.get_month_dates(request, month)
            month_start_date = month["start_timestamp"]
            month_end_date = month["end_timestamp"]
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        events = models.Event.objects.none()
        # print(events)
        try:
            if request.user.is_superuser:
                # events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date)
                events = models.Event.objects.none()
                print("User is super user, so, no events deleted")
                # print(events)
            elif request.user.is_staff:
                # events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.company).delete()
                events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.company).delete()
                print("user is a staff, so events deleted")
                print(events)
            else:    
                # events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.employee.company).delete()
                events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.employee.company).delete()
                print("user is an employee, so events deleted")
                print(events)
        except Exception:
            events = models.Event.objects.none()
        # events.delete()
        return super().destroy(request, *args, **kwargs)


class WeekViewSet(utility.swagger_documentation_factory("week"), viewsets.ModelViewSet):
    queryset = models.Week.objects.all()
    serializer_class = serializers.WeekSerializer
    serializer_action_classes = {
        'list': serializers.WeekResponseSerializer,
        'retrieve': serializers.WeekResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filterset_class = filters.WeekFilter

    def perform_create(self, serializer):
        return serializer.save()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
        
    def get_queryset(self):
        # if self.request.user.is_superuser:
        #     return super().get_queryset()
        
        # try:
        #     if self.request.user.is_staff:
        #         return models.Week.objects.filter(company=self.request.user.company)    
        #     return models.Week.objects.filter(company=self.request.user.employee.company)
        # except Exception:
        #     return models.Week.objects.none()
        
        return super().get_queryset()


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
    #     try:
    #         return super().create(request, *args, **kwargs)
    #         print(**kwargs)
    #     except Exception as e:
    #         error_resp = {'detail': f"{e}"}
    #         return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        try:
            link = utils.send_company_link(request, email)
        except Exception as e:
            # print("error:")
            # print(e)
            # print(serializer)
            error_response = {
                'errors': (serializer.errors or f"{e}"),
                'detail': "Link could not be sent"
            }
            return response.Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data['link'] = link
        print(serializer.validated_data)

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)





class WeeklyReportView(generics.GenericAPIView):
    
    serializer_class = serializers.WeeklyReportSerializer
    
    @swagger_auto_schema(
        operation_description="Generate Weekly Report",
        operation_summary='Generate Weekly Report'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        company = ""
        try:
            if request.user.is_staff:
                company=request.user.company
            else:    
                company=request.user.employee.company
        except Exception as e:
            company = None

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("\n\nSerializer valid\n\n")
        try:
            # emp_id = int(serializer.validated_data['id'])
            # client = models.Client.objects.get(id=int(kwargs['id']))
            # employee = models.Employee.objects.get(id=emp_id)
            # client.employees.add(employee)
            # client.refresh_from_db()
            # serialized_client = serializers.ClientResponseSerializer(client)
            # print(serialized_client.data)
            
            weeks_data = serializer.validated_data['weeks']
            weeks = models.Week.objects.none()
            
            try:
                if request.user.is_superuser:
                    weeks = models.Week.objects.filter(id__in=weeks_data)
                elif request.user.is_staff:
                    weeks = models.Week.objects.filter(id__in=weeks_data, client__company=request.user.company)
                else:    
                    weeks = models.Week.objects.filter(id__in=weeks_data, client__company=request.user.employee.company)
            except Exception:
                weeks = models.Week.objects.none()
            
            # print(f"weeks: {weeks}")
            
            serialized_weeks = serializers.WeekResponseSerializer(weeks, many=True, context={'request': request})
            
            events = models.Event.objects.none()
            random_date = "2022-04-25"
            data = []
            for week in weeks:
                print(f"{week.start_date}, {week.end_date} - {week.end_date >= week.start_date} - {random_date >=  week.end_date}")
                events = models.Event.objects.none()
                events |= models.Event.objects.filter(date__gte=week.start_date, date__lte=week.end_date)
                serialized_events = serializers.EventResponseSerializer(events, many=True, context={'request': request})
                report_data = {}
                report_data[f"{week.name}"] = serialized_events.data
                # print(serialized_events.data)
                data.append(report_data)
                
            event_id_list = []
            for event in events:
                event_id_list.append(event.id)
            
            try:
                employees = models.Employee.objects.filter(Q(company=company) | Q(branch__company=company))
                for employee in employees:
                    email = utils.send_employee_weekly_report_email(request, employee, event_id_list)
                    
                clients = models.Client.objects.filter(company=company)
                # print(f"\n\nAll Clients: {clients}\n\n")
                for client in clients:
                    email = utils.send_client_weekly_report_email(request, client, event_id_list)
            except Exception as e:
                print(f'An exception occurred:{e}')
            
            resp_data = {'result': data,}
            return response.Response(resp_data, status=status.HTTP_200_OK)
        except Exception as e:
            # print(f"\n\n{e}\n\n")
            error_resp = {'errors': serializer.errors, 'detail': f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Weeks for Weekly Report",
        operation_summary='Get Weeks for Weekly Report'
    )
    def get(self, request, *args, **kwargs):
        
        try:
            # try:
            #     month = models.Month.objects.get(is_active=True)
            # except Exception as e:
            #     error_resp = {"detail": f"More than one month is active"}
            #     return response.Response(error_resp, status=status.HTTP_404_NOT_FOUND)
            # day = 1
            # year = int(month.year)
            
            # month_repr = f"{day} {month.month}, {month.year}"
            # print(f"month_repr: {month_repr}")
            
            # month_start = datetime.strptime(month_repr, '%d %B, %Y')
            # print(f"month_start: {month_start}")
            
            # month_int = str(datetime.strptime(month.month, '%B'))
            # print(f"month_int: {month_int}")
            # print(f"month_start.month: {month_start.month}")
            
            # month_range = calendar.monthrange(year, month_start.month)
            # print(f"month_range: {month_range}")
            
            # last_day = month_range[1]
            
            # month_end_repr = f"{last_day} {month.month}, {month.year}"
            # print(f"month_end_repr: {month_end_repr}")
            
            # month_end = datetime.strptime(month_end_repr, '%d %B, %Y')
            # print(f"month_end: {month_end}")
            
            # print("month start repr")
            # print(month_start.strftime('%Y-%m-%d'))
            # month_start_date = month_start.strftime('%Y-%m-%d')
            # print("month end repr")
            # print(month_end.strftime('%Y-%m-%d'))
            # month_end_date = month_end.strftime('%Y-%m-%d')
            month = utils.get_month_dates(request)
            month_start_date = month["start_timestamp"]
            month_end_date = month["end_timestamp"]
            
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        weeks = models.Week.objects.none()
        try:
            if request.user.is_superuser:
                # weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date)
                weeks = models.Week.objects.filter()
            elif request.user.is_staff:
                weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date, client__company=request.user.company)
            else:    
                weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date, client__company=request.user.employee.company)
        except Exception:
            weeks = models.Week.objects.none()
        
        # serializer = self.get_serializer(data=request.data)
        serialized_weeks = serializers.WeekResponseSerializer(weeks, many=True, context={'request': request})

        try:
            # serialized_weeks.is_valid(raise_exception=True)
            resp_data = {'result': serialized_weeks.data,}
            return response.Response(resp_data, status=status.HTTP_200_OK)
            # return super().get(request, *args, **kwargs)
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)


class PublishMonthView(generics.GenericAPIView):
    
    # serializer_class = serializers.WeeklyReportSerializer
    
    @swagger_auto_schema(
        operation_description="Publish Month",
        operation_summary='Publish Month'
    )
    def get(self, request, *args, **kwargs):
        
        try:
            all_months = models.Month.objects.all().update(is_active=False)
            month = models.Month.objects.get(id=int(kwargs['id']))
            month.is_active = True
            month.save()
            month.refresh_from_db()
            serialized_month = serializers.MonthResponseSerializer(month, context={'request': request})
            
            try:
                employees = models.Employee.objects.filter(company=month.company)
                for employee in employees:
                    email = utils.send_employee_schedule_publish_email(request, employee)
            except Exception as e:
                print(f'An exception occurred:{e}')
            
            resp_data = {'result': serialized_month.data,}
            return response.Response(resp_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)




class MonthEventView(generics.GenericAPIView):
    
    # serializer_class = serializers.WeeklyReportSerializer
    
    @swagger_auto_schema(
        operation_description="Get all events in a month",
        operation_summary='Get all events in a month'
    )
    # def get(self, request, *args, **kwargs):
        
    #     try:
    #         all_months = models.Month.objects.all().update(is_active=False)
    #         month = models.Month.objects.get(id=int(kwargs['id']))
    #         month.is_active = True
    #         month.save()
    #         month.refresh_from_db()
    #         serialized_month = serializers.MonthResponseSerializer(month, context={'request': request})
            
    #         try:
    #             employees = models.Employee.objects.filter(company=month.company)
    #             for employee in employees:
    #                 email = utils.send_employee_schedule_publish_email(request, employee)
    #         except Exception as e:
    #             print(f'An exception occurred:{e}')
            
    #         resp_data = {'result': serialized_month.data,}
    #         return response.Response(resp_data, status=status.HTTP_200_OK)
            
    #     except Exception as e:
    #         error_resp = {"detail": f"{e}"}
    #         return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):
        
        try:
            month = utils.get_month_dates(request)
            month_start_date = month["start_timestamp"]
            month_end_date = month["end_timestamp"]
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        # weeks = models.Week.objects.none()
        # try:
        #     if request.user.is_superuser:
        #         # weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date)
        #         weeks = models.Week.objects.filter()
        #     elif request.user.is_staff:
        #         weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date, client__company=request.user.company)
        #     else:    
        #         weeks = models.Week.objects.filter(start_date__gte=month_start_date, end_date__lte=month_end_date, client__company=request.user.employee.company)
        # except Exception:
        #     weeks = models.Week.objects.none()
        
        events = models.Event.objects.none()
        try:
            if request.user.is_superuser:
                events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date)
                # print(events)
            elif request.user.is_staff:
                events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.company)
                # print(events)
            else:    
                events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=request.user.employee.company)
                # print(events)
        except Exception:
            events = models.Event.objects.none()
            
        # print(events)
        
        # try:
        #     events = models.Event.objects.filter(date__gte=month_start_date, date__lte=month_end_date, company=company)
        # except:
        #     pass
        
        # serializer = self.get_serializer(data=request.data)
        # serialized_weeks = serializers.WeekResponseSerializer(weeks, many=True, context={'request': request})
        serialized_events = serializers.EventResponseSerializer(events, many=True, context={'request': request})

        try:
            # serialized_weeks.is_valid(raise_exception=True)
            # resp_data = {'result': serialized_weeks.data,}
            resp_data = {'result': serialized_events.data,}
            return response.Response(resp_data, status=status.HTTP_200_OK)
            # return super().get(request, *args, **kwargs)
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class EmployeeAccountView(generics.GenericAPIView):
    
    # serializer_class = serializers.WeeklyReportSerializer
    
    @swagger_auto_schema(
        operation_description="Get Authenticated Employee",
        operation_summary='Get Authenticated Employee'
    )
    def get(self, request, *args, **kwargs):
        
        try:
            employee = models.Employee.objects.get(user=request.user)
            serialized_employee = serializers.EmployeeResponseSerializer(employee, context={'request': request})
            resp_data = {'result': serialized_employee.data,}
            return response.Response(resp_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_resp = {"detail": f"{e}"}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)        


class AddClientEmployeeView(generics.GenericAPIView):
    
    serializer_class = serializers.EmployeeHelperSerializer
    
    @swagger_auto_schema(
        operation_description="Add an Employee to a client",
        operation_summary='Add Employee to client'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            emp_id = int(serializer.validated_data['id'])
            client = models.Client.objects.get(id=int(kwargs['id']))
            employee = models.Employee.objects.get(id=emp_id)
            client.employees.add(employee)
            client.refresh_from_db()
            serialized_client = serializers.ClientResponseSerializer(client)
            print(serialized_client.data)
            
            resp_data = {'data': serialized_client.data, 'detail': 'Employee added sucessfully'}
            return response.Response(resp_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_resp = {'errors': serializer.errors, 'detail': e}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)


class DeleteClientEmployeeView(generics.GenericAPIView):
    
    serializer_class = serializers.EmployeeHelperSerializer
    
    @swagger_auto_schema(
        operation_description="Remove an Employee from a client",
        operation_summary='Remove Employee from client'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            emp_id = int(serializer.validated_data['id'])
            client = models.Client.objects.get(id=int(kwargs['id']))
            employee = models.Employee.objects.get(id=emp_id)
            client.employees.remove(employee)
            
            resp_data = {'data': serializer.validated_data, 'detail': 'Employee removed sucessfully'}
            return response.Response(resp_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_resp = {'errors': serializer.errors, 'detail': e}
            return response.Response(error_resp, status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)
