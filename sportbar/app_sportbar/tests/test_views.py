from datetime import datetime, timedelta
from pprint import pprint

from django.test import Client, TestCase
from django.urls import reverse

from app_sportbar.models import Championship

from app_sportbar.models import Category, Match

from app_cart.forms import CartAddProductForm


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
                event_date=datetime.now() + timedelta(days=7),
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
        response = self.client.get(reverse("sportbar:category", kwargs={"slug": obj.slug}))
        self.assertIsNotNone(response.context["cart_add_form"])
        self.assertIsInstance(response.context["cart_add_form"], CartAddProductForm)
