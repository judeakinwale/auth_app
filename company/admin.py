from django.contrib import admin
from company import models

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.Phone)
admin.site.register(models.Branch)
admin.site.register(models.Department)
admin.site.register(models.Employee)
