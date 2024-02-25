from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from app_cart.forms import CartAddProductForm
from app_cart.models import Cart
from app_sportbar.models import MenuPosition


def cart(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart_instance":cart})


def cart_add(request, id):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(
            product=MenuPosition.objects.get(pk=id),
            **form.cleaned_data)
        print(cart.cart)
        for item in cart.cart.values():
            print(item)
        return redirect(request.META.get('HTTP_REFERER'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(MenuPosition, id=product_id)
    cart.remove(product)
    return redirect('cart:cart')





