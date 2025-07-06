from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.apis.teams.serializers import TeamSerializer
from apps.teams.models import Team
from rest_framework.viewsets import ModelViewSet
from apps.teams.filters import TeamFilter
from django_filters.rest_framework import DjangoFilterBackend

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    filter_backends = (DjangoFilterBackend,)
    
    