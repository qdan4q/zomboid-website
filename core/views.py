from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import SiteSettingsForm
from .models import SiteSettings


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Требуются права администратора.")
        return view_func(request, *args, **kwargs)

    return wrapped


def home(request):
    from marketplace.models import MarketplaceListing
    from news.models import NewsArticle

    if "visitor_number" not in request.session:
        request.session["visitor_number"] = 1138 + get_user_model().objects.count()

    articles = NewsArticle.objects.filter(visibility=NewsArticle.Visibility.SURVIVORS)[:4]
    listings = MarketplaceListing.objects.filter(status=MarketplaceListing.Status.ACTIVE)[:5]
    return render(
        request,
        "core/home.html",
        {
            "latest_articles": articles,
            "latest_listings": listings,
            "survivor_count": get_user_model()
            .objects.filter(is_active=True, is_staff=False)
            .count(),
        },
    )


@staff_required
def control_panel(request):
    from marketplace.models import MarketplaceListing
    from news.models import NewsArticle

    return render(
        request,
        "core/control_panel.html",
        {
            "article_count": NewsArticle.objects.count(),
            "listing_count": MarketplaceListing.objects.count(),
            "user_count": get_user_model().objects.count(),
        },
    )


@staff_required
def site_settings_edit(request):
    settings = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, instance=settings)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Настройки сайта обновлены.")
        return redirect("control_panel")
    return render(request, "core/site_settings_form.html", {"form": form})
