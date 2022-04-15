from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company import views

app_name = 'company'

router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('branch', views.BranchViewSet)
router.register('department', views.DepartmentViewSet)
router.register('employee', views.EmployeeViewSet)

# branch_router = DefaultRouter()
# router.register('branch', views.BranchViewSet)

urlpatterns = [
  path("", include(router.urls)),
  # path("", include(branch_router.urls))
]
