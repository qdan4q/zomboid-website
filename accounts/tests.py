from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


User = get_user_model()


class AccountTests(TestCase):
    def setUp(self):
        self.survivor = User.objects.create_user(
            username="rosewood",
            password="safe-test-password",
        )
        self.admin = User.objects.create_user(
            username="relay_admin",
            password="safe-test-password",
            is_staff=True,
        )

    def test_profile_is_created_with_user(self):
        self.assertTrue(UserProfile.objects.filter(user=self.survivor).exists())

    def test_survivor_can_log_in(self):
        response = self.client.post(
            reverse("login"),
            {"username": "rosewood", "password": "safe-test-password"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_survivor_cannot_change_status(self):
        self.client.force_login(self.survivor)
        response = self.client.post(
            reverse("profile_edit"),
            {
                "character_name": "Scout",
                "biography": "Keeps watch near the relay.",
                "occupation": "Park ranger",
                "status": UserProfile.Status.DEAD,
            },
        )
        self.assertRedirects(response, reverse("profile"))
        self.survivor.profile.refresh_from_db()
        self.assertEqual(self.survivor.profile.character_name, "Scout")
        self.assertEqual(self.survivor.profile.status, UserProfile.Status.UNKNOWN)

    def test_survivor_cannot_access_control_panel_or_user_management(self):
        self.client.force_login(self.survivor)
        self.assertEqual(self.client.get(reverse("control_panel")).status_code, 403)
        self.assertEqual(self.client.get(reverse("user_manage")).status_code, 403)

    def test_staff_can_edit_user_profile_and_administrator_flag(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("user_edit", args=[self.survivor.pk]),
            {
                "username": self.survivor.username,
                "email": "survivor@example.test",
                "is_active": "on",
                "is_staff": "on",
                "character_name": "Doctor Greene",
                "biography": "Runs the improvised clinic.",
                "occupation": "Doctor",
                "status": UserProfile.Status.INJURED,
            },
        )
        self.assertRedirects(response, reverse("user_manage"))
        self.survivor.refresh_from_db()
        self.survivor.profile.refresh_from_db()
        self.assertTrue(self.survivor.is_staff)
        self.assertEqual(self.survivor.profile.status, UserProfile.Status.INJURED)
