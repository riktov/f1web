"""URLs for the browse app"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
