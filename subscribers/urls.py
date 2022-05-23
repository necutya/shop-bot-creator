from django.urls import path

from subscribers.views import (
    SubscribersListView,
    ban_subscriber,
    unban_subscriber
)

app_name = "subscribers"

urlpatterns = [
    path("subscribers/",
         SubscribersListView.as_view(),
         name="subscriber-list"),
    path("subscribers/<int:sub_id>/ban", ban_subscriber,
         name="subscriber-ban"),
    path("subscribers/<int:sub_id>/unban", unban_subscriber,
         name="subscriber-unban"),
]
