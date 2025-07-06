from django_filters import FilterSet
from django_filters.rest_framework import NumberFilter, CharFilter
from apps.teams.models import Team  

class TeamFilter(FilterSet):
    year = NumberFilter(field_name="year", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Team
        fields = ("year", "name")