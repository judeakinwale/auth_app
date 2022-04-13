from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as JWTViews
from user import views

app_name = 'user'

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('account/', views.ManageUserApiView.as_view(), name="account"),
    path("login/", JWTViews.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path('logout/', views.LogoutApiView.as_view(), name="logout"),
    path("token/verify", JWTViews.TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh", JWTViews.TokenRefreshView.as_view(), name="token_refresh"),
]
