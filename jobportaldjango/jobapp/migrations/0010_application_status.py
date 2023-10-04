# Generated by Django 4.2.3 on 2023-09-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0009_alter_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('viewed', 'Viewed'), ('profile_visited', 'Profile Visited')], default='', max_length=20),
        ),
    ]