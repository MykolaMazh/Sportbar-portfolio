from decimal import Decimal

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from app_sportbar.models import MenuPosition


class Cart:

    def __init__(self, request):
        # current session
        self.session = request.session

        # session cart
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        # freeze the current price
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()


    def __iter__(self):
        product_ids = self.cart.keys()
        # getting products from model
        products = MenuPosition.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_cost(self):
    # the cart total cost
        return sum(Decimal(item['price']) * item['quantity'] for item in
               self.cart.values())

    def save(self):
        # update session. it's a dict now
        self.session[settings.CART_SESSION_ID] = self.cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # delete the cart from session
        del self.session[settings.CART_SESSION_ID]


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    phone = models.TextField(validators=[RegexValidator(
        regex=r'^\d{10}$',
        message="phone number should consists of 10 figures")
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
        return 'Order {}'.format(self.id)

    class Meta:
        ordering = ('-created_at',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(MenuPosition, related_name='products_in_order', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity





