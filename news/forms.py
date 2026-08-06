from django import forms

from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = [
            "title",
            "summary",
            "content",
            "image",
            "in_game_date",
            "news_type",
            "visibility",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12}),
            "in_game_date": forms.DateInput(attrs={"type": "date"}),
            "visibility": forms.RadioSelect,
        }
        help_texts = {
            "image": "Необязательное изображение в поддерживаемом формате размером не более 3 МБ.",
            "in_game_date": "Необязательная дата события в ролевой игре.",
            "visibility": "Закрытые отчёты никогда не передаются браузерам выживших.",
        }
