from django import forms
from django.core.validators import RegexValidator

from app_cart.models import Order


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"style": "width:10%"}))
    update_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    phone = forms.CharField(validators=[RegexValidator(
        regex=r'^\d{10}$',
        message="phone number should consists of 10 figures")
    ])
    class Meta:
        model = Order
        fields = ("deliver_by",'address', "phone")
        widgets = {
            "deliver_by": forms.DateTimeInput(attrs={"type":"datetime-local"})
        }