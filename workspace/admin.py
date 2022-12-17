from django.contrib import admin

from workspace.models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hashed_value', 'created_at']
    search_fields = ['name', 'hashed_value']