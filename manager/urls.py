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
    WorkerDeleteView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    toggle_assign_to_task,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeDetailView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    CommentaryUpdateView,
    CommentaryDeleteView
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
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task-types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail"
    ),
    path(
        "task-types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "commentaries/<int:pk>/update/",
        CommentaryUpdateView.as_view(),
        name="commentary-update"
    ),
    path(
        "commentaries/<int:pk>/delete/",
        CommentaryDeleteView.as_view(),
        name="commentary-delete"
    ),
]

app_name = "manager"
