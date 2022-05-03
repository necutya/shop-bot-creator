from django.test import TestCase
from django.contrib.auth import get_user_model

from bots_mailings.models import Post, SentMessage
from bots_mailings.services import create_sent_message_object
from bots_management.models import Bot


class ServicesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(username="super", password="1234")
        cls.bot = Bot.objects.create(
            name="test",
            slug="test",
            token="123",
            telegram_operator="test",
            owner=cls.user,
        )
        cls.post = Post.objects.create(
            bot=cls.bot,
        )

    def test_create_sent_message_object(self):
        create_sent_message_object(
            chat_id=123,
            message_id="123",
            post=self.post,
        )
        self.assertTrue(SentMessage.objects.filter(chat_id=123, message_id=123, post=self.post).exists())
