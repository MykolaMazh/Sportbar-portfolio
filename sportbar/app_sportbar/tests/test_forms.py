from django.test import TestCase

from app_sportbar.forms import ClientCreationForm


class ClientCreationFormTest(TestCase):
    def test_form_is_valid_without_avatar(self):
        form_data = {
            "username": "test_user",
            "password1": "qazwsxddf6577",
            "password2": "qazwsxddf6577",
        }
        form = ClientCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
