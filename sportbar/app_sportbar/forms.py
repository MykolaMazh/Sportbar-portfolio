from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from app_sportbar.models import BookedTable


class ClientCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "avatar")


class BookTableForm(forms.ModelForm):
    class Meta:
        model = BookedTable
        fields = ['datatime_booked', 'phone']
        widgets = {
            'datatime_booked': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'phone': forms.NumberInput(attrs={'type': 'tel'})
        }
