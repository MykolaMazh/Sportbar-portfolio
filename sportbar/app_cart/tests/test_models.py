from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from app_cart.models import OrderItem, Order
from app_sportbar.models import MenuPosition, Category


class OrderTest(TestCase):
    def test_get_total_cost(self):
        user = get_user_model().objects.create_user(
            username="user", password="qwerty123456"
        )
        order = Order.objects.create(
            client=user, phone="1234567890", address="test address"
        )
        category = Category.objects.create(
            title="test category", slug="test-category"
        )
        for num in range(1, 21):
            product = MenuPosition.objects.create(
                title=f"test menu position{num}",
                price=num / 2 + 0.33,
                category=category,
            )
            OrderItem.objects.create(
                order=order, product=product, price=product.price, quantity=num
            )

            self.assertEqual(
                order.get_total_cost(),
                sum(
                    (
                        num * Decimal(f"{round(num / 2 + 0.33, 2)}")
                        for num in range(1, 21)
                    )
                ),
            )
