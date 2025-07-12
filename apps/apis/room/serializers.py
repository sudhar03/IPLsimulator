from rest_framework import serializers
from apps.room.models import Room, AuctionPlayer, TeamState
from apps.teams.models import Team
from apps.apis.teams.serializers import TeamSerializer


class RoomSerializer(serializers.ModelSerializer):
    team = TeamSerializer(source="selected_team", read_only=True)
    class Meta:
        model = Room
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        if Room.objects.filter(user=validated_data["user"], year=validated_data["year"], completed=False).exists():
            raise serializers.ValidationError(f"You already have an active room for {validated_data["year"]}. Complete it first.")
        return super().create(validated_data)



class TeamStateSerializer(serializers.ModelSerializer):
    auction_players = serializers.SerializerMethodField()
    team = TeamSerializer(read_only=True)
    class Meta:
        model = TeamState
        fields = "__all__"

    def get_auction_players(self, obj):
        auction_players = AuctionPlayer.objects.filter(room=obj.room, final_team=obj)
        return AuctionPlayerSerializer(auction_players, many=True).data

class ReadTeamStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamState
        fields = "__all__"


class AuctionPlayerSerializer(serializers.ModelSerializer):
    current_bid_team = TeamSerializer(source="current_bid_team.team", read_only=True)
    final_team = TeamSerializer(source="final_team.team", read_only=True)
    class Meta:
        model = AuctionPlayer
        fields = "__all__"
