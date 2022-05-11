# Generated by Django 3.2.9 on 2022-05-10 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_month_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months', to='company.company', verbose_name='Company'),
        ),
    ]