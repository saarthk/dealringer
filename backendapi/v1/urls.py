from rest_framework import routers
from . import views
from django.urls import path

router = routers.SimpleRouter()
router.register(r"phones", views.PhoneReadOnlyViewSet)
router.register(r"postings", views.PostingViewSet)

urlpatterns = [
    path("webhooks/", views.webhook_view),
    path("savedphones/", views.get_saved_phones, name="saved-phones"),
    path("search/", views.SearchPhones.as_view(), name="search-phones"),
]

urlpatterns += router.urls
