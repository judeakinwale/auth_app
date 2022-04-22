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
# router.register('employee/email', views.EmployeeSetupEmailView, basename='employee_email')

urlpatterns = [
  path("", include(router.urls)),
  path("employee/email", views.EmployeeSetupEmailView.as_view(), name='employee_email'),
  # path("test/", views.test, name="testing"),
]
