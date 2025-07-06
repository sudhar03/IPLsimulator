from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    year = models.IntegerField(default=2008)
    purse = models.IntegerField(default=100_000_000)
    selected_team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


    def __str__(self):
        return self.name