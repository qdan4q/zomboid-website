from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import MarketplaceListing


class MarketplacePermissionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user("owner", password="test-pass-123")
        self.other = user_model.objects.create_user("other", password="test-pass-123")
        self.staff = user_model.objects.create_user(
            "staff", password="test-pass-123", is_staff=True
        )
        self.listing = MarketplaceListing.objects.create(
            title="Spare axe",
            description="Still sharp enough for chopping.",
            category=MarketplaceListing.Category.FOR_SALE,
            author=self.owner,
            character_name="Mara Pike",
            price_or_trade="Two cans of food",
            meeting_location="Relay tower K-12",
            contact_information="Leave a note at the tower",
        )

    def listing_data(self, **overrides):
        data = {
            "title": "Working radio",
            "description": "Battery powered and tested yesterday.",
            "category": MarketplaceListing.Category.TRADE,
            "character_name": "Mara Pike",
            "price_or_trade": "Medicine",
            "meeting_location": "Old gas station",
            "contact_information": "Channel 8 after dark",
        }
        data.update(overrides)
        return data

    def test_survivor_can_create_listing(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("listing_create"), self.listing_data())

        created = MarketplaceListing.objects.get(title="Working radio")
        self.assertRedirects(response, created.get_absolute_url())
        self.assertEqual(created.author, self.owner)
        self.assertEqual(created.status, MarketplaceListing.Status.ACTIVE)

    def test_survivor_can_edit_own_listing(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("listing_edit", args=[self.listing.pk]),
            self.listing_data(title="Sharpened spare axe"),
        )

        self.assertRedirects(response, self.listing.get_absolute_url())
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, "Sharpened spare axe")

    def test_survivor_cannot_edit_another_users_listing(self):
        self.client.force_login(self.other)

        response = self.client.post(
            reverse("listing_edit", args=[self.listing.pk]),
            self.listing_data(title="Stolen listing"),
        )

        self.assertEqual(response.status_code, 403)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, "Spare axe")

    def test_staff_can_edit_any_listing(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("listing_edit", args=[self.listing.pk]),
            self.listing_data(
                title="Closed by staff",
                status=MarketplaceListing.Status.CLOSED,
            ),
        )

        self.assertRedirects(response, reverse("listing_manage"))
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, "Closed by staff")
        self.assertEqual(self.listing.status, MarketplaceListing.Status.CLOSED)

    def test_staff_can_delete_any_listing(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse("listing_delete", args=[self.listing.pk]))

        self.assertRedirects(response, reverse("listing_manage"))
        self.assertFalse(MarketplaceListing.objects.filter(pk=self.listing.pk).exists())

    def test_only_active_listings_are_public(self):
        self.listing.status = MarketplaceListing.Status.SOLD
        self.listing.save()

        list_response = self.client.get(reverse("listing_list"))
        detail_response = self.client.get(
            reverse("listing_detail", args=[self.listing.pk])
        )

        self.assertNotContains(list_response, self.listing.title)
        self.assertEqual(detail_response.status_code, 404)

    def test_owner_and_staff_can_view_inactive_listing(self):
        self.listing.status = MarketplaceListing.Status.SOLD
        self.listing.save()

        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("listing_detail", args=[self.listing.pk])).status_code,
            200,
        )
        self.client.force_login(self.staff)
        self.assertEqual(
            self.client.get(reverse("listing_detail", args=[self.listing.pk])).status_code,
            200,
        )

    def test_owner_can_mark_listing_sold(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("listing_mark_sold", args=[self.listing.pk])
        )

        self.assertRedirects(response, reverse("listing_list"))
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, MarketplaceListing.Status.SOLD)
