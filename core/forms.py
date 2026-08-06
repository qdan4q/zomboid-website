from django import forms

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["website_name", "welcome_message", "emergency_message", "server_status"]
        widgets = {"welcome_message": forms.Textarea(attrs={"rows": 4})}

