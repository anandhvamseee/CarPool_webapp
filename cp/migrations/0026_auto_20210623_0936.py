# Generated by Django 3.2 on 2021-06-23 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0025_userprofile_delete_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='message',
        ),
        migrations.AddField(
            model_name='share',
            name='Fare',
            field=models.IntegerField(default=0),
        ),
    ]
