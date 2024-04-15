from rest_framework import routers
from .views import PhoneReadOnlyViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"phones", PhoneReadOnlyViewSet)

urlpatterns = router.urls
