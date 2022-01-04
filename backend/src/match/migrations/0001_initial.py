# Generated by Django 4.0 on 2021-12-22 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
        ('core', '0004_rename_valid_until_notification_showuntil_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_mode', models.IntegerField(choices=[(1, 'None'), (2, 'Read Only'), (3, 'Read Write')], default=1)),
                ('title', models.CharField(max_length=22)),
                ('subtitle', models.CharField(max_length=22, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(choices=[(1, 'Created'), (2, 'Map Ban'), (3, 'Playing'), (4, 'Finished'), (5, 'Dummy')], default=1)),
                ('best_of', models.IntegerField(default=1)),
                ('score_blue', models.IntegerField(default=0)),
                ('score_orange', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.league')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.season')),
                ('sponsors', models.ManyToManyField(to='main.Sponsor')),
                ('team_blue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_blue', to='main.team')),
                ('team_orange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_orange', to='main.team')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('win_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_win_team', to='main.team')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_no', models.IntegerField()),
                ('win_type', models.IntegerField(choices=[(1, 'Kills'), (2, 'Defuser Planted'), (3, 'Defuser Disabled'), (4, 'Time')], default=1)),
                ('score_blue', models.IntegerField()),
                ('score_orange', models.IntegerField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('atk_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_atk_team', to='main.team')),
                ('bomb_spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bombspot')),
                ('def_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_def_team', to='main.team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.match')),
                ('of_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round_of_team', to='main.team')),
                ('win_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_win_team', to='main.team')),
            ],
        ),
        migrations.CreateModel(
            name='OperatorBans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.match')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.operator')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Ban'), (2, 'Pick'), (3, 'Decider'), (4, 'Default Ban')])),
                ('order', models.IntegerField(default=0)),
                ('play_order', models.IntegerField(default=0)),
                ('win_type', models.IntegerField(choices=[(1, 'None'), (2, 'Regular Win'), (3, 'Overtime Win'), (4, 'Draw')], default=1)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Playing'), (3, 'Finished')], default=1)),
                ('score_blue', models.IntegerField(default=0)),
                ('score_orange', models.IntegerField(default=0)),
                ('atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_atk_team', to='main.team')),
                ('choose_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choose_team', to='main.team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.match')),
                ('ot_atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ot_atk_team', to='main.team')),
                ('win_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='map_win_team', to='main.team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('matches', models.ManyToManyField(to='match.Match')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
