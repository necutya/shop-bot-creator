import base64
import json
import random
import zlib
from typing import Type, List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from administration.models import Country, DeliveryType, PaymentType
from keyboards.inline_callbacks import InlineCallbacks
from keyboards.utils import _make_uchr
from orders.models import Basket
from products.models import Product, Category


class InlineKeyboardBuilder:
    inline_buttons: List[InlineKeyboardButton] = []

    @staticmethod
    def add_like_btn(product: Product, message_to_edit: str, start_from: int) -> Type['InlineKeyboardBuilder']:
        """
        Add like button to keyboard
        """
        callback_data = {
            'type': 'like',
            'id': product.id,
            'message_to_edit': message_to_edit,
            'start_from': start_from,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{_make_uchr('U+2665')} {product.likes}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_seen_btn(product: Product, ) -> Type['InlineKeyboardBuilder']:
        """
        Add like button to keyboard
        """
        callback_data = {
            'type': 'seen',
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{_make_uchr('U+1F440')} {product.views_count}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_cart_add_btn(product: Product, amount: int) -> Type['InlineKeyboardBuilder']:
        """
        Add button to add item to cart
        """
        callback_data = {
            'type': 'add_cart',
            'id': product.id,
            'amount': amount,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Придбати {_make_uchr('U+1F4B8')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_incr_item_btn(product: Product, amount: int, message_to_edit: str, start_from: str, category_id: int) -> \
            Type['InlineKeyboardBuilder']:
        """
        Add button to increment item in cart
        """
        callback_data = {
            'type': 'incr',
            'id': product.id,
            'message_to_edit': message_to_edit,
            'amount': amount,
            'start_from': start_from,
            'category_id': category_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{_make_uchr('U+2795')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_decr_item_btn(product: Product, amount: int, message_to_edit: str, start_from: str, category_id: int) -> \
            Type['InlineKeyboardBuilder']:
        """
        Add button to decrement item in cart
        """
        callback_data = {
            'type': 'decr',
            'id': product.id,
            'message_to_edit': message_to_edit,
            'amount': amount,
            'start_from': start_from,
            'category_id': category_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{_make_uchr('U+2796')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_delete_item_btn(product: Product) -> Type['InlineKeyboardBuilder']:
        """
        Add button to delete item in cart
        """
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{_make_uchr('U+1F5D1')}",
            callback_data=f"delete {product.id}"
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_category_btn(category: Category) -> Type['InlineKeyboardBuilder']:
        """
        Add button to delete item in cart
        """
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{category.name.title()}",
            callback_data=f"category {category.id}"
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_next_page_btn(pager_type: str, pager_item_id: int, message_id: str, category_id: int) -> Type[
        'InlineKeyboardBuilder']:
        """
        Add button to delete item in cart
        """
        callback_data = {
            'type': 'next',
            pager_type: True,
            'start_from': pager_item_id,
            'message_to_edit': message_id,
            'category_id': category_id
        }

        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Наступна сторінка {_make_uchr('U+2B07')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_prev_page_btn(pager_type: str, pager_item_id: int, message_id: str, category_id: int) -> Type[
        'InlineKeyboardBuilder']:
        """
        Add button to delete item in cart
        """
        callback_data = {
            'type': 'prev',
            pager_type: True,
            'start_from': pager_item_id,
            'message_to_edit': message_id,
            'category_id': category_id
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Минула сторінка {_make_uchr('U+1F53C')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_choose_country_btn(country: Country, order_id: int, message_id: str) -> Type['InlineKeyboardBuilder']:
        """
        Add button to choose country for order
        """
        callback_data = {
            'type': 'choose_country',
            'id': order_id,
            'country_id': country.id,
            'message_to_edit': message_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{country.name}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_choose_delivery_btn(delivery: DeliveryType, order_id: int, message_id: str) -> Type['InlineKeyboardBuilder']:
        """
        Add button to choose delivery type for order
        """
        callback_data = {
            'type': 'choose_delivery',
            'id': order_id,
            'delivery_id': delivery.id,
            'message_to_edit': message_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{delivery.name}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_choose_payment_btn(payment: PaymentType, order_id: int, message_id: str) -> Type['InlineKeyboardBuilder']:
        """
        Add button to choose payment type for order
        """
        callback_data = {
            'type': 'choose_payment',
            'id': order_id,
            'payment_id': payment.id,
            'message_to_edit': message_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"{payment.name}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_submit_btn(order_id: int, message_id: str) -> Type['InlineKeyboardBuilder']:
        """
        Add submit button for order
        """
        callback_data = {
            'type': 'submit_order',
            'id': order_id,
            'message_to_edit': message_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Підтвердити {_make_uchr('U+2705')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_cancelled_btn(order_id: int, message_id: str) -> Type['InlineKeyboardBuilder']:
        """
        Add submit button for order
        """
        callback_data = {
            'type': 'cancelled_order',
            'id': order_id,
            'message_to_edit': message_id,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Відмінити {_make_uchr('U+274C')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_edit_btn(order_id: int, message_to_edit: str) -> Type['InlineKeyboardBuilder']:
        """
        Add decline button for order
        """
        callback_data = {
            'type': 'edit_order',
            'id': order_id,
            'message_to_edit': message_to_edit,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Редагувати {_make_uchr('U+1F4DD')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_clear_basket_btn(basket: Basket, message_to_edit: str) -> \
            Type['InlineKeyboardBuilder']:
        callback_data = {
            'type': 'clear_cart',
            'id': basket.id,
            'message_to_edit': message_to_edit,
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Очистити кошик{_make_uchr('U+1F5D1')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_create_order_btn() -> \
            Type['InlineKeyboardBuilder']:
        callback_data = {
            'type': 'create_order',
        }
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=f"Створити замовлення {_make_uchr('U+1F6D2')}",
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def add_custom_btn(text: str, callback_data: dict) -> Type['InlineKeyboardBuilder']:
        """
        Add decline button for order
        """
        InlineKeyboardBuilder.inline_buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=InlineCallbacks.set(callback_data)
        ))
        return InlineKeyboardBuilder

    @staticmethod
    def create(row_width: int = 2) -> InlineKeyboardMarkup:
        """
        Creates keyboard markup for buttons
        Maximum buttons in line - 3, but can be less
        """
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*InlineKeyboardBuilder.inline_buttons)
        InlineKeyboardBuilder.inline_buttons.clear()
        return markup
