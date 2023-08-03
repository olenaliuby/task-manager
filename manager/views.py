from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from manager.models import Task


@login_required
def index(request):
    """View function for the home page of the app."""
    task_list = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    ).filter(assignees=request.user)

    to_do_tasks = []
    in_progress_tasks = []
    done_tasks = []
    archived_tasks = []

    for task in task_list:
        if task.status == Task.StatusChoices.TO_DO:
            to_do_tasks.append(task)
        elif task.status == Task.StatusChoices.IN_PROGRESS:
            in_progress_tasks.append(task)
        elif task.status == Task.StatusChoices.DONE:
            done_tasks.append(task)
        elif task.status == Task.StatusChoices.ARCHIVED:
            archived_tasks.append(task)

    context = {
        "task_list": task_list,
        "to_do_tasks": to_do_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
        "archived_tasks": archived_tasks,
        "to_do_tasks_count": len(to_do_tasks),
        "in_progress_tasks_count": len(in_progress_tasks),
        "done_tasks_count": len(done_tasks),
        "archived_tasks_count": len(archived_tasks),
    }

    return render(request, "manager/index.html", context=context)
