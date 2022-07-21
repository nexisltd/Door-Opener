from django.contrib import admin
from django.urls import path
from django.views import View
from . import views
from django.urls import re_path

urlpatterns = [
    # path('admin/', admin.site.urls),
    #  path('door/',views.Door.as_view()),
    path('',views.index, name='door'),
    # path('door/',views.door_open, name='open'),
    path('door/',views.Door.as_view(), name='open'),
    
    # path('live/', views.livecam_feed, name='livecam_feed'),

    re_path(r'ws/socket-server/', views.DoorConsumer.as_asgi(), name='socket')
]
