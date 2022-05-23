from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from bots_management.models import Bot


def make_message_upload_path(instance: 'Message', filename: str) -> str:
    return f'messages/{instance.sender.bot.name}/{filename}'


def make_reply_upload_path(instance: 'Reply', filename: str) -> str:
    return f'messages/{instance.message.sender.bot.name}/{filename}'


class Subscriber(models.Model):
    """
    Model representing subscriber.
    """
    name = models.CharField("Ім'я", max_length=500, blank=True, null=True)
    username = models.CharField("Нікнейм", max_length=500, blank=True, null=True)
    chat_id = models.CharField("UID чату", max_length=24)
    info = models.TextField("Інформація о користувачі", blank=True,
                            null=True, default=None)
    avatar = models.CharField(
        "Посилання на аватар", max_length=500, blank=True,
        null=True, default=None)
    is_active = models.BooleanField("Чи є підписником", default=True)
    created = models.DateTimeField("Створений", auto_now_add=True)
    updated = models.DateTimeField("Оновлений", auto_now=True)
    is_admin = models.BooleanField("Модератор", default=False)
    bot = models.ForeignKey(
        to=Bot, verbose_name="Яким ботом користується",
        related_name="subscribers", on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"
        db_table = "Subscribers"
        unique_together = [["chat_id", "bot"]]

    def ban_user(self):
        """
        Ban current user.
        """
        if self.is_active is True:
            self.is_active = False
            self.save()

    def __str__(self) -> str:
        return f"{self.name} - <{self.bot}>"

    def get_absolute_url(self) -> str:
        return reverse("subscribers:subscriber-detail",
                       kwargs={"slug": self.chat_id})
