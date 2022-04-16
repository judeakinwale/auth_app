from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from user import managers
from company.mixins import EmployeePermissionsMixin

# Create your models here.


class Company(models.Model):

    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True)
    province = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    contact_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    website = models.CharField(max_length=250, null=True)
    logo = models.ImageField(upload_to='images/company/%Y/%m/%d/', blank=True, null=True, max_length=254)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    # TODO: Add properties for phone_numbers, employees

    def __str__(self):
        return self.name


class Phone(models.Model):

    # TODO: Remove company from phone model
    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="phone_numbers", on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey("Branch", verbose_name=_("Branch"), related_name="phone_numbers", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

    def __str__(self):
        return f"{self.company.name} - {self.phone_number}"


class Department(models.Model):

    # TODO: Remove company from Department model
    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="departments", on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey("Branch", verbose_name=_("Branch"), related_name="departments", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name


class Branch(models.Model):

    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="branches", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True)
    province = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    contact_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name


class Employee(AbstractBaseUser, EmployeePermissionsMixin):

    class RoleChoices(models.TextChoices):
        Admin = 'Admin', _('Admin')
        HR = 'HR', _('HR')
        Staff = 'Staff', _('Staff')
        Manager = 'Manager', _('Manager')
        Team_Lead = 'Team Lead', _('Team Lead')

    first_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=50, null=True, blank=True)
    # TODO: Remove company from employee model
    company = models.ForeignKey(Company, verbose_name=_("Company"), related_name="employees", on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), related_name="employees", on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, verbose_name=_("Department"), related_name="employees", on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=250, null=True)
    role = models.CharField(
        max_length=250,
        choices=RoleChoices.choices,
        default=RoleChoices.Staff,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True)
    province = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='images/profile/%Y/%m/%d/', blank=True, null=True, max_length=254)
    hobbies = models.TextField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Location(models.Model):

    company = models.OneToOneField(Company, verbose_name=_("Company"), related_name="location", on_delete=models.CASCADE)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    # Replacement for longitude and latitude
    # point = models.PointField(srid=4326,dim=3) # for postgres db
    accuracy = models.FloatField(default=0.0) # meters, rounded up
    altitude = models.FloatField(null=True, blank=True) # meters, rounded
    max_radius = models.FloatField(default=0.0, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        try:
            return f"{self.company.name} - y: {self.longitude}, x: {self.latitude}"
        except Exception:
            return f"{self.company.name}"