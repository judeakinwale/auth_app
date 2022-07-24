from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as JWTViews
from user import views

app_name = 'user'

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('trial', views.TrialViewSet)
router.register(
    'passwordreset', 
    views.DecoratedResetPasswordRequestTokenViewSet, 
    basename='reset-password-request',
)
router.register(
    'passwordreset/confirm', 
    views.DecoratedResetPasswordConfirmViewSet, 
    basename='reset-password-confirm',
)
router.register(
    'passwordreset/validate', 
    views.DecoratedResetPasswordValidateTokenViewSet, 
    basename='reset-password-validate',
)
# router.register(
#     'user/trial', 
#     views.TrialUserApiView(), 
#     basename='trial-user',
# )

urlpatterns = [
    path("", include(router.urls)),
    path('account/', views.ManageUserApiView.as_view(), name="account"),
    path("login/", views.DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path('logout/', views.LogoutApiView.as_view(), name="logout"),
    path("token/verify", views.DecoratedTokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh", views.DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("user/trial", views.TrialUserApiView.as_view(), name="trial-user-detail"),
]
