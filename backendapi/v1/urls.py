from rest_framework import routers
from . import views
from django.urls import path

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"phones", views.PhoneReadOnlyViewSet)

urlpatterns = [
    path("webhooks/", views.webhook_view),
]

urlpatterns += router.urls
