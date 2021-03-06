from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company import views

app_name = 'company'

router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('branch', views.BranchViewSet)
router.register('department', views.DepartmentViewSet)
router.register('employee', views.EmployeeViewSet)
router.register('location', views.LocationViewSet)
router.register('client', views.ClientViewSet)
router.register('event', views.EventViewSet)
router.register('month', views.MonthViewSet)
router.register('schedule', views.ScheduleViewSet)
router.register('week', views.WeekViewSet)

urlpatterns = [
  path("", include(router.urls)),
  path("employee/account", views.EmployeeAccountView.as_view(), name='employee_acccount'),
  path("employee/email", views.EmployeeSetupEmailView.as_view(), name='employee_email'),
  path("week/report", views.WeeklyReportView.as_view(), name='weekly_report'),
  path("client/<id>/employee/add", views.AddClientEmployeeView.as_view(), name='client_employee_add'),
  path("client/<id>/employee/remove", views.DeleteClientEmployeeView.as_view(), name='client_employee_remove'),
  path("month/<id>/publish", views.PublishMonthView.as_view(), name='publish_month'),
  path("month/<id>/events", views.MonthEventView.as_view(), name='month_event'),
  # path("test/", views.test, name="testing"),
]
