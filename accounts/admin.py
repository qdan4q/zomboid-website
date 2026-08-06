from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "character_name", "occupation", "status")
    list_filter = ("status",)
    search_fields = ("user__username", "character_name", "occupation")
