from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("accounts", "0002_alter_userprofile_options_alter_userprofile_avatar_and_more")]
    operations = [migrations.CreateModel(
        name="DirectMessage",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("body", models.TextField(max_length=4000, verbose_name="сообщение")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="отправлено")),
            ("read_at", models.DateTimeField(blank=True, null=True, verbose_name="прочитано")),
            ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="received_messages", to=settings.AUTH_USER_MODEL, verbose_name="получатель")),
            ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_messages", to=settings.AUTH_USER_MODEL, verbose_name="отправитель")),
        ],
        options={"verbose_name": "личное сообщение", "verbose_name_plural": "личные сообщения", "ordering": ["created_at", "pk"], "indexes": [models.Index(fields=["recipient", "read_at"], name="accounts_di_recipie_7d3c9e_idx"), models.Index(fields=["sender", "recipient", "created_at"], name="accounts_di_sender__a86a1b_idx")]},
    )]
