# Generated for the initial Knox Community Network schema.

import core.validators
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsArticle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("summary", models.CharField(max_length=400)),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="news/%Y/%m/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"]
                            ),
                            core.validators.validate_image_size,
                        ],
                    ),
                ),
                (
                    "news_type",
                    models.CharField(
                        choices=[
                            ("world", "World News"),
                            ("knox", "Knox Zone News"),
                            ("military", "Military Report"),
                            ("scientific", "Scientific Report"),
                            ("radio", "Radio Message"),
                            ("rumor", "Survivor Rumor"),
                        ],
                        default="knox",
                        max_length=20,
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[
                            ("survivors", "Survivors and Administrators"),
                            ("admin_only", "Administrators Only"),
                        ],
                        default="survivors",
                        max_length=20,
                    ),
                ),
                ("in_game_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="news_articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-pk"]},
        ),
    ]
