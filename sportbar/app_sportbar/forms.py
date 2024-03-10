from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from app_sportbar.models import BookedTable


class ClientCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "avatar")


class BookedTableForm(forms.ModelForm):
    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="phone number should consists of 10 figures"
            )
        ]
    )

    class Meta:
        model = BookedTable
        fields = ["phone", "match", "client"]
        widgets = {"match": forms.HiddenInput(), "client": forms.HiddenInput()}
