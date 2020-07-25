# Generated by Django 3.0.8 on 2020-07-25 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20200718_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='atk_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_atk_team', to='dashboard.Team'),
        ),
        migrations.AlterField(
            model_name='round',
            name='def_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_def_team', to='dashboard.Team'),
        ),
        migrations.CreateModel(
            name='MapSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_score_blue', models.IntegerField(default=0)),
                ('final_score_orange', models.IntegerField(default=0)),
                ('atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_settings_atk_team', to='dashboard.Team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('ot_atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_settings_ot_atk_team', to='dashboard.Team')),
            ],
        ),
    ]
