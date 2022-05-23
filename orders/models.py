from decimal import Decimal

from django.db import models

from bots_management.models import Bot
from products.models import Product
from subscribers.models import Subscriber
from administration.models import (
    Country, DeliveryType, PaymentType
)


class MultipleActiveBasketException(Exception):
    def __init__(self, subscriber, message="Subscriber from chat {} has more than one active basket."):
        self.subscriber = subscriber
        self.message = message.format(self.subscriber.chat_id)
        super().__init__(message)

    def __str__(self):
        return self.message


class Basket(models.Model):
    subscriber = models.ForeignKey(
        Subscriber,
        verbose_name="Володар кошику",
        on_delete=models.CASCADE,
        related_name="baskets",
    )
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(
        Product,
        verbose_name="Товари",
        related_name="baskets",
        through='BasketProduct'
    )
    archived = models.DateTimeField("Дата архівування", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            qs = type(self).objects.filter(subscriber=self.subscriber, is_active=True)
            if qs.exists() and qs.first().id != self.id:
                raise MultipleActiveBasketException(self.subscriber)
        super().save(*args, **kwargs)

    @property
    def price(self) -> float:
        """
        Calculate the total price of the basket
        """
        s = 0

        for product in self.products.all():
            product_baskets = BasketProduct.objects.filter(product=product, basket=self)
            for basket_product in product_baskets.all():
                s += product.final_price * basket_product.amount

        return s

    def __str__(self) -> str:
        return f"Basket of {self.subscriber.chat_id} <bot: f{self.subscriber.bot.name}> - (active={self.is_active})"


class BasketProduct(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        "Кількість", default=1
    )



class Order(models.Model):
    DRAFT = 'draft'
    NEW = 'new'
    CANCELED = 'canceled'
    ACCEPTED = 'accepted'
    DONE = 'done'

    STATUSES = [
        (NEW, 'Новий'),
        (CANCELED, 'Відміна'),
        (ACCEPTED, 'Прийнятий'),
        (DONE, 'Закритий'),
    ]

    basket = models.ForeignKey(
        Basket,
        verbose_name="Кошик",
        on_delete=models.CASCADE,
        related_name="Orders",
    )

    country = models.ForeignKey(
        Country,
        verbose_name="Країна доставки",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )

    delivery_type = models.ForeignKey(
        DeliveryType,
        verbose_name="Тип доставки",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )

    payment_type = models.ForeignKey(
        PaymentType,
        verbose_name="Спосіб оплати",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        'Статус замовлення',
        choices=STATUSES,
        default=NEW,
        max_length=60
    )

    price = models.DecimalField("Сума", max_digits=6, decimal_places=2)

    created_stamp = models.DateTimeField("Дата створення", auto_now_add=True)
    closed_stamp = models.DateTimeField("Дата обробки", blank=True, null=True)

    customerComment = models.CharField("Коментар покупця", max_length=1200, null=True)
    shopComment = models.CharField("Коментар продваця", max_length=1200, null=True)

    def __str__(self) -> str:
        return f"Order {self.basket.subscriber.chat_id} <bot: f{self.basket.subscriber.bot.name}> - {self.status}"

    def editable(self):
        return self.status == Order.NEW

    def save(self, *args, **kwargs):
        self.basket.is_active = False
        self.basket.save()
        super().save(*args, **kwargs)
