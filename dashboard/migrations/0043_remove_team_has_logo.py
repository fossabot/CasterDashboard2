# Generated by Django 3.0.8 on 2020-08-31 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_auto_20200831_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='has_logo',
        ),
    ]
