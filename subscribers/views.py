from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from bots_management.mixins import ModeratorRequiredMixin
from bots_management.services import get_bot_by_slug

from subscribers.models import Subscriber
from subscribers.services import (
    get_subscribers_of_bot,
)


class SubscribersListView(ModeratorRequiredMixin, generic.ListView):
    """
    List of all subscribers of a particular channel.
    """

    template_name = "subscribers/subscriber_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        return get_subscribers_of_bot(
            self.kwargs["slug"],
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bot"] = get_bot_by_slug(self.kwargs["slug"])
        return context


def ban_subscriber(request, slug, sub_id):
    return resolve_subscriber(request, slug, sub_id, 'ban')


def unban_subscriber(request, slug, sub_id):
    return resolve_subscriber(request, slug, sub_id, 'unban')


def resolve_subscriber(request, bot_slug, sub_id, status):
    if request.method == 'POST':
        order = get_object_or_404(Subscriber, pk=sub_id)
        order.is_active = status == 'unban'
        order.save()

        # todo: send acceptance to chat of subscriber
        return redirect('bots-management:subscribers:subscriber-list', slug=bot_slug)

    return Http404
