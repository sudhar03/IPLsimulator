from rest_framework.routers import SimpleRouter
from .apis import RoomViewSet

router = SimpleRouter()
router.register(r"", RoomViewSet)

urlpatterns = router.urls
