# Generated by Django 3.2 on 2021-06-27 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0030_inter_loc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inter_loc',
            old_name='lat_arr',
            new_name='lat_long',
        ),
        migrations.RemoveField(
            model_name='inter_loc',
            name='long_arr',
        ),
    ]
