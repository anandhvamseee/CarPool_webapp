# Generated by Django 3.2 on 2021-05-20 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0004_auto_20210520_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('not specified', 'not specified')], default='male', max_length=20),
        ),
    ]
