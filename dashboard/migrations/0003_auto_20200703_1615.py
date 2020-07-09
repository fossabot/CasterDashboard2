# Generated by Django 3.0.8 on 2020-07-03 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20200701_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_mode', models.CharField(max_length=5, null=True)),
                ('title', models.CharField(max_length=22)),
                ('subtitle', models.CharField(max_length=22, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
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
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=22)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_logo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.League')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_no', models.IntegerField()),
                ('win_type', models.CharField(max_length=255)),
                ('score_blue', models.IntegerField()),
                ('score_orange', models.IntegerField()),
                ('atk_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atk_team', to='dashboard.Team')),
                ('bombspot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.BombSpot')),
                ('def_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='def_team', to='dashboard.Team')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('win_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_win_team', to='dashboard.Team')),
            ],
        ),
        migrations.CreateModel(
            name='OperatorBans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Operator')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Team')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Season'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_blue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_blue', to='dashboard.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_orange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_orange', to='dashboard.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='win_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_win_team', to='dashboard.Team'),
        ),
        migrations.CreateModel(
            name='MapWins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('win_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MapBan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Map')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Team')),
            ],
        ),
    ]
