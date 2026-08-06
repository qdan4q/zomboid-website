from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import MarketplaceListingForm, StaffMarketplaceListingForm
from .models import MarketplaceListing


def listing_list(request):
    listings = MarketplaceListing.objects.filter(
        status=MarketplaceListing.Status.ACTIVE
    ).select_related("author")
    return render(request, "marketplace/listing_list.html", {"listings": listings})


def listing_detail(request, pk):
    listings = MarketplaceListing.objects.select_related("author")
    if not (request.user.is_authenticated and request.user.is_staff):
        if request.user.is_authenticated:
            listings = listings.filter(
                Q(status=MarketplaceListing.Status.ACTIVE) | Q(author=request.user)
            )
        else:
            listings = listings.filter(status=MarketplaceListing.Status.ACTIVE)
    listing = get_object_or_404(listings, pk=pk)
    return render(request, "marketplace/listing_detail.html", {"listing": listing})


@login_required
def listing_create(request):
    if request.method == "POST":
        form = MarketplaceListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            messages.success(request, "Объявление опубликовано.")
            return redirect(listing)
    else:
        form = MarketplaceListingForm()

    return render(
        request,
        "marketplace/listing_form.html",
        {"form": form, "page_title": "Создать объявление"},
    )


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk)
    if listing.author != request.user and not request.user.is_staff:
        raise PermissionDenied

    form_class = (
        StaffMarketplaceListingForm
        if request.user.is_staff
        else MarketplaceListingForm
    )
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listing = form.save()
            messages.success(request, "Объявление обновлено.")
            if listing.status == MarketplaceListing.Status.ACTIVE:
                return redirect(listing)
            if request.user.is_staff:
                return redirect("listing_manage")
            return redirect("listing_list")
    else:
        form = form_class(instance=listing)

    return render(
        request,
        "marketplace/listing_form.html",
        {"form": form, "listing": listing, "page_title": "Редактировать объявление"},
    )


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk)
    if listing.author != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Объявление удалено.")
        if request.user.is_staff:
            return redirect("listing_manage")
        return redirect("listing_list")

    return render(
        request,
        "marketplace/listing_confirm_delete.html",
        {"listing": listing},
    )


@login_required
@require_POST
def listing_mark_sold(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk)
    if listing.author != request.user:
        raise PermissionDenied

    listing.status = MarketplaceListing.Status.SOLD
    listing.save(update_fields=["status", "updated_at"])
    messages.success(request, "Объявление отмечено как проданное.")
    return redirect("listing_list")


@login_required
def listing_manage(request):
    if not request.user.is_staff:
        raise PermissionDenied

    listings = MarketplaceListing.objects.select_related("author").all()
    return render(
        request,
        "marketplace/listing_manage.html",
        {"listings": listings},
    )
