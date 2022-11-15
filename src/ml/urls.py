from django.urls import path

from ml import views

urlpatterns = [
    path("test/", views.mlrun),
]
