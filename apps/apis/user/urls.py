from rest_framework import routers
from .apis import AuthView, UserModelViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register(r"", UserModelViewSet)

urlpatterns = [
    path("login/", AuthView.as_view(), name="login"),
]

urlpatterns += router.urls

