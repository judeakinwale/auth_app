# Generated by Django 3.2.9 on 2022-04-21 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20220421_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]