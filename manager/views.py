from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    WorkerPositionSearchForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskNameSearchForm,
    TaskCreateForm,
)
from manager.models import Task, Worker


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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.prefetch_related("assigned_tasks")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        position = self.request.GET.get("position", "")

        context["search_form"] = WorkerPositionSearchForm(
            initial={"position": position}
        )

        return context

    def get_queryset(self):
        form = WorkerPositionSearchForm(self.request.GET)
        if form.is_valid():
            return super().get_queryset().filter(
                position__icontains=form.cleaned_data["position"]
            )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("assigned_tasks")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    )
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TaskNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            return super().get_queryset().filter(
                name__icontains=form.cleaned_data["name"]
            )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (
        Task.objects
        .prefetch_related("assignees")
        .select_related("task_type")
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


@login_required
def toggle_assign_to_task(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (
            Task.objects.get(id=pk) in worker.assigned_tasks.all()
    ):
        worker.assigned_tasks.remove(pk)
    else:
        worker.assigned_tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("manager:task-detail", args=[pk]))
