from django.db import models
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/%Y/%m/%d', max_length=100,
                              blank=True)
    description = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class MenuPosition(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_positions")
    image = models.ImageField(upload_to='images/%Y/%m/%d', max_length=100,
                              blank=True)

    def __str__(self):
        return self.title