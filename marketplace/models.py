from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from core.validators import validate_image_size


class MarketplaceListing(models.Model):
    class Category(models.TextChoices):
        FOR_SALE = "for_sale", "Продажа"
        WANTED = "wanted", "Розыск"
        TRADE = "trade", "Обмен"
        SERVICES = "services", "Услуги"
        GROUP_RECRUITMENT = "group_recruitment", "Набор в группу"
        WARNING = "warning", "Предупреждение"
        OTHER = "other", "Прочее"

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        SOLD = "sold", "Продано"
        CLOSED = "closed", "Закрыто"

    title = models.CharField("заголовок", max_length=200)
    description = models.TextField("описание")
    category = models.CharField("категория", max_length=24, choices=Category.choices)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="автор",
        on_delete=models.CASCADE,
        related_name="marketplace_listings",
    )
    character_name = models.CharField("имя персонажа", max_length=100)
    price_or_trade = models.CharField("цена или условия обмена", max_length=200)
    meeting_location = models.CharField("место встречи", max_length=200)
    contact_information = models.CharField("способ связи", max_length=200)
    image = models.ImageField(
        "изображение",
        upload_to="marketplace/",
        blank=True,
        help_text="Необязательное изображение размером не более 3 МБ.",
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "gif", "webp"]),
            validate_image_size,
        ],
    )
    status = models.CharField(
        "состояние",
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата изменения", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "объявление"
        verbose_name_plural = "объявления"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"pk": self.pk})
