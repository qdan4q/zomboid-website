from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.views import staff_required

from .forms import (
    StaffProfileForm,
    StaffUserCreationForm,
    StaffUserForm,
    SurvivorProfileForm,
)
from .models import UserProfile


User = get_user_model()


@login_required
def profile(request):
    survivor_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    listings = request.user.marketplace_listings.all()
    return render(
        request,
        "accounts/profile.html",
        {"profile": survivor_profile, "listings": listings},
    )


@login_required
def profile_edit(request):
    survivor_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = SurvivorProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=survivor_profile,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль выжившего обновлён.")
        return redirect("profile")
    return render(request, "accounts/profile_form.html", {"form": form})


@staff_required
def user_manage(request):
    users = list(User.objects.order_by("username"))
    # The signal covers new users; this also repairs accounts created before
    # the profile table existed.
    for managed_user in users:
        UserProfile.objects.get_or_create(user=managed_user)
    return render(request, "accounts/user_manage.html", {"users": users})


@staff_required
def user_create(request):
    form = StaffUserCreationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, f"Учётная запись {user.username} создана.")
        return redirect("user_manage")
    return render(
        request,
        "accounts/user_form.html",
        {"user_form": form, "creating": True},
    )


@staff_required
@transaction.atomic
def user_edit(request, user_id):
    managed_user = get_object_or_404(User, pk=user_id)
    managed_profile, _ = UserProfile.objects.get_or_create(user=managed_user)
    user_form = StaffUserForm(request.POST or None, instance=managed_user)
    profile_form = StaffProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=managed_profile,
    )
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, f"Учётная запись {managed_user.username} обновлена.")
        return redirect("user_manage")
    return render(
        request,
        "accounts/user_form.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "managed_user": managed_user,
            "creating": False,
        },
    )


@staff_required
@require_POST
def user_toggle_active(request, user_id):
    managed_user = get_object_or_404(User, pk=user_id)
    if managed_user == request.user:
        messages.error(request, "Здесь нельзя отключить собственную учётную запись.")
        return redirect("user_manage")
    managed_user.is_active = not managed_user.is_active
    managed_user.save(update_fields=["is_active"])
    state = "включена" if managed_user.is_active else "отключена"
    messages.success(request, f"Учётная запись {managed_user.username} {state}.")
    return redirect("user_manage")
