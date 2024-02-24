from django.shortcuts import render, get_object_or_404

from app_cart.forms import CartAddProductForm
from app_cart.models import Cart
from app_sportbar.models import MenuPosition



def cart_add(request, slug):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(
            product=MenuPosition.objects.get(slug=slug),
            **form.cleaned_data)





