# Generated by Django 3.2 on 2021-06-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0022_ride_requests_spots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='women_only',
            field=models.BooleanField(choices=[('true', 'true'), ('false', 'false')], default=False),
        ),
    ]
