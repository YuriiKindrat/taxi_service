from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def test_str_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test1")

        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_str_driver(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345678",
            first_name="Test",
            last_name="Test",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_str_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test1")

        car = Car.objects.create(model="test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_license_number_of_driver(self):
        license_number = "GHT12345"
        driver = Driver.objects.create(
            username="test",
            password="test12345678",
            license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)


