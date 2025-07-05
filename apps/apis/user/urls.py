from rest_framework import routers
from .apis import AuthView
from django.urls import path


urlpatterns = [
    path("login/", AuthView.as_view(), name="login"),
]
