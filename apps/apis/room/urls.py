from rest_framework.routers import SimpleRouter
from .apis import RoomViewSet, AuctionPlayerViewSet, TeamStateViewSet, BidAPIView
from django.urls import path

router = SimpleRouter()
router.register(r"", RoomViewSet)
router.register(r"auction/player", AuctionPlayerViewSet)
router.register(r"team/state", TeamStateViewSet)

urlpatterns = [
    path("user/auction/", BidAPIView.as_view(), name="user_auction"),
]
urlpatterns += router.urls