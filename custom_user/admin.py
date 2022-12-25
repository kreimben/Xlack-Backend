from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from custom_user.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'display_name', 'title', 'phone_number']
    fieldsets = (
        ('Xlack Application Related', {'fields': ('display_name', 'title', 'phone_number', 'profile_image')}),
        ('Django Default', {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
