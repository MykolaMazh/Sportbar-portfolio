from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, MenuPosition


class CategoryTest(TestCase):
    def setUp(self):
        self.obj = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )

    def test_str(self):
        self.assertEqual(str(self.obj), self.obj.title)

    def test_get_absolute_url(self):
        self.assertEqual(
            reverse(
                "app_sportbar:category",
                kwargs={"slug": self.obj.slug}
            ), self.obj.get_absolute_url())

class MenuPositionTest(TestCase):
    def test_str(self):
        category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
        obj = MenuPosition.objects.create(
            title='Test MenuPosition',
            price=Decimal('100.22'),
            category=category
        )
        self.assertEqual(str(obj), obj.title)
