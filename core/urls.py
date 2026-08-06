from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("control-panel/", views.control_panel, name="control_panel"),
    path("control-panel/site-settings/", views.site_settings_edit, name="site_settings_edit"),
]

