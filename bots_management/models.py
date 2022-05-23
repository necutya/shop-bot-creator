from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django.conf import settings
from telegram_api.api import set_webhook as set_telegram_webhook
from administration.models import (
    Country, DeliveryType, PaymentType, Currency
)


class TermsOfAgreementException(Exception):
    def __init__(self, message="Без пользовательского соглашения невозможно создать бота"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class Bot(models.Model):
    """
    Model for representing channel.
    Each channel has its own bots with own tokens.
    We can crete webhooks using slugs of each model.
    """
    name = models.CharField("Назва", max_length=128, unique=True)
    slug = models.SlugField("URL", max_length=128, unique=True)
    description = models.CharField(
        "Опис", max_length=250, blank=True, null=True
    )
    token = models.CharField("Токен", max_length=150, unique=True)
    owner = models.ForeignKey(
        get_user_model(), blank=True, verbose_name="Власник", on_delete=models.CASCADE, related_name="bots"
    )
    telegram_operator = models.CharField(
        "Посилання на telegram оператора", max_length=255
    )

    available_countries = models.ManyToManyField(
        Country, verbose_name="Доступні країни", related_name="bots"
    )
    available_delivery_type = models.ManyToManyField(
        DeliveryType, verbose_name="Доступні типи доставок", related_name="bots"
    )
    available_payment_types = models.ManyToManyField(
        PaymentType, verbose_name="Доступні способи оплати", related_name="bots"
    )
    currency = models.ForeignKey(
        Currency, verbose_name="Валюта", related_name="bots", on_delete=models.SET_NULL, null=True
    )
    is_webhook_set = models.BooleanField(
        "Установлен ли вебхук", default=False
    )
    welcome_text = models.TextField(
        verbose_name="Вітальне повідомлення", blank=True,
        null=True, default=None
    )
    terms_of_agreement = models.BooleanField("Користувацька угода", default=False)

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"
        db_table = "bots"

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        response: dict = set_telegram_webhook(token=self.token, host=settings.SITE_URL, slug=self.slug)
        if response.get("ok"):
            self.is_webhook_set = True
            self.save()

    def get_update_url(self) -> str:
        return reverse("bots-management:bot-update",
                       kwargs={"slug": self.slug})

    def get_delete_url(self) -> str:
        return reverse("bots-management:bot-delete",
                       kwargs={"slug": self.slug})
