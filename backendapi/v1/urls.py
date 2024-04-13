from django.urls import path
from . import views

urlpatterns = [path("phone/<model_name>", views.get_phone_price)]
