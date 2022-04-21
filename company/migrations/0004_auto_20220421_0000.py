# Generated by Django 3.2.9 on 2022-04-21 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['id'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterField(
            model_name='event',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Started', 'Started'), ('Completed', 'Completed')], default='Pending', max_length=250),
        ),
    ]
