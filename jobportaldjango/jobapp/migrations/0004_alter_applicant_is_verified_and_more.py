# Generated by Django 4.2.3 on 2023-09-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0003_applicant_is_blocked_company_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
    ]