import re
from html.parser import HTMLParser
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class ControlPanelTests(TestCase):
    def setUp(self):
        self.survivor = get_user_model().objects.create_user(
            username="survivor", password="test-pass-123"
        )
        self.admin = get_user_model().objects.create_user(
            username="operator", password="test-pass-123", is_staff=True
        )

    def test_survivor_cannot_access_control_panel(self):
        self.client.force_login(self.survivor)
        response = self.client.get(reverse("control_panel"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_access_control_panel(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("control_panel"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("control_panel"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('control_panel')}")


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


class RussianInterfaceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        output = StringIO()
        call_command("seed_demo_data", stdout=output)
        cls.admin = get_user_model().objects.get(username="администратор")

    def assert_no_english_visible_text(self, response):
        self.assertEqual(response.status_code, 200)
        parser = VisibleTextParser()
        parser.feed(response.content.decode("utf-8"))
        visible_text = " ".join(parser.parts)
        english_words = sorted(set(re.findall(r"[A-Za-z]{2,}", visible_text)))
        self.assertEqual(english_words, [], visible_text)

    def test_public_pages_have_only_russian_visible_text(self):
        for url_name in ["home", "news_list", "listing_list", "login"]:
            with self.subTest(url_name=url_name):
                self.assert_no_english_visible_text(self.client.get(reverse(url_name)))

    def test_administrator_pages_have_only_russian_visible_text(self):
        self.client.force_login(self.admin)
        urls = [
            reverse("profile"),
            reverse("control_panel"),
            reverse("site_settings_edit"),
            reverse("user_manage"),
            reverse("user_create"),
            reverse("news_manage"),
            reverse("news_create"),
            reverse("listing_manage"),
            reverse("admin:index"),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assert_no_english_visible_text(self.client.get(url))
