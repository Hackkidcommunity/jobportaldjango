# Generated by Django 4.2.3 on 2023-09-26 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0006_jobposting'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_profile_complete',
            field=models.BooleanField(default=False),
        ),
    ]
