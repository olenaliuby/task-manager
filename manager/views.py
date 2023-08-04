from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from collections import defaultdict

from manager.forms import (
    WorkerPositionSearchForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskNameSearchForm,
    TaskCreateForm,
    TaskTypeNameSearchForm,
    TaskTypeCreateForm, CommentaryForm,
)
from manager.models import Task, Worker, TaskType, Commentary


@login_required
def index(request):
    """View function for the home page of the app."""
    task_list = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    ).filter(assignees=request.user)

    tasks_by_status = defaultdict(list)

    for task in task_list:
        tasks_by_status[task.status].append(task)

    context = {
        "task_list": task_list,
    }

    for status, task_list in tasks_by_status.items():
        context[f"status_{status}_tasks"] = task_list
        context[f"status_{status}_tasks_count"] = len(task_list)

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

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentaryForm()
        task = self.get_object()
        context["comments"] = task.commentaries.all()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentaryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.get_object()
            comment.user = request.user
            comment.save()
            return redirect(self.get_object().get_absolute_url())
        return super().get(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm

    def get_success_url(self):
        return reverse("manager:task-detail", args=[self.object.pk])


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


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        form = TaskTypeNameSearchForm(self.request.GET)

        if form.is_valid():
            return super().get_queryset().filter(
                name__icontains=form.cleaned_data["name"]
            )


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    queryset = TaskType.objects.prefetch_related("tasks")
    form_class = TaskTypeCreateForm
    template_name = "manager/task_type_form.html"

    def get_success_url(self):
        return reverse("manager:task-type-detail", args=[self.object.pk])


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    queryset = TaskType.objects.prefetch_related("tasks")
    template_name = "manager/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    context_object_name = "task_type"
    template_name = "manager/task_type_form.html"

    def get_success_url(self):
        return reverse("manager:task-type-detail", args=[self.object.pk])


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("manager:task-type-list")


class CommentaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Commentary
    form_class = CommentaryForm
    template_name = "manager/commentary_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        commentary = self.get_object()
        task_id = commentary.task_id
        return reverse("manager:task-detail", kwargs={"pk": task_id})


class CommentaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Commentary
    template_name = "manager/commentary_confirm_delete.html"

    def get_success_url(self):
        commentary = self.get_object()
        task_id = commentary.task_id
        return reverse("manager:task-detail", kwargs={"pk": task_id})
