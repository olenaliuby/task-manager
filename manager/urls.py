"""
URL configuration for manager app.
"""
from django.urls import path

from manager.views import (
    index,
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("team/", WorkerListView.as_view(), name="worker-list"),
    path("team/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("team/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path(
        "team/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "team/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
]

app_name = "manager"
