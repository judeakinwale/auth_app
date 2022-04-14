from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company import views

app_name = 'company'

router = DefaultRouter()
router.register('', views.CompanyViewSet)

urlpatterns = [
  path("", include(router.urls)),
]
