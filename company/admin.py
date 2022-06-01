from django.contrib import admin
from company import models

# Register your models here.

class EventAdmin(admin.ModelAdmin):
  list_display = [
    "company",
    "client",
    "employee",
    "end_date",
    "date",
    "is_active",
    "status",
  ]


admin.site.register(models.Company)
admin.site.register(models.Phone)
admin.site.register(models.Branch)
admin.site.register(models.Department)
admin.site.register(models.Employee)
admin.site.register(models.Location)
admin.site.register(models.Client)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Month)
admin.site.register(models.Schedule)
admin.site.register(models.Week)
