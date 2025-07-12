from django_filters import FilterSet
from django_filters.rest_framework import NumberFilter, CharFilter, BooleanFilter
from apps.room.models import AuctionPlayer, TeamState


class AuctionPlayerFilter(FilterSet):
    year = NumberFilter(field_name="year", lookup_expr="exact")
    status = CharFilter(field_name="status", lookup_expr="icontains")
    class Meta:
        model = AuctionPlayer
        fields = ("year", "status")

class TeamStateFilter(FilterSet):
    is_user = BooleanFilter(field_name="is_user", lookup_expr="exact")
    year = NumberFilter(field_name="year", lookup_expr="exact")
    class Meta:
        model = TeamState
        fields = ("year", "is_user")