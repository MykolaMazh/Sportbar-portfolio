from django import forms

from app_cart.models import Order


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    update_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', "phone")