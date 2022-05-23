from typing import Type, List
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from django.db.models import Sum

from keyboards.utils import _make_uchr
from orders.models import Basket


class KeyboardBuilder:
    buttons: List[KeyboardButton] = []

    @staticmethod
    def add_home_btn() -> Type['KeyboardBuilder']:
        """
        Add home catalog to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Головна {_make_uchr('U+1F3E0')}"))
        return KeyboardBuilder

    @staticmethod
    def add_catalog_btn() -> Type['KeyboardBuilder']:
        """
        Add news catalog to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Каталог {_make_uchr('U+1F4C2')}"))
        return KeyboardBuilder

    @staticmethod
    def add_categories_btn() -> Type['KeyboardBuilder']:
        """
        Add news categories to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Категорії {_make_uchr('U+1F5C3')}"))
        return KeyboardBuilder

    @staticmethod
    def add_cart_btn() -> Type['KeyboardBuilder']:
        """
        Add news cart to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Корзина {_make_uchr('U+1F6D2')}"))
        return KeyboardBuilder

    @staticmethod
    def add_orders_btn():
        """
        Add orders orders to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Замовлення {_make_uchr('U+1F4E6')}"))
        return KeyboardBuilder

    @staticmethod
    def add_help_btn() -> Type['KeyboardBuilder']:
        """
        Add help button to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Допомога {_make_uchr('U+1F937')}"))
        return KeyboardBuilder

    @staticmethod
    def add_news_btn() -> Type['KeyboardBuilder']:
        """
        Add news button to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Новини {_make_uchr('U+1F4F0')}"))
        return KeyboardBuilder

    @staticmethod
    def add_create_order_btn() -> Type['KeyboardBuilder']:
        """
        Add create order button to keyboard
        """
        KeyboardBuilder.buttons.append(
            KeyboardButton(
                text=f"Зробити замовлення {_make_uchr('U+2705')}")
        )
        return KeyboardBuilder

    @staticmethod
    def add_check_basket_btn() -> Type['KeyboardBuilder']:
        """
        Add create order button to keyboard
        """
        KeyboardBuilder.buttons.append(
            KeyboardButton(
                text=f"Кошик {_make_uchr('U+1F440')}")
        )
        return KeyboardBuilder

    @staticmethod
    def add_clear_cart_btn() -> Type['KeyboardBuilder']:
        """
        Add delete order button to keyboard
        """
        KeyboardBuilder.buttons.append(
            KeyboardButton(
                text=f"Очистити кошик {_make_uchr('U+274C')}")
        )
        return KeyboardBuilder

    @staticmethod
    def add_cart_prev_page_btn(basket: Basket) -> Type['KeyboardBuilder']:
        """
        Add next page of basket`s items button to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Минула сторінка {_make_uchr('U+2B06')}"))
        return KeyboardBuilder

    @staticmethod
    def add_cart_next_page_btn(basket: Basket) -> Type['KeyboardBuilder']:
        """
        Add next page of basket`s items button to keyboard
        """
        KeyboardBuilder.buttons.append(KeyboardButton(text=f"Наступна сторінка {_make_uchr('U+2B07')}"))
        return KeyboardBuilder

    @staticmethod
    def create(row_width: int = 3, selective: bool = True) -> ReplyKeyboardMarkup:
        """
        Creates keyboard markup for buttons
        Maximum buttons in line - 3, but can be less
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width, selective=selective)
        markup.add(*KeyboardBuilder.buttons)
        KeyboardBuilder.buttons.clear()
        return markup