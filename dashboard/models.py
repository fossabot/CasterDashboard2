"""
Main database model definitions
"""

import os
import logging
import secrets
from datetime import datetime

from PIL import Image
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import *
from django.dispatch import receiver

import caster_dashboard_2.settings.base as django_settings
from dashboard.validators import *
from caster_dashboard_2.helpers.image_handler import *

logger = logging.getLogger(__name__)


class OverwriteStorage(FileSystemStorage):
    """Replaces existing files on model update"""

    def get_available_name(self, name, max_length=None):
        # Found at http://djangosnippets.org/snippets/976/

        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=128, blank=True, null=True)
    confirmed = models.BooleanField(default=0)

    def __str__(self):
        return "Profile: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User: %(user)s] Creating Profile via receiver" % {'user': instance})
        registration_token = secrets.token_hex(64)
        Profile.objects.create(user=instance, registration_token=registration_token)


class Version(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    release_date = models.DateField(auto_now_add=True, blank=True)
    changelog = models.TextField()

    def __str__(self):
        return self.name


class Map(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MapPool(models.Model):
    name = models.CharField(max_length=255)
    maps = models.ManyToManyField(Map)

    def __str__(self):
        return self.name


class BombSpot(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    floor = models.CharField(max_length=7, default='1F')
    bomb_spot = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.bomb_spot


class Operator(models.Model):
    name = models.CharField(max_length=255)
    side = models.CharField(max_length=3)

    def __str__(self):
        return self.name


def league_logo_path(instance, filename):
    return "leagues/{0}.png".format(instance.id)


class League(models.Model):
    name = models.CharField(max_length=255)
    is_restricted = models.BooleanField(default=True)
    has_custom_overlay = models.BooleanField(default=False)

    league_logo = models.ImageField(upload_to=league_logo_path, validators=[validate_square_logo], blank=True,
                                    null=True)
    league_logo_small = models.ImageField(upload_to=league_logo_path, blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=League)
def league_pre_save(sender, instance, **kwargs):
    instance.full_clean()


@receiver(post_save, sender=League)
def league_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.league_logo:
        if not instance.league_logo.name.__contains__(str(instance.id) + "_500.webp"):
            convert_league_logo(instance.id, instance.league_logo.path)
            os.remove(instance.league_logo.path)

            instance.league_logo = "leagues/%(id)s_500.webp" % ({'id': instance.id})
            instance.league_logo_small = "leagues/%(id)s_50.webp" % ({'id': instance.id})
            instance.save()

    else:
        no_logo_path = os.path.join(django_settings.MEDIA_ROOT, "teams", "_nologo.png")
        convert_league_logo(instance.id, no_logo_path)

        instance.league_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
        instance.league_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
        instance.save()


@receiver(pre_delete, sender=League)
def league_pre_delete(sender, instance, **kwargs):
    # Auto delete image
    if instance.league_logo:
        if os.path.isfile(instance.league_logo.path):
            os.remove(instance.league_logo.path)


class LeagueGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    rank = models.CharField(max_length=255, default="user")

    def __str__(self):
        return "LeagueGroup: " + str(self.user) + " / " + str(self.league) + " / " + self.rank


class Season(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    official_season = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


def team_logo_path(instance, filename):
    if instance.id:
        return "teams/{0}.png".format(instance.id)
    else:
        return "teams/{0}".format(filename)


class Team(models.Model):
    name = models.CharField(max_length=22, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    team_logo = models.ImageField(upload_to=team_logo_path, validators=[validate_square_logo], blank=True, null=True)
    team_logo_small = models.ImageField(upload_to=team_logo_path, blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Team)
def team_pre_save(sender, instance, **kwargs):
    instance.full_clean()


@receiver(post_save, sender=Team)
def team_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.team_logo:
        if not instance.team_logo.name.__contains__(str(instance.id) + "_500.webp"):
            convert_team_logo(instance.id, instance.team_logo.path)
            os.remove(instance.team_logo.path)

            instance.team_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
            instance.team_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
            instance.save()

    else:
        no_logo_path = os.path.join(django_settings.MEDIA_ROOT, "teams", "_nologo.png")
        convert_team_logo(instance.id, no_logo_path)

        instance.team_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
        instance.team_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
        instance.save()


@receiver(pre_delete, sender=Team)
def team_pre_delete(sender, instance, **kwargs):
    # Auto delete images
    team_logo = instance.team_logo.path
    team_logo_small = instance.team_logo_small.path

    os.remove(team_logo)
    os.remove(team_logo_small)


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    sponsor_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    light_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    dark_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Sponsor)
def sponsor_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.sponsor_logo:
        instance.has_logo = True
        if not instance.sponsor_logo.name.__contains__(str(instance.id)):
            old_path = os.path.join(django_settings.MEDIA_ROOT, instance.sponsor_logo.name)
            new_path = os.path.join(django_settings.MEDIA_ROOT, "sponsors", str(instance.id) + ".png")

            # Remove old file if it exists
            if os.path.isfile(new_path):
                logger.info("Removing old sponsor logo file: " + new_path)
                try:
                    os.remove(new_path)
                except OSError as e:
                    logger.error("Error removing old sponsor logo file: " + str(e))

            # Move new file in place
            try:
                os.rename(old_path, new_path)
            except OSError as e:
                logger.error('Error moving sponsor logo file: ' + str(e))

            instance.sponsor_logo = "sponsors/{0}.png".format(str(instance.id))
            instance.save()


@receiver(pre_delete, sender=Sponsor)
def sponsor_pre_delete(sender, instance, **kwargs):
    if instance.sponsor_logo:
        logo = instance.sponsor_logo.path
        # Auto delete image
        if logo:
            if os.path.exists(instance.sponsor_logo.path):
                os.remove(instance.sponsor_logo.path)


class MatchState(models.Model):
    state = models.CharField(max_length=255, default="created")

    def __str__(self):
        return self.state


class Match(models.Model):
    user = models.ManyToManyField(User)
    share_mode = models.CharField(max_length=5, blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    title = models.CharField(max_length=22)
    sponsors = models.ManyToManyField(Sponsor, blank=True, null=True)
    subtitle = models.CharField(max_length=22, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.ForeignKey(MatchState, default=1, on_delete=models.SET_DEFAULT)
    best_of = models.IntegerField(default=1)
    team_blue = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_blue")
    team_orange = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_orange")
    score_blue = models.IntegerField(default=0)
    score_orange = models.IntegerField(default=0)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="match_win_team")

    def serialize(self):
        if self.win_team is not None:
            win_team = self.win_team.name
        else:
            win_team = ''

        return {
            'id': self.id,
            'season': self.season.name,
            'league': self.league.name,
            'title': self.title,
            'sponsors': None,
            'subtitle': self.subtitle,
            'state': self.state.state,
            'best_of': self.best_of,
            'team_blue': self.team_blue.name,
            'team_orange': self.team_orange.name,
            'score_blue': self.score_blue,
            'score_orange': self.score_orange,
            'win_team': win_team,
        }

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=Match)
def match_post_save(sender, instance, **kwargs):
    # Send message to Websocket Consumer
    channel_layer = get_channel_layer()
    match_data = instance.serialize()

    map_picks = MapBan.objects.filter(match=instance).all()
    maps = []
    for m in map_picks:
        if m.type == "pick" or m.type == "decider":
            maps.append({'map': m.map.id, 'type': m.type, 'team': m.team.id})

    data = {'match': match_data, 'maps': maps}

    for user in instance.user.all():
        async_to_sync(channel_layer.group_send)(
            str(user) + "_match_data",
            {
                "type": "send_message",
                "message": data,
            }
        )


class MapBan(models.Model):
    TYPE_CHOICES = [
        (1, "Ban"),
        (2, "Pick"),
        (3, "Decider"),
        (4, "Default Ban")
    ]

    STATUS_CHOICES = [
        (1, "Created"),
        (2, "Playing"),
        (3, "Finished"),
        (4, "Unknown")
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    order = models.IntegerField(default=1)
    play_order = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return str(self.id) + "- Match: " + str(self.match)


@receiver(post_save, sender=MapBan)
def map_ban_post_save(sender, instance, **kwargs):
    # Set Match state
    match_state = MatchState.objects.get(id=2)
    instance.match.state = match_state
    instance.match.save()


class MapWins(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "MapWins:" + str(self.map.name) + " - Match: " + str(self.match)


class MapSettings(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="map_settings_atk_team")
    ot_atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="map_settings_ot_atk_team")
    final_score_blue = models.IntegerField(default=0)
    final_score_orange = models.IntegerField(default=0)

    def __str__(self):
        return "MapSettings: " + str(self.map.name) + " - Match: " + str(self.match.id)


class OperatorBans(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.operator.name + " - Match: " + str(self.match)


@receiver(post_save, sender=OperatorBans)
def operator_bans_post_save(sender, instance, **kwargs):
    # Update Match state
    map_play_order = MapPlayOrder.objects.get(match=instance.match, map=instance.map)
    new_match_state = MatchState.objects.get(id=(2 + map_play_order.order))
    match = instance.match
    match.state = new_match_state
    match.save()


class WinType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Round(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    round_no = models.IntegerField()
    bombspot = models.ForeignKey(BombSpot, on_delete=models.CASCADE)
    atk_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_atk_team")
    def_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_def_team")
    of_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name="round_of_team")
    win_type = models.ForeignKey(WinType, on_delete=models.CASCADE)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_win_team")
    score_blue = models.IntegerField()
    score_orange = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.round_no) + " - Match: " + str(self.match)
