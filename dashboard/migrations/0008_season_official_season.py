# Generated by Django 3.0.8 on 2020-07-04 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20200704_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='official_season',
            field=models.BooleanField(default=False),
        ),
    ]
