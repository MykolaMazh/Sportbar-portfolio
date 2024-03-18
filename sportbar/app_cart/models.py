from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from app_sportbar.models import MenuPosition


class Order(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    phone = models.TextField(
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="phone number should consists of 10 figures",
            )
        ]
    )
    address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    deliver_by = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    # total order cost with get_cost() from related Model OrderItem
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

    def __str__(self):
        return "Order {}".format(self.id)

    class Meta:
        ordering = ("-created_at",)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        MenuPosition,
        related_name="products_in_order",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{}".format(self.id)

    def get_cost(self):
        return self.price * self.quantity
