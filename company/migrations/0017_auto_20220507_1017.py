# Generated by Django 3.2.9 on 2022-05-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_auto_20220507_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='end_date',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='week',
            name='start_date',
            field=models.CharField(max_length=250),
        ),
    ]