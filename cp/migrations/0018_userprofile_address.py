# Generated by Django 3.2 on 2021-06-18 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0017_share_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, default='press the edit button to add address'),
        ),
    ]
