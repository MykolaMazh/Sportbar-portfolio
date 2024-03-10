from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from app_cart.forms import CartAddProductForm, OrderForm
from app_cart.models import Cart, OrderItem, Order
from app_sportbar.models import MenuPosition


def cart(request):
    cart = Cart(request)
    return render(
        request,
        "cart/cart.html",
        {
            "cart_instance": cart,
        },
    )


def cart_add(request, id):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(product=MenuPosition.objects.get(pk=id), **form.cleaned_data)
        return redirect(request.META.get("HTTP_REFERER"))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(MenuPosition, id=product_id)
    cart.remove(product)
    return redirect("cart:cart")


class CreateOrder(View):
    def get(self, request):
        order_form = OrderForm()
        return render(
            request,
            "cart/order_form.html",
            {"order_form": order_form}
        )

    def post(self, request):
        order_form = OrderForm(request.POST)
        cart_instance = Cart(request)
        if order_form.is_valid():
            if len(cart_instance) > 0:
                if request.user.is_authenticated:
                    order = order_form.save(commit=False)
                    order.client = request.user
                    order.save()
                else:
                    order = order_form.save()
            for item in cart_instance:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart_instance.clear()
        return render(
            request,
            "cart/order_form.html",
            {"order_form": order_form}
        )


class OrdersList(LoginRequiredMixin, ListView):
    model = Order
    template_name = "cart/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).prefetch_related(
            "order_items__product"
        )
