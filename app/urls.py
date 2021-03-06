"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from app.schema import schema_view
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

# @csrf_exempt
# def render_react(request):
#     context = {}
#     return render(request, "index.html", context)

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r"^$", render_react),
    # re_path(r"^(?:.*)/?$", render_react),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('user.urls', namespace='user')),
    path('', include('company.urls', namespace='company')),
    # path("password_reset/", include('django_rest_passwordreset.urls', namespace='password_reset')), # For django-rest-passwordreset
    
    # For drf-yasg
    path("swagger(<format>\\.json|\\.yaml)", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
