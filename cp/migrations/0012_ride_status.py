# Generated by Django 3.2 on 2021-06-12 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0011_alter_ride_requests_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_status', models.BooleanField(default=False)),
                ('ride_request_mod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ride_request_model', to='cp.ride_requests')),
            ],
        ),
    ]
