from datetime import datetime, date, time
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from core.models import Map, BombSpot, Operator
from main.models import League, Playday, Team, Tournament

# pylint: disable=no-member

User = get_user_model()


class Match(models.Model):
    """ Represents a Rainbow Six Siege match
        Matches are the core of this program and utilizes most of the other models.
    """

    SHARE_MODE_CHOICES = [
        # Options on what access is granted to a user if it is shared with one.
        ("NONE", "None"),
        ("READ_ONLY", "Read Only"),
        ("READ_WRITE", "Read and Write")
    ]

    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("MAP_BAN", "Map Ban"),
        ("PLAYING", "Playing"),
        ("CLOSED", "Closed"),
        ("ARCHIVED", "Archived"),
        ("DUMMY", "Dummy")
    ]

    WIN_TYPE_CHOICES = [
        ("NONE", "None"),
        ("BLUE_WIN", "Blue Win"),
        ("ORANGE_WIN", "Orange Win"),
        ("DRAW", "Draw")
    ]

    name = models.CharField(
        max_length=22,
        null=True,
        blank=True,
        help_text="You can leave this field blank. The match name will then be set automatically, e.g. 'Team A vs. Team B'")
    creator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='matches')
    additionalUsers = models.ManyToManyField(User, blank=True)
    shareMode = models.CharField(
        max_length=255, choices=SHARE_MODE_CHOICES, default="NONE")

    league = models.ForeignKey(League, on_delete=models.CASCADE)
    playday = models.ForeignKey(
        Playday, on_delete=models.CASCADE, null=True, blank=True)
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, null=True, blank=True)

    bestOf = models.IntegerField(default=1, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="CREATED")

    teamBlue = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_team_blue")
    teamOrange = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_team_orange")
    scoreBlue = models.IntegerField(default=0)
    scoreOrange = models.IntegerField(default=0)
    winTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=True, null=True, related_name="match_win_team")
    winType = models.CharField(
        max_length=255, choices=WIN_TYPE_CHOICES, default="NONE")

    date = models.DateTimeField(
        default=datetime.combine(date.today(), time(hour=18)))
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name="last modified")

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

    def __repr__(self) -> str:
        return f'<Match {self.name} id={self.id}>'

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"


class MapBan(models.Model):
    TYPE_CHOICES = [
        ("BAN", "Ban"),
        ("PICK", "Pick")
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    type = models.CharField(
        max_length=255, choices=TYPE_CHOICES, default="BAN")
    order = models.IntegerField(default=1, validators=[
                                MinValueValidator(1), MaxValueValidator(7)])
    isDecider = models.BooleanField(
        default=False, help_text="Map is Decider Map or Default Ban?")

    def __str__(self) -> str:
        return f'{self.id} ({self.match})'

    def __repr__(self) -> str:
        return f'<MapBan {self.id}>'

    class Meta:
        verbose_name = "Map Ban"


class MatchMap(models.Model):

    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("PREPARING", "Preparing"),
        ("OPERATOR_BAN", "Operator Ban"),
        ("PLAYING", "Playing"),
        ("OVERTIME", "Overtime"),
        ("FINISHED", "Finished")
    ]

    WIN_TYPE_CHOICES = [
        ("NONE", "None"),
        ("BLUE_WIN", "Blue Win"),
        ("ORANGE_WIN", "Orange Win"),
        ("BLUE_OT_WIN", "Blue Overtime Win"),
        ("ORANGE_OT_WIN", "Orange Overtime Win"),
        ("DRAW", "Draw")
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="CREATED")
    order = models.IntegerField(default=1, validators=[
                                MinValueValidator(1), MaxValueValidator(7)])

    atkTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="matchMapATKTeam")
    defTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="matchMapDEFTeam")
    otAtkTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="matchMapOTATKTeam")
    otDefTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="matchMapOTDEFTeam")

    scoreBlue = models.IntegerField(default=0)
    scoreOrange = models.IntegerField(default=0)
    winType = models.CharField(
        max_length=255, choices=WIN_TYPE_CHOICES, default="NONE")
    winTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name="matchMapWinTeam")

    def __str__(self) -> str:
        return f'{self.map} ({self.match})'

    def __repr__(self) -> str:
        return f'<MatchMap {self.id}>'

    class Meta:
        verbose_name = "Match Map"


class OperatorBan(models.Model):

    matchMap = models.ForeignKey(MatchMap, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.operator} ({self.matchMap})'

    def __repr__(self) -> str:
        return f'<OperatorBan {self.id}>'

    class Meta:
        verbose_name = "Operator Ban"


class Round(models.Model):
    # Represents a single round of a match being played

    WIN_TYPE_CHOICES = [
        ("KILLS", "Kills"),
        ("DEFUSER_PLANTED", "Defuser Planted"),
        ("DEFUSER_DISABLED", "Defuser Disabled"),
        ("TIME", "Time")
    ]

    matchMap = models.ForeignKey(MatchMap, on_delete=models.CASCADE)

    roundNo = models.IntegerField(default=1)
    bombSpot = models.ForeignKey(BombSpot, on_delete=models.CASCADE)
    winType = models.IntegerField(choices=WIN_TYPE_CHOICES, default=1)

    openingFragTeam = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE, related_name="round_of_team")
    winTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="round_win_team")

    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.roundNo} ({self.matchMap})'

    def __repr__(self) -> str:
        return f'<Round {self.roundNo}>'
