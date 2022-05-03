from django.test import TestCase
from django.contrib.auth import get_user_model

from bots_mailings.models import Post, SentMessage
from bots_management.models import Bot


class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="super", password="1234")
        bot = Bot.objects.create(
            name="test",
            slug="test",
            token="123",
            telegram_operator="test",
            owner=user,
        )
        cls.post = Post.objects.create(
            bot=bot,
        )

    def test_str(self):
        self.assertEqual(self.post.__str__(), "Post 1")

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/bot/test/mailing/1/")

    def test_get_update_url(self):
        self.assertEqual(self.post.get_update_url(), "/bot/test/mailing/1/update/")

    def test_get_delete_url(self):
        self.assertEqual(self.post.get_delete_url(), "/bot/test/mailing/1/delete/")


class SentMessageModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_superuser(username="super", password="1234")
        bot = Bot.objects.create(
            name="test",
            slug="test",
            token="123",
            telegram_operator="test",
            owner=user,
        )
        cls.post = Post.objects.create(
            bot=bot,
        )
        cls.sent_message = SentMessage.objects.create(
            chat_id=123,
            message_id=1,
            post=cls.post,
        )

    def test_str(self):
        self.assertEqual(self.sent_message.__str__(), "Sent message 1 to 123")
