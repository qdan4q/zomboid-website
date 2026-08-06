from django.db import OperationalError, ProgrammingError

from .models import SiteSettings


def site_context(request):
    try:
        site_settings = SiteSettings.load()
    except (OperationalError, ProgrammingError):
        site_settings = SiteSettings()
    return {
        "site_settings": site_settings,
        "visitor_number": f"{request.session.get('visitor_number', 1138):07d}",
    }

