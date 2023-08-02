from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from manager.models import Worker, Task, TaskType, Commentary


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}
         ),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info",
         {"fields": ("first_name", "last_name", "position",)}
         ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ["name", "task_type", "priority"]
    list_display = ["name", "task_type", "priority"]


admin.site.register(TaskType)
admin.site.register(Commentary)
admin.site.unregister(Group)
