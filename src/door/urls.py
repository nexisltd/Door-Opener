from django.contrib import admin
from django.urls import include, path, re_path
from django.views import View

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ml.urls")),
    path("door/", views.Door.as_view()),
    path("", views.index, name="door"),
    # path('door/',views.door_open, name='open'),
    path("door/", views.Door.as_view(), name="open"),
    # path('live/', views.livecam_feed, name='livecam_feed'),
]
