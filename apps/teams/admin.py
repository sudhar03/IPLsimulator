from django.contrib import admin
from django.apps import apps
from apps.teams.models import Team, GenericPlayer

# Register your models here.
my_app = apps.get_app_config("teams")

admin.site.register(Team)
admin.site.register(GenericPlayer)  