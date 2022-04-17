from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user import models

# Register your models here.

class UserAdmin(BaseUserAdmin):
  ordering = ['id']
  list_display = ['email', 'first_name', 'last_name']
  fieldsets = (
      # (None, {'fields': ('email', 'password')}),
      (_('Personal Info'), {'fields': ('first_name', 'last_name', 'middle_name', 'username', 'email', 'employee_id')}),
      (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_employee', 'is_superuser')
      }),
      (_('Important Dates'), {'fields': ('last_login',)}),
      (_('Other'), {'fields': ('groups', 'user_permissions')})
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'password1', 'password2')
    }),
  )


admin.site.register(models.User, UserAdmin)