# Generated by Django 3.2.9 on 2022-04-22 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0007_company_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='admin',
            field=models.OneToOneField(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='admin'),
        ),
    ]