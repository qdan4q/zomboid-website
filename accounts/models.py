from django.conf import settings
from django.db import models

from core.validators import validate_image_size


class UserProfile(models.Model):
    class Status(models.TextChoices):
        ALIVE = "alive", "Жив"
        MISSING = "missing", "Пропал без вести"
        INJURED = "injured", "Ранен"
        UNKNOWN = "unknown", "Неизвестно"
        DEAD = "dead", "Мёртв"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    character_name = models.CharField("имя персонажа", max_length=100, blank=True)
    avatar = models.ImageField(
        "аватар",
        upload_to="avatars/",
        blank=True,
        validators=[validate_image_size],
    )
    biography = models.TextField("краткая биография", blank=True)
    occupation = models.CharField("занятие", max_length=100, blank=True)
    status = models.CharField(
        "текущее состояние",
        max_length=10,
        choices=Status.choices,
        default=Status.UNKNOWN,
    )

    class Meta:
        verbose_name = "профиль выжившего"
        verbose_name_plural = "профили выживших"

    def __str__(self):
        return self.character_name or self.user.username


class DirectMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="отправитель", on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="получатель", on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField("сообщение", max_length=4000)
    created_at = models.DateTimeField("отправлено", auto_now_add=True)
    read_at = models.DateTimeField("прочитано", null=True, blank=True)

    class Meta:
        ordering = ["created_at", "pk"]
        verbose_name = "личное сообщение"
        verbose_name_plural = "личные сообщения"
        indexes = [models.Index(fields=["recipient", "read_at"]), models.Index(fields=["sender", "recipient", "created_at"])]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.body[:40]}"
