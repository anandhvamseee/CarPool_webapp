# Generated by Django 3.2 on 2021-06-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0026_auto_20210623_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='vehicle_info',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
