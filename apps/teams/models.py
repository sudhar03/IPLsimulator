from django.db import models



class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="logo", blank=True, null=True)
    year = models.IntegerField()
    
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"{self.name} - {self.year}"