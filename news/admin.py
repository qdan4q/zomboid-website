from django.contrib import admin

from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "news_type", "visibility", "author", "created_at")
    list_filter = ("news_type", "visibility", "created_at")
    search_fields = ("title", "summary", "content")
    readonly_fields = ("created_at", "updated_at")
