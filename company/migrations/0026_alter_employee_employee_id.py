# Generated by Django 3.2.9 on 2022-05-28 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0025_event_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
