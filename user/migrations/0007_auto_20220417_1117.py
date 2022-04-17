# Generated by Django 3.2.9 on 2022-04-17 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
