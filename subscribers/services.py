from typing import Union

from django.db.models import Q, QuerySet

from bots_management.models import Bot
from keyboards.inline_callbacks import InlineCallbacks
from telegram_api.actions import ACTION_MAP
from telegram_api.callbacks import CALLBACK_MAP
from .models import Subscriber


def get_subscriber(uid: str, bot: Bot) -> Union[Subscriber, None]:
    return Subscriber.objects.filter(
        Q(user_id=uid) & Q(bot=bot)
    ).first()


def get_subscriber_telegram(user: dict,
                            bot: Bot) -> Union[Subscriber, None]:
    username = user.get('username')
    name = user.get('first_name', '') + ' ' + user.get('last_name', '')
    if not username:
        username = name
    return Subscriber.objects.update_or_create(
        chat_id=user.get('id'),
        bot=bot,
        defaults={
            'chat_id': user.get('id'),
            'name': name,
            'username': username,
            'is_active': True,
            'is_admin': bot.telegram_operator == user.get('username'),
            'bot': bot,
        }
    )


def get_action_by_text(text) -> int:
    return ACTION_MAP[text.split(' ')[0]]


def get_callback(text) -> (dict, int):
    callback_data = InlineCallbacks.get(text)
    if not callback_data:
        return None, None
    return callback_data, CALLBACK_MAP[callback_data.get('type', '')]


def get_subscribers_of_bot(slug: str) -> QuerySet:
    return Subscriber.objects.filter(bot__slug=slug).order_by("-is_admin", "-is_active")
