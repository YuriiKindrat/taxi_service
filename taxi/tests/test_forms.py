from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number

class FormTests(TestCase):
    def test_license_vlaidation(self):

        with self.assertRaises(ValidationError):
            validate_license_number("AAa12345")
        with self.assertRaises(ValidationError):
            validate_license_number("AA12345")
        with self.assertRaises(ValidationError):
            validate_license_number("aaa12345")
        with self.assertRaises(ValidationError):
            validate_license_number("AAA1234")
        with self.assertRaises(ValidationError):
            validate_license_number("AAA1234a")
        with self.assertRaises(ValidationError):
            validate_license_number("AAA123456")
        self.assertTrue(validate_license_number("AAA12345"))

    def test_driver_creation_form(self):
        data = {"username": "test",
                "first_name": "test",
                "last_name": "test",
                "license_number": "GTR12345",
                "password1": "Test12345678",
                "password2": "Test12345678"}
        form = DriverCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
