# Generated by Django 4.0 on 2021-12-22 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_bombspot_options_alter_map_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='valid_until',
            new_name='showUntil',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='name',
        ),
        migrations.AddField(
            model_name='notification',
            name='lastModified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
