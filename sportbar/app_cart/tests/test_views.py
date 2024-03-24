from datetime import datetime, timedelta
import datetime as dt

from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.urls import reverse

from app_sportbar.models import MenuPosition, Category
from app_cart.models import Order


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

class CartRemoveTest(TestCase):

    def setUp(self):
        session = self.client.session
        session[settings.CART_SESSION_ID] = {'1': {'quantity': 12, 'price': '2.37'}, '2': {'quantity': 7, 'price': '12.37'}}
        session.save()

    def test_product_deleted_from_session(self):
        category = Category.objects.create(
                title="Test Category", slug="test-category"
            )
        product = MenuPosition.objects.create(
                title="Product 1", price=2.37, category=category
            )
        product_id = product.id
        url = reverse("cart:move-off-cart", args=[product_id])
        self.client.get(url)
        cart = (
            Session.objects.get().get_decoded().get(settings.CART_SESSION_ID)
        )
        self.assertNotIn(str(product_id), cart)



class CreateOrderTest(TestCase):
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
        self.client.post(
            self.url1,
            {"quantity": 12, "update_quantity": False},
            HTTP_REFERER=self.initial_url,
        )
        self.product2 = MenuPosition.objects.create(
            title="Product 2", price=12.37, category=self.category
        )
        url2 = reverse("cart:add-to-cart", kwargs={"id": self.product2.id})
        self.client.post(
            url2,
            {"quantity": 7, "update_quantity": False},
            HTTP_REFERER=self.initial_url,
        )

    def test_post_clear_session(self):
        url = reverse("cart:order-form")
        response = self.client.post(url, {
            "deliver_by": datetime.now() + timedelta(weeks=1),
            "address": "test address",
            "phone": 1234567890
        })
        self.assertRaises(KeyError, lambda: self.client.session[settings.CART_SESSION_ID])

    def test_post_create_order(self):
        url = reverse("cart:order-form")
        deliver_by = datetime.now(tz=dt.timezone.utc) + timedelta(weeks=1)
        address = "test address"
        phone = 1234567890
        response = self.client.post(url, {
            "deliver_by": deliver_by,
            "address": address,
            "phone": phone
        })
        order = Order.objects.get()
        self.assertEqual(order.deliver_by, deliver_by)
        self.assertEqual(order.address, address)
        self.assertEqual(order.phone, str(phone))