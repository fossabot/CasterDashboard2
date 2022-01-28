# Generated by Django 3.0.8 on 2020-10-07 11:47

import dashboard.models.models
import dashboard.validators
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BombSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(choices=[('B', 'Basement'), ('1F', 'First Floor'), ('2F', 'Second Floor'), ('3F', 'Third Floor'), ('EXT', 'Exterior')], default='1F', max_length=3)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_restricted', models.BooleanField(default=True)),
                ('has_custom_overlay', models.BooleanField(default=False)),
                ('league_logo', models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.league_logo_path, validators=[dashboard.validators.validate_square_logo])),
                ('league_logo_small', models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.league_logo_path)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_mode', models.IntegerField(choices=[(1, 'None'), (2, 'Read Only'), (3, 'Read Write')], default=1)),
                ('title', models.CharField(max_length=22)),
                ('subtitle', models.CharField(max_length=22, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(choices=[(1, 'Created'), (2, 'Map Ban'), (3, 'Playing'), (4, 'Finished'), (5, 'Dummy')], default=1)),
                ('best_of', models.IntegerField(default=1)),
                ('score_blue', models.IntegerField(default=0)),
                ('score_orange', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.League')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('side', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=22, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('team_logo', models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.team_logo_path, validators=[dashboard.validators.validate_square_logo])),
                ('team_logo_small', models.ImageField(blank=True, null=True, upload_to=dashboard.models.models.team_logo_path)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('public', models.BooleanField(default=True)),
                ('sponsor_logo', models.ImageField(blank=True, null=True, upload_to='sponsors')),
                ('light_logo', models.ImageField(blank=True, null=True, upload_to='sponsors')),
                ('dark_logo', models.ImageField(blank=True, null=True, upload_to='sponsors')),
                ('league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.League')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('official_season', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.League')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_no', models.IntegerField()),
                ('win_type', models.IntegerField(choices=[(1, 'Kills'), (2, 'Defuser Planted'), (3, 'Defuser Disabled'), (4, 'Time')], default=1)),
                ('score_blue', models.IntegerField()),
                ('score_orange', models.IntegerField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('atk_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_atk_team', to='dashboard.Team')),
                ('bomb_spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.BombSpot')),
                ('def_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_def_team', to='dashboard.Team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('of_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round_of_team', to='dashboard.Team')),
                ('win_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_win_team', to='dashboard.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_token', models.CharField(blank=True, max_length=128, null=True)),
                ('confirmed', models.BooleanField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OperatorBans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Operator')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Ban'), (2, 'Pick'), (3, 'Decider'), (4, 'Default Ban')])),
                ('order', models.IntegerField(default=0)),
                ('play_order', models.IntegerField(default=0)),
                ('win_type', models.IntegerField(choices=[(1, 'None'), (2, 'Regular Win'), (3, 'Overtime Win'), (4, 'Draw')], default=1)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Playing'), (3, 'Finished')], default=1)),
                ('score_blue', models.IntegerField(default=0)),
                ('score_orange', models.IntegerField(default=0)),
                ('atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_atk_team', to='dashboard.Team')),
                ('choose_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choose_team', to='dashboard.Team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('ot_atk_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ot_atk_team', to='dashboard.Team')),
                ('win_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='map_win_team', to='dashboard.Team')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Season'),
        ),
        migrations.AddField(
            model_name='match',
            name='sponsors',
            field=models.ManyToManyField(blank=True, null=True, to='dashboard.Sponsor'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_blue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_blue', to='dashboard.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_orange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_orange', to='dashboard.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='win_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_win_team', to='dashboard.Team'),
        ),
        migrations.CreateModel(
            name='MapPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('maps', models.ManyToManyField(to='dashboard.Map')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(choices=[(1, 'User'), (2, 'Operator'), (3, 'Manager'), (4, 'Admin')], default=1)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.League')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bombspot',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map'),
        ),
    ]