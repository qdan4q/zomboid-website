from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import NewsArticle


class NewsVisibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.survivor = user_model.objects.create_user(
            username="survivor",
            password="test-password-123",
        )
        cls.staff = user_model.objects.create_user(
            username="administrator",
            password="test-password-123",
            is_staff=True,
        )
        cls.public_article = NewsArticle.objects.create(
            title="Public Water Advisory",
            summary="Boil all water taken from the river.",
            content="Public instructions for every survivor.",
            news_type=NewsArticle.NewsType.KNOX,
            visibility=NewsArticle.Visibility.SURVIVORS,
            author=cls.staff,
        )
        cls.hidden_article = NewsArticle.objects.create(
            title="Restricted KX-17 Findings",
            summary="Classified summary that must remain hidden.",
            content="Classified infected behavior observations.",
            news_type=NewsArticle.NewsType.SCIENTIFIC,
            visibility=NewsArticle.Visibility.ADMIN_ONLY,
            author=cls.staff,
        )

    def test_survivor_list_contains_public_article_but_no_hidden_data(self):
        self.client.force_login(self.survivor)

        response = self.client.get(reverse("news_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.public_article.title)
        self.assertNotContains(response, self.hidden_article.title)
        self.assertNotContains(response, self.hidden_article.summary)
        self.assertNotContains(response, self.hidden_article.content)
        self.assertNotIn(self.hidden_article, response.context["articles"])

    def test_hidden_article_direct_url_returns_404_for_survivor_and_visitor(self):
        detail_url = reverse("news_detail", args=[self.hidden_article.pk])

        self.assertEqual(self.client.get(detail_url).status_code, 404)
        self.client.force_login(self.survivor)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, self.hidden_article.content, status_code=404)

    def test_staff_can_view_hidden_article_and_sees_admin_label(self):
        self.client.force_login(self.staff)

        list_response = self.client.get(reverse("news_list"))
        detail_response = self.client.get(
            reverse("news_detail", args=[self.hidden_article.pk])
        )

        self.assertContains(list_response, self.hidden_article.title)
        self.assertContains(list_response, "ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ")
        self.assertContains(detail_response, self.hidden_article.content)
        self.assertContains(detail_response, "ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ")

    def test_survivor_cannot_access_news_management_views(self):
        self.client.force_login(self.survivor)
        protected_urls = [
            reverse("news_create"),
            reverse("news_manage"),
            reverse("news_edit", args=[self.public_article.pk]),
            reverse("news_delete", args=[self.public_article.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_staff_create_sets_logged_in_user_as_author(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("news_create"),
            {
                "title": "New Radio Intercept",
                "summary": "A short transmission crossed the emergency band.",
                "content": "The speaker warned listeners to avoid the northern road.",
                "news_type": NewsArticle.NewsType.RADIO,
                "visibility": NewsArticle.Visibility.ADMIN_ONLY,
                "in_game_date": "1993-07-18",
            },
        )

        article = NewsArticle.objects.get(title="New Radio Intercept")
        self.assertRedirects(response, article.get_absolute_url())
        self.assertEqual(article.author, self.staff)

    def test_staff_can_change_visibility_and_survivor_sees_article_immediately(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("news_edit", args=[self.hidden_article.pk]),
            {
                "title": self.hidden_article.title,
                "summary": self.hidden_article.summary,
                "content": self.hidden_article.content,
                "news_type": self.hidden_article.news_type,
                "visibility": NewsArticle.Visibility.SURVIVORS,
                "in_game_date": "",
            },
        )
        self.assertRedirects(response, self.hidden_article.get_absolute_url())
        self.hidden_article.refresh_from_db()
        self.assertEqual(
            self.hidden_article.visibility,
            NewsArticle.Visibility.SURVIVORS,
        )

        self.client.force_login(self.survivor)
        self.assertContains(self.client.get(reverse("news_list")), self.hidden_article.title)
        self.assertContains(
            self.client.get(self.hidden_article.get_absolute_url()),
            self.hidden_article.content,
        )

    def test_visibility_form_uses_two_clear_radio_choices(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse("news_create"))

        self.assertContains(response, 'type="radio"', count=2)
        self.assertContains(response, "Выжившие и администраторы")
        self.assertContains(response, "Только администраторы")
