from datetime import datetime

from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.urls import reverse

from app_sportbar.models import MenuPosition, Category


class CartTest(TestCase):
    def test_cart_content_in_session(self):
        url = reverse("cart:cart")
        response = self.client.get(url)
        self.assertEqual(
            response.context["cart_instance"].cart,
            self.client.session.get(settings.CART_SESSION_ID),
        )


class CartAddTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product1 = MenuPosition.objects.create(
            title="Product 1", price=2.37, category=self.category
        )
        self.initial_url = reverse("sportbar:home")
        self.url1 = reverse(
            "cart:add-to-cart", kwargs={"id": self.product1.id}
        )
        self.product1_quantity = 1
        self.client.post(
            self.url1,
            {"quantity": self.product1_quantity, "update_quantity": False},
            HTTP_REFERER=self.initial_url,
        )

    def test_added_product_in_session(self):
        cart = (
            Session.objects.get().get_decoded().get(settings.CART_SESSION_ID)
        )
        cart_product1 = cart.get(str(self.product1.id))
        self.assertEqual(cart_product1["quantity"], self.product1_quantity)
        self.assertEqual(cart_product1["price"], str(self.product1.price))

    def test_added_another_product_to_existing_cart(self):
        product2 = MenuPosition.objects.create(
            title="Product 2", price=12.37, category=self.category
        )
        url2 = reverse("cart:add-to-cart", kwargs={"id": product2.id})
        self.client.post(
            url2,
            {"quantity": 7, "update_quantity": False},
            HTTP_REFERER=self.initial_url,
        )

        cart = (
            Session.objects.get().get_decoded().get(settings.CART_SESSION_ID)
        )
        cart_product1 = cart.get(str(self.product1.id))
        cart_product2 = cart.get(str(product2.id))
        self.assertEqual(cart_product1["quantity"], self.product1_quantity)
        self.assertEqual(cart_product1["price"], str(self.product1.price))
        self.assertEqual(cart_product2["quantity"], 7)
        self.assertEqual(cart_product2["price"], str(product2.price))

    def test_added_the_same_product_to_existing_cart(self):
        add_quantity = 12
        self.client.post(
            self.url1,
            {"quantity": add_quantity, "update_quantity": False},
            HTTP_REFERER=self.initial_url,
        )

        cart = (
            Session.objects.get().get_decoded().get(settings.CART_SESSION_ID)
        )
        cart_product1 = cart.get(str(self.product1.id))
        self.assertEqual(
            cart_product1["quantity"], self.product1_quantity + add_quantity
        )
        self.assertEqual(cart_product1["price"], str(self.product1.price))

    def test_update_quantity(self):
        new_quantity = 15
        self.client.post(
            self.url1,
            {"quantity": new_quantity, "update_quantity": True},
            HTTP_REFERER=self.initial_url,
        )

        cart = (
            Session.objects.get().get_decoded().get(settings.CART_SESSION_ID)
        )
        cart_product1 = cart.get(str(self.product1.id))
        self.assertEqual(
            cart_product1["quantity"], new_quantity
        )
