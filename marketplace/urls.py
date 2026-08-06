from django.urls import path

from . import views


urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("create/", views.listing_create, name="listing_create"),
    path("manage/", views.listing_manage, name="listing_manage"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("<int:pk>/edit/", views.listing_edit, name="listing_edit"),
    path("<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("<int:pk>/sold/", views.listing_mark_sold, name="listing_mark_sold"),
]
