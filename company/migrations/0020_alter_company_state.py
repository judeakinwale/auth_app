# Generated by Django 3.2.9 on 2022-05-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_alter_company_contact_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]