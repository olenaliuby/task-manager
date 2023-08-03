"""
URL configuration for manager app.
"""
from django.urls import path

from manager.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "manager"
