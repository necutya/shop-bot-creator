from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import (
    telegram_index, BotListView,
    BotDetailView, BotDeleteView, BotUpdateView,
    BotCreateView, root_view, info_view,
)

app_name = "bots-management"

urlpatterns = [
    path("", root_view, name="root"),

    path("/info", info_view, name="info"),

    path("bots/",
         BotListView.as_view(),
         name="bot-list"),
    path("bot/create/",
         BotCreateView.as_view(),
         name="bot-create"),
    path("bot/<str:slug>/delete",
         BotDeleteView.as_view(),
         name="bot-delete"),
    path("bot/<str:slug>/update/",
         BotUpdateView.as_view(),
         name="bot-update"),

    path("bot/<str:slug>/",
         include("subscribers.urls", namespace="subscribers")),

    path("bot/<str:slug>/",
         include("products.urls", namespace="products")),

    path("bot/<str:slug>/",
         include("orders.urls", namespace="orders")),

    path("telegram/api/<str:slug>/", telegram_index),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
