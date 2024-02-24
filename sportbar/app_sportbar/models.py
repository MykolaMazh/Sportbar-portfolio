from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
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
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

class Match(models.Model):
    title = models.CharField(max_length=250)
    championship = models.ForeignKey(
        "Championship",
        on_delete=models.CASCADE
    )
    event_date = models.DateTimeField()
    preview = models.TextField()
    poster = models.ImageField(upload_to='images/match_poster/%Y/%m/%d', max_length=100,
                              blank=True)

    def __str__(self):

        return f"{self.title} - {self.event_date.strftime('%M/%d %H:%M')}"


class Championship(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Client(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars/%Y/%m/%d', blank=True, null=True, max_length=250)

