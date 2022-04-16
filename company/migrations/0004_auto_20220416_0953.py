# Generated by Django 3.2.9 on 2022-04-16 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20220415_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='zip_code',
            new_name='postal_code',
        ),
        migrations.RenameField(
            model_name='branch',
            old_name='local_govt',
            new_name='province',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='zip_code',
            new_name='postal_code',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='local_govt',
            new_name='province',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='zip_code',
            new_name='postal_code',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='local_govt',
            new_name='province',
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='hobbies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='join_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, max_length=254, null=True, upload_to='images/company/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='company.department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, max_length=254, null=True, upload_to='images/profile/%Y/%m/%d/'),
        ),
    ]