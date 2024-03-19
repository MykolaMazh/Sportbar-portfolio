from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_sportbar.models import Championship, Category, Match, BookedTable
from app_cart.forms import CartAddProductForm
from app_sportbar.forms import BookedTableForm





class TestIndex(TestCase):
    def setUp(self) -> None:
        self.url = reverse("sportbar:home")

    def test_index_context_contain_all(self):
        for num in range(10):
            Championship.objects.create(title=f"Test championship{num}")
            Category.objects.create(
                title=f"Test category{num}", slug=f"test-category{num}"
            )
            Match.objects.create(
                title=f"Test match{num}",
                championship=Championship.objects.get(pk=1),
                event_date=timezone.now() + timedelta(days=7),
            )
        response = self.client.get(self.url)
        self.assertEqual(response.context["championships"].count(), 10)
        self.assertEqual(response.context["categories"].count(), 10)
        self.assertEqual(response.context["matches"].count(), 10)


class CategoryDetailViewTest(TestCase):
    def test_cart_add_form_in_context(self):
        obj = Category.objects.create(
            title="Test category", slug="test-category"
        )
        response = self.client.get(
            reverse("sportbar:category", kwargs={"slug": obj.slug})
        )
        self.assertIsNotNone(response.context["cart_add_form"])
        self.assertIsInstance(
            response.context["cart_add_form"], CartAddProductForm
        )


class BookedTableCreateViewTest(TestCase):
    def setUp(self):
        championship = Championship.objects.create(title="Test championship")
        self.match = Match.objects.create(
            title="Test match",
            championship=championship,
            event_date=timezone.now(),
        )
        self.url = reverse(
            "sportbar:booked-table", kwargs={"match_id": self.match.pk}
        )

    def test_authentication_required(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_form_is_custom_with_initial_data(self):
        user = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456"
        )
        self.client.force_login(user)

        response = self.client.get(self.url)

        self.assertEqual(response.context["form"].data["match"], self.match.pk)
        self.assertIsInstance(response.context["form"], BookedTableForm)

    def test_no_form_and_error_in_context_if_all_booked(self):
        for num in range(settings.MAX_BAR_CAPACITY):
            user = get_user_model().objects.create_user(
                username=f"user{num}", password="qwerty123456"
            )
            self.client.force_login(user)
            BookedTable.objects.create(match=self.match,
                                       client=user, phone="1234567890")
        user = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456"
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"], "")
        self.assertIn("excess_error",  response.context)
