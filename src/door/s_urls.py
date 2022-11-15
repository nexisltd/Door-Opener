from django.contrib import admin
from django.urls import path
from django.views import View
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r"ws/socket-server/", views.DoorConsumer.as_asgi(), name="socket"),
]
