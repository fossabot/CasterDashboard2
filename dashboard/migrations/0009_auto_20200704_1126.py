# Generated by Django 3.0.8 on 2020-07-04 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_season_official_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='league',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.League'),
        ),
    ]
