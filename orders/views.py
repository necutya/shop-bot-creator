from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from bots_management.mixins import OwnerRequiredMixin
from bots_management.services import get_bot_by_slug
from orders.models import Order
from telegram_api.api import send_message


class OrderListView(OwnerRequiredMixin, ListView):
    template_name = "orders/order_list.html"
    context_object_name = 'orders'

    def get_queryset(self):
        bot = get_bot_by_slug(self.kwargs['slug'])
        return Order.objects.filter(basket__subscriber__bot=bot).exclude(status=Order.DRAFT)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


def accept_order(request, slug, order_id):
    return resolve_order(request, slug, order_id, Order.ACCEPTED)


def decline_order(request, slug, order_id):
    return resolve_order(request, slug, order_id, Order.CANCELED)


def resolve_order(request, bot_slug, order_id, status):
    if request.method == 'POST':
        data = request.POST
        comment = data.get("comment")

        order = get_object_or_404(Order, pk=order_id)
        order.status = status
        if comment:
            order.shopComment = comment
        order.save()

        send_message(
            chat_id=order.basket.subscriber.chat_id,
            token=order.basket.subscriber.bot.token,
            text=f"""Статус вашого замовлення був змінений на {order.get_status_display()}.
<b>Коментар магазину</b>: {order.shopComment if order.shopComment else '-'}
            
<b>ID</b>: {order.id}
<b>Статус</b>: {order.get_status_display()}
<b>Ціна</b>: {order.basket.price}
<b>Дата створення</b>: {order.created_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
<b>Ваш коментар</b>: {order.customerComment if order.customerComment else '-'}
<b>Товари</b>: {', '.join([product.name for product in order.basket.products.all()])}

Для отримання більш детальної інформації зв'яжіться з оператором магазину: @{order.basket.subscriber.bot.telegram_operator}
""",

        )
        return redirect('bots-management:orders:order-list', slug=bot_slug)

    return Http404
