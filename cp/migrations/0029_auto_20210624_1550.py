# Generated by Django 3.2 on 2021-06-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0028_share_vehicle_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='Fare',
            new_name='fare',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('LGBTQ', 'LGBTQ')], default='male', max_length=20),
        ),
    ]
