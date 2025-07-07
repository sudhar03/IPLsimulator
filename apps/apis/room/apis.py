from rest_framework.viewsets import ModelViewSet
from apps.room.models import Room
from apps.apis.room.serializers import RoomSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class RoomViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

