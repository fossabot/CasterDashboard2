# Generated by Django 3.0.8 on 2020-07-18 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_mappool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mappool',
            name='maps',
        ),
        migrations.AddField(
            model_name='mappool',
            name='maps',
            field=models.ManyToManyField(to='dashboard.Map'),
        ),
    ]