from rest_framework.viewsets import ModelViewSet
from apps.apis.room.serializers import RoomSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.room.models import AuctionPlayer, TeamState, Room
from apps.room.filters import AuctionPlayerFilter, TeamStateFilter
from apps.apis.room.serializers import AuctionPlayerSerializer, TeamStateSerializer
from apps.room.tasks import next_bid_flow

class RoomViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BidAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        current_player = self.request.data.get("current_player")
        room = self.request.data.get("room")
        team_state = TeamState.objects.get(room=room, is_user=True)
        auction_player = AuctionPlayer.objects.get(id=current_player)
        if auction_player.current_bid_team == team_state:
            return Response({"detail": "You have already bid for this player"}, status=status.HTTP_400_BAD_REQUEST)

        auction_player.current_bid_team = team_state
        auction_player.current_bid = next_bid_flow(auction_player)
        auction_player.save()
        return Response({"detail": "Bid placed successfully"}, status=status.HTTP_200_OK)

class AuctionPlayerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AuctionPlayer.objects.all()
    http_method_names = ("get",)
    serializer_class = AuctionPlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionPlayerFilter

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        return self.queryset.filter(room=room_id)

class TeamStateViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TeamState.objects.all()
    http_method_names = ("get",)
    serializer_class = TeamStateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamStateFilter

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        return self.queryset.filter(room=room_id)