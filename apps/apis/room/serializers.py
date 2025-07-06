from rest_framework import serializers
from apps.room.models import Room
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
