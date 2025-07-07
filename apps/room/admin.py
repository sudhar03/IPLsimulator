from django.contrib import admin

from .models import Room, AuctionPlayer, TeamState

admin.site.register(Room)
admin.site.register(AuctionPlayer)
admin.site.register(TeamState)
