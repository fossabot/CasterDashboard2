# Generated by Django 3.0.8 on 2020-07-01 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bombspot',
            name='floor',
            field=models.CharField(default='1F', max_length=2),
        ),
        migrations.AlterField(
            model_name='bombspot',
            name='bomb_spot',
            field=models.CharField(default='', max_length=255),
        ),
    ]
