from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.views import staff_required

from .forms import (
    DirectMessageForm,
    StaffProfileForm,
    StaffUserCreationForm,
    StaffUserForm,
    SurvivorProfileForm,
)
from .models import DirectMessage, UserProfile


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
def public_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id, is_active=True)
    if profile_user == request.user:
        return redirect("profile")
    survivor_profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    listings = profile_user.marketplace_listings.filter(status="active")
    return render(request, "accounts/public_profile.html", {"profile_user": profile_user, "profile": survivor_profile, "listings": listings})


@login_required
def message_inbox(request):
    messages_qs = DirectMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related("sender", "recipient")
    conversations = {}
    for direct_message in messages_qs.order_by("-created_at", "-pk"):
        other_user = direct_message.recipient if direct_message.sender_id == request.user.id else direct_message.sender
        if other_user.pk not in conversations:
            conversations[other_user.pk] = {"user": other_user, "last_message": direct_message, "unread_count": 0}
        if direct_message.recipient_id == request.user.id and direct_message.read_at is None:
            conversations[other_user.pk]["unread_count"] += 1
    return render(request, "accounts/message_inbox.html", {"conversations": conversations.values()})


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id, is_active=True)
    if other_user == request.user:
        messages.error(request, "Нельзя отправить сообщение самому себе.")
        return redirect("message_inbox")
    form = DirectMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        direct_message = form.save(commit=False)
        direct_message.sender = request.user
        direct_message.recipient = other_user
        direct_message.save()
        return redirect("conversation", user_id=other_user.pk)
    thread = DirectMessage.objects.filter(Q(sender=request.user, recipient=other_user) | Q(sender=other_user, recipient=request.user)).select_related("sender", "recipient")
    DirectMessage.objects.filter(sender=other_user, recipient=request.user, read_at__isnull=True).update(read_at=timezone.now())
    return render(request, "accounts/conversation.html", {"other_user": other_user, "thread": thread, "form": form})


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
