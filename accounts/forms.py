from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from core.validators import validate_image_size

from .models import UserProfile


User = get_user_model()


class SurvivorProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["character_name", "avatar", "biography", "occupation"]
        widgets = {"biography": forms.Textarea(attrs={"rows": 6})}


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "character_name",
            "avatar",
            "biography",
            "occupation",
            "status",
        ]
        widgets = {"biography": forms.Textarea(attrs={"rows": 6})}


class StaffUserForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Администратор", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "is_active", "is_staff"]


class StaffUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта", required=False)
    is_active = forms.BooleanField(label="Учётная запись активна", initial=True, required=False)
    is_staff = forms.BooleanField(label="Администратор", required=False)
    character_name = forms.CharField(label="Имя персонажа", max_length=100, required=False)
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        validators=[validate_image_size],
    )
    biography = forms.CharField(
        label="Краткая биография",
        required=False,
        widget=forms.Textarea(attrs={"rows": 6}),
    )
    occupation = forms.CharField(label="Занятие", max_length=100, required=False)
    status = forms.ChoiceField(
        label="Текущее состояние",
        choices=UserProfile.Status.choices,
        initial=UserProfile.Status.UNKNOWN,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "is_active", "is_staff"]

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.character_name = self.cleaned_data["character_name"]
            profile.avatar = self.cleaned_data["avatar"]
            profile.biography = self.cleaned_data["biography"]
            profile.occupation = self.cleaned_data["occupation"]
            profile.status = self.cleaned_data["status"]
            profile.save()
        return user
