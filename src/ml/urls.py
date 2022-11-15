from django.contrib import admin
from django.urls import path
from django.views import View
from . import views
from django.urls import re_path

urlpatterns = [
    path("mldata/", views.ML.as_view(), name="ml"),
]
