from django.urls import path, include
from apps.apis.user import urls as user_urls
from apps.apis.teams import urls as teams_urls
from apps.apis.room import urls as room_urls

app_name = "api"

urlpatterns = [
    path("user/", include(user_urls)),
    path("teams/", include(teams_urls)),
    path("room/", include(room_urls)),]
