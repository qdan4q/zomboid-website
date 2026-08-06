from django.contrib import admin

from .models import MarketplaceListing


@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "description", "character_name", "author__username")
    readonly_fields = ("created_at", "updated_at")
