from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.teams.models import Team
from apps.teams.models import GenericPlayer

class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    year = models.IntegerField(default=2008)
    purse = models.BigIntegerField(default=1_00_000_000_000)
    selected_team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


    def __str__(self):
        return self.name

class AuctionPlayer(TimeStampedModel):
    NATIONALITY = Choices("INDIAN", "OVERSEAS",)
    STATUS = Choices("PENDING","ACTIVE", "UNSOLD", "SOLD")
    name = models.CharField(max_length=255)
    player_type = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255, choices=NATIONALITY)
    base_price = models.IntegerField()
    room = models.ForeignKey("room.Room", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS, default=STATUS.PENDING)
    current_bid = models.IntegerField(default=0)
    current_bid_team = models.ForeignKey("room.TeamState", on_delete=models.CASCADE, null=True, blank=True, related_name="current_bid_team")
    final_price = models.IntegerField(default=0)
    final_team = models.ForeignKey("room.TeamState", on_delete=models.CASCADE, null=True, blank=True, related_name="final_team")
    personality = models.CharField(max_length=255, null=True, blank=True)
    bowling_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    batting_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_percentage = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Auction Player"
        verbose_name_plural = "Auction Players"

    def __str__(self):
        return self.name

class TeamState(models.Model):
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="team_state")
    room = models.ForeignKey("room.Room", on_delete=models.CASCADE, related_name="team_state")
    players_count = models.IntegerField(default=0)
    purse = models.BigIntegerField(default=0)
    is_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Team State"
        verbose_name_plural = "Team States"

    def __str__(self):
        return f"{self.team.name} - {self.room.name}"
    


@receiver(post_save, sender=Room)
def create_room(sender, instance, created, **kwargs):
    if created:
        for player in GenericPlayer.objects.all():
            AuctionPlayer.objects.create(room=instance, name=player.name, player_type=player.player_type, nationality=player.nationality, base_price=player.base_price,
            personality=player.personality, bowling_average=player.bowling_average, batting_average=player.batting_average, overall_percentage=player.overall_percentage)

        teams = Team.objects.filter(year=instance.year)
        for team in teams.exclude(id=instance.selected_team.id):
            TeamState.objects.create(team=team, room=instance, is_user=False, purse=instance.purse)
        TeamState.objects.create(team=instance.selected_team, room=instance, is_user=True, purse=instance.purse)

        