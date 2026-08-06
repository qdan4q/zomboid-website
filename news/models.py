from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from core.validators import validate_image_size


class NewsArticle(models.Model):
    class NewsType(models.TextChoices):
        WORLD = "world", "Мировые новости"
        KNOX = "knox", "Новости зоны Нокс"
        MILITARY = "military", "Военная сводка"
        SCIENTIFIC = "scientific", "Научный отчёт"
        RADIO = "radio", "Радиосообщение"
        RUMOR = "rumor", "Слух выживших"

    class Visibility(models.TextChoices):
        SURVIVORS = "survivors", "Выжившие и администраторы"
        ADMIN_ONLY = "admin_only", "Только администраторы"

    title = models.CharField("заголовок", max_length=200)
    summary = models.CharField("краткое описание", max_length=400)
    content = models.TextField("полный текст")
    image = models.ImageField(
        "изображение",
        upload_to="news/%Y/%m/",
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"]
            ),
            validate_image_size,
        ],
    )
    news_type = models.CharField(
        "тип новости",
        max_length=20,
        choices=NewsType.choices,
        default=NewsType.KNOX,
    )
    visibility = models.CharField(
        "видимость",
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.SURVIVORS,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="автор",
        on_delete=models.PROTECT,
        related_name="news_articles",
    )
    in_game_date = models.DateField("игровая дата", blank=True, null=True)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата изменения", auto_now=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "новостная статья"
        verbose_name_plural = "новостные статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk})
