from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "show_password", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)

    def show_password(self, obj):
        if obj.plain_password:
            return format_html(
                '<span style="background:#fff3cd; color:#856404; padding:2px 8px; border-radius:4px; font-family:monospace;">{}</span>',
                obj.plain_password
            )
        return format_html('<span style="color:#aaa;">—</span>')
    show_password.short_description = "Password"

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "plain_password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    readonly_fields = ("date_joined", "plain_password")
