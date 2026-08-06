from django.contrib import admin

from .models import DirectMessage, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "character_name", "occupation", "status")
    list_filter = ("status",)
    search_fields = ("user__username", "character_name", "occupation")


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "created_at", "read_at")
    search_fields = ("sender__username", "recipient__username", "body")
    readonly_fields = ("created_at", "read_at")
