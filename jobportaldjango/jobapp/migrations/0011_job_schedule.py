# Generated by Django 4.2.3 on 2023-09-27 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0010_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='schedule',
            field=models.CharField(default=False, max_length=100),
        ),
    ]
