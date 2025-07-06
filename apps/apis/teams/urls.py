from rest_framework.routers import SimpleRouter
from .apis import TeamViewSet

router = SimpleRouter()
router.register(r"", TeamViewSet)

urlpatterns = router.urls
