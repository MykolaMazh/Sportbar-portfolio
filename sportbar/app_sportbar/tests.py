from django.test import TestCase
from django.urls import reverse

from .models import Category


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
