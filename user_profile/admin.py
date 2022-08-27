from django.contrib import admin

from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_id', 'bio', 'created_at']
    search_fields = ['user_id', 'user_email']
