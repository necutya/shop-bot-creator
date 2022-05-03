import time

from django.test import TestCase
from django.test import Client
from unittest.mock import patch

from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from bots_mailings.models import Post
from bots_management.models import Bot


class MailingListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="moderator")
        user.set_password('1234')
        user.save()

        cls.bot_slug = "test"
        bot = Bot.objects.create(
            name="test",
            slug=cls.bot_slug,
            token="123",
            telegram_operator="test",
            owner=user,
        )

    def test_view_url(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(f"/bot/{self.bot_slug}/mailings/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-list", kwargs={"slug": self.bot_slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-list", kwargs={"slug": self.bot_slug}))
        self.assertTemplateUsed(response, "bots_mailings/mailing_list.html")


class MailingCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="moderator")
        user.set_password('1234')
        user.save()

        cls.bot_slug = "test"
        cls.bot = Bot.objects.create(
            name="test",
            slug=cls.bot_slug,
            token="123",
            telegram_operator="test",
            owner=user,
        )

    def test_view_url(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(f"/bot/{self.bot_slug}/mailing/create/")
        self.assertEqual(response.status_code, 200)

        response = c.post(f"/bot/{self.bot_slug}/mailing/create/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-create", kwargs={"slug": self.bot_slug}))
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse("bots-management:mailings:mailing-create", kwargs={"slug": self.bot_slug}))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-create", kwargs={"slug": self.bot_slug}))
        self.assertTemplateUsed(response, "bots_mailings/mailing_create.html")

        response = c.post(reverse("bots-management:mailings:mailing-create", kwargs={"slug": self.bot_slug}))
        self.assertTemplateNotUsed(response)

    def test_view(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.post(
            reverse("bots-management:mailings:mailing-create", kwargs={"slug": self.bot_slug}),
            {
                "bot": self.bot,
            }
        )
        posts = Post.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].bot, self.bot)
        self.assertEqual(response.status_code, 302)


class MailingGetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="moderator")
        user.set_password('1234')
        user.save()

        cls.bot_slug = "test"
        cls.bot = Bot.objects.create(
            name="test",
            slug=cls.bot_slug,
            token="123",
            telegram_operator="test",
            owner=user,
        )
        cls.post = Post.objects.create(
            bot=cls.bot,
        )

    def test_view_url(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(f"/bot/{self.bot_slug}/mailing/{self.post.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-detailed",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-detailed",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertTemplateUsed(response, "bots_mailings/mailing_detailed.html")


class MailingDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="moderator")
        user.set_password('1234')
        user.save()

        cls.bot_slug = "test"
        cls.bot = Bot.objects.create(
            name="test",
            slug=cls.bot_slug,
            token="123",
            telegram_operator="test",
            owner=user,
        )
        cls.post = Post.objects.create(
            bot=cls.bot,
        )

    def test_view_url(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(f"/bot/{self.bot_slug}/mailing/{self.post.id}/delete/")
        self.assertEqual(response.status_code, 200)

        response = c.delete(f"/bot/{self.bot_slug}/mailing/{self.post.id}/delete/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-delete",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertEqual(response.status_code, 200)

        response = c.delete(reverse("bots-management:mailings:mailing-delete",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-delete",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertTemplateUsed(response, "bots_mailings/mailing_delete.html")

        response = c.delete(reverse("bots-management:mailings:mailing-delete",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        self.assertTemplateNotUsed(response)

    def test_view(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.delete(reverse("bots-management:mailings:mailing-delete",
                                 kwargs={"slug": self.bot_slug, "pk": self.post.id}))
        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)
        self.assertEqual(response.status_code, 302)


class MailingUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username="moderator")
        user.set_password('1234')
        user.save()
        cls.user = user

        cls.bot = Bot.objects.create(
            name="test1",
            slug="test1",
            token="123",
            telegram_operator="test1",
            owner=user,
        )
        cls.post = Post.objects.create(
            bot=cls.bot,
        )

    def test_view_url(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(f"/bot/{self.bot.slug}/mailing/{self.post.id}/update/")
        self.assertEqual(response.status_code, 200)

        response = c.put(f"/bot/{self.bot.slug}/mailing/{self.post.id}/update/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-update",
                                 kwargs={"slug": self.bot.slug, "pk": self.post.id}))
        self.assertEqual(response.status_code, 200)

        response = c.put(reverse("bots-management:mailings:mailing-update",
                                 kwargs={"slug": self.bot.slug, "pk": self.post.id}))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        c = Client()
        c.login(username="moderator", password="1234")
        response = c.get(reverse("bots-management:mailings:mailing-update",
                                 kwargs={"slug": self.bot.slug, "pk": self.post.id}))
        self.assertTemplateUsed(response, "bots_mailings/mailing_update.html")

        response = c.put(reverse("bots-management:mailings:mailing-update",
                                 kwargs={"slug": self.bot.slug, "pk": self.post.id}))
        self.assertTemplateNotUsed(response)

    def test_view(self):
        send_time = time.time()
        c = Client()
        c.login(username="moderator", password="1234")
        posts = Post.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].send_time, None)
        response = c.put(
            reverse("bots-management:mailings:mailing-update",
                                 kwargs={"slug": self.bot.slug, "pk": self.post.id
                                         }),
            {"send_time": send_time}
        )
        posts = Post.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(response.status_code, 302)
