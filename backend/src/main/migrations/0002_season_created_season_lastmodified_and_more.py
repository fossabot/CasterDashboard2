# Generated by Django 4.0 on 2021-12-22 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='lastModified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='league',
            name='customDesign',
            field=models.BooleanField(default=False, verbose_name='custom design'),
        ),
        migrations.AlterField(
            model_name='league',
            name='lastModified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='league',
            name='logoSmall',
            field=models.ImageField(blank=True, null=True, upload_to='leagues', verbose_name='small logo'),
        ),
        migrations.AlterField(
            model_name='season',
            name='seasonNo',
            field=models.IntegerField(default=1, verbose_name='season number'),
        ),
    ]
