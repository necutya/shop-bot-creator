import json
import logging
import time

from bots_management.models import Bot
from bots_management.services import get_bot_by_slug
from keyboards.inline_keyboard_builder import InlineKeyboardBuilder
from keyboards.keyboard_builder import KeyboardBuilder
from keyboards.utils import _make_uchr
from orders.models import Order, Basket, BasketProduct
from products.models import Product, Category
from subscribers.models import Subscriber
from subscribers.services import get_subscriber_telegram, get_action_by_text, get_callback
from telegram_api.actions import *
from telegram_api.callbacks import *
from telegram_api.api import send_message, send_photo, edit_photo, edit_message, edit_message_reply_markup, \
    send_callback_answer

logger = logging.getLogger(__name__)


def handle_telegram_event(incoming_data: dict, bot_slug: str) -> None:
    print(incoming_data)
    bot = get_bot_by_slug(slug=bot_slug)
    message_type = "callback" if incoming_data.get("callback_query") else "message"
    if message_type == "message":
        message = incoming_data["message"]

        user = incoming_data.get('message').get('chat')
        sub, created = get_subscriber_telegram(user, bot)
        print(
            f"""Subscriber {sub} create new {created} (False=update)"""
        )

        if message:
            if 'text' in message:
                if message.get("text") == "/start":
                    start_handler(
                        in_data=incoming_data, bot=bot, sub=sub
                    )
                elif message.get("text").startswith("/"):
                    sys_action_handler(
                        in_data=incoming_data, bot=bot, sub=sub
                    )
                else:
                    action_handler(
                        in_data=incoming_data, bot=bot, sub=sub
                    )
    elif message_type == "callback":
        callback_handler(incoming_data["callback_query"], bot)


def action_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    actions = get_action_by_text(text=in_data['message']['text'])
    if actions == HOME_ACTION_ID:
        return start_handler(in_data, bot, sub)
    elif actions == HELP_ACTION_ID:
        return help_message_handler(in_data, bot, sub)
    elif actions == CATALOG_ACTION_ID:
        return catalog_message_handler(in_data, bot, sub, 0)
    elif actions == CATEGORY_ACTION_ID:
        return category_message_handler(in_data, bot, sub)
    elif actions == ORDERS_ACTION_ID:
        return orders_message_handler(in_data, bot, sub)
    elif actions == BASKET_ACTION_ID:
        return check_basket_message_handler(in_data, bot, sub)


def sys_action_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    sys = in_data['message']['text'].split(' ')[0]
    if sys == '/comment':
        return add_order_comment_handler(in_data, bot, sub)


def callback_handler(in_data: dict, bot: Bot) -> None:
    user = in_data.get('from')
    sub, created = get_subscriber_telegram(user, bot)
    print(
        f"""Subscriber {sub} create new {created} (False=update)"""
    )

    callback, callback_id = get_callback(text=in_data['data'])
    if callback is None:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )

    if callback_id in (NEXT_CALLBACK_ID, PREV_CALLBACK_ID):
        if callback.get('products', False):
            message_to_edit = callback['message_to_edit']
            start_from = callback['start_from']
            return catalog_message_handler(in_data, bot, sub, int(start_from), message_to_edit,
                                           in_data['message']['message_id'], category_id=callback["category_id"])

    elif callback_id == CATEGORY_CALLBACK_ID:
        category_id = callback.get('id', None)
        return catalog_message_handler(in_data, bot, sub, 0, category_id=category_id)

    elif callback_id == LIKE_CALLBACK_ID:
        product_id = callback.get('id', None)
        message_to_edit = callback.get('message_to_edit', None)
        start_from = callback['start_from']
        return like_message_handler(in_data, bot, sub, start_from, product_id=product_id,
                                    message_id=message_to_edit)

    elif callback_id == ORDER_CALLBACK_ID:
        order_id = callback.get('id', None)
        message_to_edit = callback.get('message_to_edit', None)
        return orders_message_handler(in_data, bot, sub, order_id=order_id,
                                      message_id=message_to_edit)

    elif callback_id in (INCR_CALLBACK_ID, DECR_CALLBACK_ID):
        message_to_edit = callback['message_to_edit']
        start_from = callback['start_from']
        amount = callback['amount']
        return catalog_message_handler(in_data, bot, sub, int(start_from), message_to_edit,
                                       in_data['message']['message_id'], category_id=callback["category_id"],
                                       current_amount=amount)

    elif callback_id == ADD_CART_CALLBACK_ID:
        product_id = callback['id']
        amount = callback['amount']
        return add_to_cart_handler(in_data, bot, sub, product_id, amount)

    elif callback_id == CLEAR_CART_CALLBACK_ID:
        message_to_edit = callback['message_to_edit']
        return clear_basket_message_handler(in_data, bot, sub, message_to_edit)

    elif callback_id == CREATE_ORDER_CALLBACK_ID:
        return create_order_handler(in_data, bot, sub)

    elif callback_id == ADD_ORDER_COUNTRY_CALLBACK_ID:
        message_to_edit = callback['message_to_edit']
        order_id = callback['id']
        country_id = callback['country_id']
        return add_order_country_handler(in_data, bot, sub, order_id, country_id, message_to_edit)

    elif callback_id == ADD_ORDER_DELIVERY_CALLBACK_ID:
        message_to_edit = callback['message_to_edit']
        order_id = callback['id']
        delivery_id = callback['delivery_id']
        return add_order_delivery_handler(in_data, bot, sub, order_id, delivery_id, message_to_edit)

    elif callback_id == ADD_ORDER_PAYMENT_CALLBACK_ID:
        message_to_edit = callback['message_to_edit']
        order_id = callback['id']
        payment_id = callback['payment_id']
        return add_order_payment_handler(in_data, bot, sub, order_id, payment_id, message_to_edit)

    elif callback_id == EDIT_ORDER_CALLBACK_ID:
        message_to_edit = callback['message_to_edit']
        order_id = callback['id']
        return create_order_handler(in_data, bot, sub, order_id=order_id, message_id=message_to_edit)

    elif callback_id in (SUBMIT_ORDER_CALLBACK_ID, CANCELLED_ORDER_CALLBACK_ID):
        message_to_edit = callback['message_to_edit']
        order_id = callback['id']
        if callback_id == SUBMIT_ORDER_CALLBACK_ID:
            action = 'submit'
        else:
            action = 'cancel'
        return resolve_order_handler(in_data, bot, sub, order_id=order_id, message_id=message_to_edit, action=action)

    elif callback_id in (AMOUNT_CALLBACK_ID, SEEN_CALLBACK_ID):
        return


def clear_basket_message_handler(in_data: dict, bot: Bot, sub: Subscriber, message_id: str = None) -> None:
    baskets = Basket.objects.filter(subscriber=sub, is_active=True).order_by("id")

    if not baskets.exists():
        send_callback_answer(
            in_data["id"],
            "У вас немає активних кошиків",
            bot.token
        )
        return

    basket = baskets.first()
    basket.products.clear()
    basket.save()

    return check_basket_message_handler(in_data, bot, sub, message_id)


def check_basket_message_handler(in_data: dict, bot: Bot, sub: Subscriber, message_id: str = None) -> None:
    baskets = Basket.objects.filter(subscriber=sub, is_active=True).order_by("id")

    if not baskets.exists():
        send_message(
            sub.chat_id,
            "У вас немає активних кошиків",
            bot.token
        )
        return

    basket = baskets.first()
    products_info = ""
    basket_keyboard = InlineKeyboardBuilder

    if not basket.products.exists():
        products_info += "-\n"

    for product in basket.products.all():
        product_baskets = BasketProduct.objects.filter(basket=basket, product=product)
        for product_basket in product_baskets.all():
            products_info += f"<i><u>{product.name}</u></i> x {product_basket.amount} ({product.final_price}x{product_basket.amount}={round(product.final_price * product_basket.amount, 2)})\n"
    else:
        products_info += f"-------------\nСума: <i><b>{basket.price}</b></i>"

    text = f"""Ваш кошик:
{products_info}
"""
    if not message_id:
        message = send_message(
            chat_id=sub.chat_id,
            text=text,
            token=bot.token
        )
    else:
        message = edit_message(
            message_id=message_id,
            chat_id=sub.chat_id,
            text=text,
            token=bot.token
        )
    edit_message_reply_markup(
        message_id=message.message_id,
        chat_id=sub.chat_id,
        token=bot.token,
        reply_markup=basket_keyboard.
            add_clear_basket_btn(basket, message.message_id).
            add_create_order_btn().
            create(1)
    )

    if not message:
        error_handler(sub.chat_id, bot.token)
        return


def orders_message_handler(in_data: dict, bot: Bot, sub: Subscriber, message_id: str = None,
                           order_id: int = None) -> None:
    orders = Order.objects.filter(basket__subscriber__bot=bot, basket__subscriber=sub).exclude(
        status=Order.DRAFT).order_by("id")

    if order_id:
        order = Order.objects.filter(basket__subscriber__bot=bot, basket__subscriber=sub).get(pk=order_id)
        order.status = Order.CANCELED
        order.save()

    cancelled_orders = []

    orders_builder = InlineKeyboardBuilder
    text = f"""<b>Загальна кількість замолвень: {orders.count()}
Кількість активних: {orders.filter(status=Order.NEW).count()}
Кількість закритих: {orders.filter(status=Order.CANCELED).count()}
Кількість опрацьованних: {orders.filter(status__in=[Order.ACCEPTED, Order.DONE]).count()}
</b>
"""

    for order in orders.all():
        products = []
        for product in order.basket.products.all():
            product_baskets = BasketProduct.objects.filter(basket=order.basket, product=product)
            for product_basket in product_baskets.all():
                products.append(f"{product.name} x {product_basket.amount}")

        text += f"""<b>ID</b>: {order.id}
<b>Статус</b>: {order.get_status_display()}
<b>Ціна</b>: {order.basket.price}
<b>Створено</b>: {order.created_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
<b>Ваш коментар</b>: {order.customerComment if order.customerComment else '-'}
<b>Коментар магазину</b>: {order.shopComment if order.shopComment else '-'}
<b>Країна доставки</b>: {order.country}
<b>Тип доставки</b>: {order.delivery_type}
<b>Тип оплати</b>: {order.payment_type}
<b>Товари</b>: {', '.join(products)}

"""
        if order.status == Order.NEW:
            cancelled_orders.append(order)

    if not message_id:
        message = send_message(
            chat_id=sub.chat_id,
            text=text,
            token=bot.token
        )
    else:
        message = edit_message(
            message_id=message_id,
            chat_id=sub.chat_id,
            text=text,
            token=bot.token
        )

    if not message:
        error_handler(sub.chat_id, bot.token)
        return

    for order in cancelled_orders:
        orders_builder.add_custom_btn(
            f"Відмінити замовлення номер {order.id}",
            callback_data={
                'type': 'order',
                'id': order.id,
                'message_to_edit': message.message_id,
            },
        )

    if cancelled_orders and not edit_message_reply_markup(
            chat_id=sub.chat_id,
            reply_markup=orders_builder.create(),
            token=bot.token,
            message_id=message.message_id
    ):
        error_handler(sub.chat_id, bot.token)
        return


def category_message_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    categories = Category.objects.filter(bot=bot).order_by("name")

    category_board_builder = InlineKeyboardBuilder
    for category in categories:
        category_board_builder.add_custom_btn(text=category.name, callback_data={
            'type': 'category',
            'id': category.id
        })

    send_message(
        chat_id=sub.chat_id,
        text=f'Категорії товарів',
        reply_markup=category_board_builder.create(),
        token=bot.token
    )


def catalog_message_handler(in_data: dict, bot: Bot, sub: Subscriber, start_from: int, message_id: str = None,
                            pagination_message_id: str = None, category_id: int = None,
                            product_id: int = None, current_amount: int = 1) -> None:
    products = Product.objects.filter(bot=bot, visible=True).order_by("name")

    if category_id:
        products.filter(categories__id=category_id)

    if product_id:
        products.get(id=product_id)

    if start_from + 1 > products.count():
        send_message(
            chat_id=sub.chat_id,
            text=f'Усі товари були переглянуті',
            token=bot.token
        )
        return

    if start_from < 0:
        send_message(
            chat_id=sub.chat_id,
            text=f'Щось пішло не так!(',
            token=bot.token
        )
        return

    product = products.all()[start_from: start_from + 1][0]

    categories = ', '.join([c.name.title() for c in product.categories.all()])
    text = f"""<b>Назва: {product.name}</b>
Опис: {product.description if product.description else '-'}
Ціна: {product.final_price} {product.bot.currency.symbol}
Категорії: {categories} 
"""
    if product.url:
        text += f"Посилання на товар в інтернет магазині: {product.url}"

    product_photo = product.photos.filter(is_main=True).first()
    photo = product_photo.image_url
    if product_photo.image:
        photo = product_photo.image.url

    incr_amount, decr_amount = current_amount, current_amount
    if current_amount < product.amount:
        incr_amount += 1

    if decr_amount > 1:
        decr_amount -= 1

    if message_id is None or message_id == 'None':
        message = send_photo(
            chat_id=sub.chat_id,
            caption=text,
            photo=photo,
            token=bot.token
        )
    else:
        message = edit_photo(
            chat_id=sub.chat_id,
            message_id=message_id,
            caption=text,
            photo=photo,
            token=bot.token,
        )

    edit_message_reply_markup(
        chat_id=sub.chat_id,
        message_id=message.message_id,
        reply_markup=InlineKeyboardBuilder.
            add_like_btn(product, message.message_id, start_from).
            add_cart_add_btn(product, current_amount).
            add_seen_btn(product).
            add_decr_item_btn(product=product, amount=decr_amount, message_to_edit=message.message_id,
                              start_from=start_from, category_id=category_id).
            add_custom_btn(f"{current_amount} шт.", {'type': 'amount'}).
            add_incr_item_btn(product=product, amount=incr_amount, message_to_edit=message.message_id,
                              start_from=start_from, category_id=category_id).
            create(3)
        ,
        token=bot.token,
    )
    if message is None:
        send_message(
            chat_id=sub.chat_id,
            text=f'Щось пішло не так!(',
            token=bot.token
        )
        return

    if product_id:
        return

    product_pagination_key_board_builder = InlineKeyboardBuilder

    if not (start_from <= 0):
        product_pagination_key_board_builder.add_prev_page_btn('products', start_from - 1, message.message_id,
                                                               category_id)

    if not (start_from + 1 >= products.count()):
        product_pagination_key_board_builder.add_next_page_btn('products', start_from + 1, message.message_id,
                                                               category_id)

    if pagination_message_id is None or pagination_message_id == 'None':
        send_message(
            chat_id=sub.chat_id,
            text=f'Відображено {start_from + 1} з {products.count()}',
            reply_markup=product_pagination_key_board_builder.create(),
            token=bot.token
        )
    else:
        edit_message(
            chat_id=sub.chat_id,
            text=f'Відображено {start_from + 1} з {products.count()}',
            reply_markup=product_pagination_key_board_builder.create(),
            token=bot.token,
            message_id=pagination_message_id,
        )

    product.views_count += 1
    product.save()


def help_message_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    text = f"Якщо ви маєте питання щодо роботи магазина ви маєте змогу з'эднатися з модератором чату @{bot.telegram_operator}."
    send_message(
        chat_id=sub.chat_id,
        text=text,
        token=bot.token
    )


def like_message_handler(in_data: dict, bot: Bot, sub: Subscriber, start_from: int, product_id: int,
                         message_id: str) -> None:
    products = Product.objects.filter(pk=product_id)
    if products:
        product = products.first()
        product.likes += 1
        product.save()
        catalog_message_handler(in_data, bot, sub, int(start_from), message_id=message_id, product_id=product_id)
    else:
        send_message(
            chat_id=sub.chat_id,
            text=f'Щось пішло не так!(',
            token=bot.token
        )


def add_to_cart_handler(in_data: dict, bot: Bot, sub: Subscriber, product_id: int, amount: int) -> None:
    products = Product.objects.filter(pk=product_id)
    if products.exists():
        product = products.first()

        if not (product.amount >= amount > 0):
            send_callback_answer(
                in_data["id"],
                "Вибрана кількість товари переищує кількість товару у магазині!",
                bot.token,
            )

        basket, created = Basket.objects.get_or_create(
            subscriber=sub,
            is_active=True,
            defaults={
                'subscriber': sub,
                'is_active': True,
            }
        )
        BasketProduct.objects.create(product=product, amount=amount, basket=basket)

        basket.save()

        send_callback_answer(
            in_data["id"],
            "Товар додано до кошика!",
            bot.token,
        )
    else:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )


def start_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    text = f'Вас вітає магазин {bot.name}'
    if welcome := bot.welcome_text:
        text = welcome
    send_message(
        chat_id=sub.chat_id,
        text=text,
        reply_markup=KeyboardBuilder.
            add_home_btn().
            add_catalog_btn().
            add_categories_btn().
            add_help_btn().
            add_check_basket_btn().
            add_orders_btn().
            create()
        ,
        token=bot.token
    )


def create_order_handler(in_data: dict, bot: Bot, sub: Subscriber, order_id: int = None,
                         message_id: str = None) -> None:
    if not order_id:
        baskets = Basket.objects.filter(subscriber=sub, is_active=True).order_by("id")

        if not baskets.exists():
            send_callback_answer(
                in_data["id"],
                "У вас немає активних кошиків",
                bot.token
            )
            return

        basket = baskets.first()

        order = Order.objects.create(
            status=Order.DRAFT,
            basket=basket,
            price=basket.price,
            created_stamp=time.time(),
        )
    else:
        orders = Order.objects.filter(pk=order_id)

        if not orders.exists():
            send_callback_answer(
                in_data["id"],
                "Щось пішло не так!",
                bot.token,
            )
            return

        order = orders.first()

    text = "Оберіть країну для доставки"

    if not message_id:
        message = send_message(
            chat_id=sub.chat_id,
            text=text,
            token=bot.token,
        )
    else:
        message = edit_message(
            message_id=message_id,
            chat_id=sub.chat_id,
            text=text,
            token=bot.token,
        )

    if not message:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    country_inline = InlineKeyboardBuilder
    for country in bot.available_countries.all():
        country_inline.add_choose_country_btn(
            country=country,
            order_id=order.id,
            message_id=message.message_id
        )

    if not edit_message_reply_markup(
            chat_id=sub.chat_id,
            reply_markup=country_inline.create(1),
            token=bot.token,
            message_id=message.message_id
    ):
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )


def add_order_country_handler(in_data: dict, bot: Bot, sub: Subscriber, order_id: int, country_id: int,
                              message_id: int) -> None:
    orders = Order.objects.filter(id=order_id)
    if not orders.exists():
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    order = orders.first()
    order.country_id = country_id
    order.save()

    text = "Оберіть спосіб доставки"

    message = edit_message(
        message_id=message_id,
        chat_id=sub.chat_id,
        text=text,
        token=bot.token,
    )

    if not message:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    delivery_inline = InlineKeyboardBuilder
    for delivery in bot.available_delivery_type.all():
        delivery_inline.add_choose_delivery_btn(
            delivery=delivery,
            order_id=order.id,
            message_id=message.message_id
        )

    if not edit_message_reply_markup(
            chat_id=sub.chat_id,
            reply_markup=delivery_inline.create(1),
            token=bot.token,
            message_id=message.message_id
    ):
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )


def add_order_delivery_handler(in_data: dict, bot: Bot, sub: Subscriber, order_id: int, delivery_id: int,
                               message_id: int) -> None:
    orders = Order.objects.filter(id=order_id)
    if not orders.exists():
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    order = orders.first()
    order.delivery_type_id = delivery_id
    order.save()

    text = "Оберіть спосіб оплати"

    message = edit_message(
        message_id=message_id,
        chat_id=sub.chat_id,
        text=text,
        token=bot.token,
    )

    if not message:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    payment_inline = InlineKeyboardBuilder
    for payment in bot.available_payment_types.all():
        payment_inline.add_choose_payment_btn(
            payment=payment,
            order_id=order.id,
            message_id=message.message_id
        )

    if not edit_message_reply_markup(
            chat_id=sub.chat_id,
            reply_markup=payment_inline.create(1),
            token=bot.token,
            message_id=message.message_id
    ):
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )


def add_order_payment_handler(in_data: dict, bot: Bot, sub: Subscriber, order_id: int, payment_id: int,
                              message_id: int) -> None:
    orders = Order.objects.filter(id=order_id)
    if not orders.exists():
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    order = orders.first()
    order.payment_type_id = payment_id
    order.save()

    products = []
    for product in order.basket.products.all():
        product_baskets = BasketProduct.objects.filter(basket=order.basket, product=product)
        for product_basket in product_baskets.all():
            products.append(f"{product.name} x {product_basket.amount}")

    text = f"""Інформація, щодо вашого замовлення: 
<b>ID</b>: {order.id}
<b>Статус</b>: {order.get_status_display()}
<b>Ціна</b>: {order.basket.price}
<b>Створено</b>: {order.created_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
<b>Ваш коментар</b>: {order.customerComment if order.customerComment else '-'}
<b>Коментар магазину</b>: {order.shopComment if order.shopComment else '-'}
<b>Країна доставки</b>: {order.country}
<b>Тип доставки</b>: {order.delivery_type}
<b>Тип оплати</b>: {order.payment_type}
<b>Товари</b>: {', '.join(products)}


Якщо бажаєте додати додаткову інформацію, щодо доставки вашого замовлення, то напишіть коментар у наступному форматі, де [order_id] - id вашого амовлення:
/comment [order_id] Тут ваш коментар...
Aбо зв'яжіться з оператором магазину: @{bot.telegram_operator}
<b>Важливо:</b> пишіть коментар перед тип як підтвердити або відхилити замовлення. Після того, як ваш коментар буде прийнятий,
підтвердіть замовлення у повідомленні вище. {_make_uchr('U+261D')}
"""

    message = edit_message(
        message_id=message_id,
        chat_id=sub.chat_id,
        text=text,
        token=bot.token,
    )

    if not message:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return

    order_inline = InlineKeyboardBuilder. \
        add_edit_btn(order_id, message.message_id). \
        add_submit_btn(order_id, message.message_id). \
        add_cancelled_btn(order_id, message.message_id)

    if not edit_message_reply_markup(
            chat_id=sub.chat_id,
            reply_markup=order_inline.create(1),
            token=bot.token,
            message_id=message.message_id
    ):
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )


def resolve_order_handler(in_data: dict, bot: Bot, sub: Subscriber, order_id: int,
                          message_id: str, action: str) -> None:
    orders = Order.objects.filter(id=order_id)
    if not orders.exists():
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )

    order = orders.first()

    text = "Щось пішло не так!"
    if action == 'submit':
        order.status = order.NEW
        order.save()
        text = "Замовлення створене. Зайчекайте на повідомлення від адміністратора, щодо підтвердження вашого замовлення.\n" \
               "Відстежити зміни можна у вкладинці ваших замовлень."
    elif action == 'cancel':
        order.delete()
        text = "Замовлення видалене."

    message = edit_message(
        message_id=message_id,
        chat_id=sub.chat_id,
        text=text,
        token=bot.token,
        reply_markup=InlineKeyboardBuilder.create(),
    )

    if not message:
        send_callback_answer(
            in_data["id"],
            "Щось пішло не так!",
            bot.token,
        )
        return


def add_order_comment_handler(in_data: dict, bot: Bot, sub: Subscriber) -> None:
    split = in_data['message']['text'].split(' ', 2)
    orders = Order.objects.filter(id=split[1])
    if not orders.exists() or len(split) != 3:
        error_handler(
            sub.chat_id, bot.token
        )
        return

    order = orders.first()
    if order.status != Order.DRAFT:
        send_message(
            chat_id=sub.chat_id,
            text=f'Це замовлення неможливо редагувати.',
            token=bot.token
        )
        return

    order.customerComment = split[2]
    order.save()

    send_message(
        chat_id=sub.chat_id,
        text=f'Ваш коментар успішно збережений!',
        token=bot.token
    )


# # TODO
# # we can't receive information, that user unsubscribe
# # Only by getting an error while sending user something
#
# # def unsubscribed_handler(in_data: dict, channel_slug: str) -> None:
# #     # TODO log that unsubscribed and
# #     #  Subscriber.object.get(uid=uid).is_active=False
# #     print(in_data)
# #     pass

def error_handler(chat_id, token):
    send_message(
        chat_id=chat_id,
        text=f'Щось пішло не так!(',
        token=token
    )
