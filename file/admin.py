from django.contrib import admin

from file.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['uploaded_by', 'file', 'created_at', 'updated_at']
    search_fields = ['uploaded_by']
