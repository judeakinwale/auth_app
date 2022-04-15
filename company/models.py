from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Company(models.Model):

    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True)
    local_govt = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    zip_code = models.CharField(max_length=250, null=True, blank=True)
    contact_person = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      null=True, blank=True
    )
    website = models.CharField(max_length=250, null=True)
    logo = models.ImageField(upload_to='images/%Y/%m/%d/company', blank=True, null=True, max_length=254)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name


class Phone(models.Model):

    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="phone_numbers", on_delete=models.CASCADE)
    branch = models.ForeignKey("Branch", verbose_name=_("Branch"), related_name="phone_numbers", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

    def __str__(self):
        return f"{self.company.name} - {self.phone_number}"
      

class Department(models.Model):

    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="departments", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name


class Branch(models.Model):

    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="branches", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True)
    local_govt = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    zip_code = models.CharField(max_length=250, null=True, blank=True)
    contact_person = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name

