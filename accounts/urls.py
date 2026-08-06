from django.urls import path

from . import views


urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("control-panel/users/", views.user_manage, name="user_manage"),
    path("control-panel/users/create/", views.user_create, name="user_create"),
    path(
        "control-panel/users/<int:user_id>/edit/",
        views.user_edit,
        name="user_edit",
    ),
    path(
        "control-panel/users/<int:user_id>/toggle-active/",
        views.user_toggle_active,
        name="user_toggle_active",
    ),
]
