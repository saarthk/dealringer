from rest_framework import routers
from . import views
from django.urls import path

router = routers.SimpleRouter()
router.register(r"phones", views.PhoneReadOnlyViewSet)
router.register(r"prices", views.PriceViewSet)

urlpatterns = [
    path("webhooks/", views.webhook_view),
]

urlpatterns += router.urls
