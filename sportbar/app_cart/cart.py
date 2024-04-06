from decimal import Decimal

from django.conf import settings

from app_sportbar.models import MenuPosition


class Cart:
    def __init__(self, request):
        """Creates an instance of the Cart class getting info from sessions
        or creates new empty session. cart example {'11': {'quantity': 2, 'price': '6.78'}}
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """adds a product to the cart or update the product quantity"""
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def __iter__(self):
        """Enable iteration over the cart({'11': {'quantity': 2, 'price': '6.78'}}) values
        and yields the dictionaries with added key
        {'quantity': 2, 'price': '6.78', 'product':'product', 'total_price': Decimal('26.78')}"""
        product_ids = self.cart.keys()
        products = MenuPosition.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_total_cost(self):
        """the cart total cost"""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def save(self):
        """Saves updated cart into session"""
        self.session[settings.CART_SESSION_ID] = self.cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        """returns number of products in cart"""
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
