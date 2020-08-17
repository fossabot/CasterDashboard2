# Generated by Django 3.0.8 on 2020-07-31 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_mapplayorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.League'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
