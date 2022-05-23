import logging
from typing import Union

import requests

from django.conf import settings

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, Message, InlineKeyboardMarkup, InputMediaPhoto
from telebot.apihelper import ApiException

from moviepy.editor import VideoFileClip

logger = logging.getLogger(__name__)


def get_webhook_info(token: str) -> dict:
    """
    Get information about tg webhook
    """
    res = requests.get(settings.TELEGRAM_BASE_URL % (token, "getWebhookInfo"))
    return res.json().get('result')


def get_bot_info(token: str) -> dict:
    """
        Get information about tg bot
    """
    res = requests.get(settings.TELEGRAM_BASE_URL % (token, "getMe"))
    return res.json().get('result')


def send_message(chat_id: str, text: str, token: str,
                 reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
                 parse_mode: str = 'HTML',
                 **kwargs) -> Message:
    """Sends `sendMessage` API request to the telegramAPI.

    chat_id: Id of the chat.
    text: Text of the message.
    reply_markup: Instance of the `InlineKeyboardMarkup`.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            **kwargs
        )
        return response
    except ApiException as e:
        logger.warning(
            f"""Send message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Send message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )


def edit_message(chat_id: str, message_id: str, text: str, token: str,
                 reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
                 parse_mode: str = 'HTML',
                 **kwargs) -> Message:
    """Sends `sendMessage` API request to the telegramAPI.

    chat_id: Id of the chat.
    text: Text of the message.
    reply_markup: Instance of the `InlineKeyboardMarkup`.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).edit_message_text(
            chat_id=chat_id,
            text=text,
            message_id=message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            **kwargs
        )
        return response
    except ApiException as e:
        logger.warning(
            f"""Edit message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Edit message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )


def edit_message_reply_markup(chat_id: str, message_id: str, token: str,
                              reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
                              **kwargs) -> Message:
    """Sends `sendMessage` API request to the telegramAPI.

    chat_id: Id of the chat.
    text: Text of the message.
    reply_markup: Instance of the `InlineKeyboardMarkup`.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            **kwargs
        )
        return response
    except ApiException as e:
        logger.warning(
            f"""Edit message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Edit message to {chat_id} failed.
            token: {token}.
            Error: {e}"""
        )


def send_photo(token: str, chat_id: str, caption: str = None, photo: str = None,
               photo_id: str = None, parse_mode="HTML",
               reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
               **kwargs) -> Message:
    """Sends `sendPhoto` API request to the telegramAPI.

    chat_id: Id of the chat.
    file_path: path to the file.
    file_id: id of the file
    token: bot's token

    Returns: None.
    """
    # if not file_id:
    #     file_id = check_file_id(action, file_path, token)
    if not photo_id and not photo:
        raise ValueError('file_id or file_path must be provided')

    try:
        if photo_id:
            response: Message = TeleBot(token).send_photo(
                chat_id=chat_id, photo=photo_id, caption=caption, parse_mode=parse_mode, reply_markup=reply_markup,
            )
        else:
            response: Message = TeleBot(token).send_photo(
                chat_id=chat_id, photo=photo, caption=caption, parse_mode=parse_mode, reply_markup=reply_markup,
            )
            # file_id = response.json.get('photo')[-1].get('file_id')
            # update_or_create_file_id(action, file_path, file_id, token)

        return response

    except ApiException as e:
        logger.warning(
            f"""Edit photo to {chat_id} failed.
            token: {token}.
            Error ApiException: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Edit photo to {chat_id} failed.
            token: {token}.
            Error Exception: {e}"""
        )


def edit_photo(token: str, chat_id: str, message_id: str, caption: str = None, photo: str = None,
               photo_id: str = None, parse_mode="HTML",
               reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
               **kwargs) -> Message:
    """Sends `sendPhoto` API request to the telegramAPI.

    chat_id: Id of the chat.
    file_path: path to the file.
    file_id: id of the file
    token: bot's token

    Returns: None.
    """
    # if not file_id:
    #     file_id = check_file_id(action, file_path, token)
    if not photo_id and not photo:
        raise ValueError('file_id or file_path must be provided')

    try:
        if photo_id:
            response: Message = TeleBot(token).edit_message_media(
                chat_id=chat_id, media=photo_id, reply_markup=reply_markup, message_id=message_id,
            )
        else:
            response: Message = TeleBot(token).edit_message_media(
                InputMediaPhoto(photo), chat_id=chat_id, message_id=message_id,
            )

        if caption:
            response: Message = TeleBot(token).edit_message_caption(
                chat_id=chat_id, caption=caption, reply_markup=reply_markup, message_id=message_id,
                parse_mode=parse_mode
            )
            # file_id = response.json.get('photo')[-1].get('file_id')
            # update_or_create_file_id(action, file_path, file_id, token)
        return response

    except ApiException as e:
        logger.warning(
            f"""Send photo to {chat_id} failed.
            token: {token}.
            Error ApiException: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Send photo to {chat_id} failed.
            token: {token}.
            Error Exception: {e}"""
        )


# def check_file_id(action: object,
#                   file_path: str,
#                   token: str) -> Union[str, None]:
#     from old_code_for_use.keyboards import IdFilesInMessenger
#     info = IdFilesInMessenger.objects.filter(action=action, token_tg=token)
#     if info.exists():
#         info = info.first()
#         if info.path_media_tg == file_path:
#             return info.telegram_id
#
#
# def update_or_create_file_id(action: object,
#                              file_path: str = None,
#                              file_id: str = None,
#                              token: str = None) -> "keIdFilesInMessenger":
#     from old_code_for_use.keyboards import IdFilesInMessenger
#     return IdFilesInMessenger.objects.update_or_create(
#         action=action,
#         token_tg=token,
#         defaults={
#             'action': action,
#             'path_media_tg': file_path,
#             'telegram_id': file_id,
#             'token_tg': token,
#         }
#     )

def send_sticker(chat_id: int, token: str,
                 sticker_path: str = None,
                 sticker_id: str = None, **kwargs) -> Message:
    """Sends `sendSticker` API request to the telegramAPI.

    chat_id: Id of the chat.
    sticker_path: path to the sticker.
    sticker_id: id of the sticker
    token: bot's token

    Returns: None.
    """
    if not sticker_id and not sticker_path:
        # TODO change it after realization telegram stiker
        return

    try:
        if sticker_path:
            with open(sticker_path, 'rb') as file:
                TeleBot(token).send_sticker(
                    chat_id=chat_id, data=file
                )
        else:
            TeleBot(token).send_sticker(
                chat_id=chat_id, data=sticker_id
            )

    except ApiException as e:
        print(f"LOGGING: {e}")
    except Exception as e:
        print(f"LOGGING: {e}")


def delete_message(chat_id: Union[str, int], message_id: int,
                   token: str) -> None:
    """
    Delete message using Telegram API
    :param chat_id: Id of a chat.
    :param message_id: Id of a message.
    :param token: Bot`s token
    """
    try:
        TeleBot(token).delete_message(chat_id=chat_id, message_id=message_id)
    except ApiException as e:
        logger.warning(
            f"""Delete message {message_id} in {chat_id} failed.
                    token: {token}.
                    Error: {e}"""
        )
    except Exception as e:
        logger.warning(
            f"""Delete message with id {message_id} in {chat_id} failed.
                    token: {token}.
                    Error: {e}"""
        )


def set_webhook(slug: str, host: str, token: str) -> dict:
    """
    Sets telegram webhook for certain channel.
    """
    webhook = f"https://{host}/telegram/api/{slug}/"
    url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook}"
    response = requests.get(url)
    logger.warning(
        f"""Set telegram-webhook {url}.
            token {token}. Answer: {response.text}"""
    )
    return response.json()


def unset_webhook_ajax(token: str) -> dict:
    """
    Sets telegram webhook for certain channel.
    """
    webhook = ""
    url = f"https://api.telegram.org/bot{token}/setWebhook?url={webhook}"
    response = requests.get(url)
    logger.warning(
        f"""Set telegram-webhook with ajax {url}.
            token {token}. Answer: {response.text}"""
    )
    return response.json()


def send_callback_answer(callback_query_id: str, text: str, token: str,

          **kwargs) -> Message:
    """Sends `sendMessage` API request to the telegramAPI.

    chat_id: Id of the chat.
    text: Text of the message.
    reply_markup: Instance of the `InlineKeyboardMarkup`.
    token: bot's token

    Returns: None.
    """
    try:
        response: Message = TeleBot(token).answer_callback_query(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=True,
            **kwargs
        )
        return response
    except ApiException as e:
        logger.warning(
            f"""Callback answer to {callback_query_id} failed.
            token: {token}.
            Error: {e}"""
        )
    except Exception as e:
        logger.critical(
            f"""Callback answer to {callback_query_id} failed.
            token: {token}.
            Error: {e}"""
        )
