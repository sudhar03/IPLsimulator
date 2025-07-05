from django.urls import path, include
from apps.apis.user import urls as user_urls

app_name = "api"

urlpatterns = [
    path("user/", include(user_urls)),]
