# Generated by Django 3.2 on 2021-07-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0034_auto_20210630_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='intermediate_locations',
            field=models.CharField(blank=True, max_length=10000000000),
        ),
    ]
