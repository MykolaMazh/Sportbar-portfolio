from django.conf import settings
from django.db import models

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
        product_id = (product.id)

        # freeze the current price
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': (product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.session[settings.CART_SESSION_ID] = self.cart
