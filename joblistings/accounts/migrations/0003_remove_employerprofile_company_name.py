# Generated by Django 5.1.2 on 2025-03-09 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employerprofile',
            name='company_name',
        ),
    ]
