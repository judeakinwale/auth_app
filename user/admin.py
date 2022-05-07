from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user import models
from company.models import Company

# Register your models here.

class CompanyInline(admin.TabularInline):
  model = Company


class UserAdmin(BaseUserAdmin):
  ordering = ['id']
  list_display = ['email', 'first_name', 'last_name']
  fieldsets = (
      # (None, {'fields': ('email', 'password')}),
      (_('Personal Info'), {'fields': ('first_name', 'last_name', 'middle_name', 'username', 'email', 'employee_id',)}),
      (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_employee', 'is_superuser')
      }),
      (_('Important Dates'), {'fields': ('last_login',)}),
      (_('Other'), {'fields': ('groups', 'user_permissions')})
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'username', 'password1', 'password2')
    }),
    (_('Permissions'), {
      'fields': ('is_active', 'is_staff', 'is_employee', 'is_superuser')
    }),
  )
  # inlines = [CompanyInline]


admin.site.register(models.User, UserAdmin)