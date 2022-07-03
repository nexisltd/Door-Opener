from django.contrib import admin
from django.urls import path
from django.views import View
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    #  path('door/',views.Door.as_view()),
    path('door/',views.index, name='door'),
    path('live/', views.livecam_feed, name='livecam_feed'),
]
