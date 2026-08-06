from django.db import models


class SiteSettings(models.Model):
    website_name = models.CharField(
        "название сайта", max_length=100, default="Общественная сеть Нокса"
    )
    welcome_message = models.TextField(
        "приветствие",
        default="Добровольный узел связи для выживших внутри закрытой зоны Нокс.",
    )
    emergency_message = models.CharField(
        "экстренное сообщение",
        max_length=255,
        default="Берегите воду. Держите радиоприёмники на частоте 88,7 МГц.",
    )
    server_status = models.CharField(
        "состояние сервера", max_length=80, default="В СЕТИ — сигнал нестабилен"
    )
    last_updated = models.DateTimeField("последнее обновление", auto_now=True)

    class Meta:
        verbose_name = "настройки сайта"
        verbose_name_plural = "настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return self.website_name
