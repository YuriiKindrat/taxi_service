from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

INDEX_URL = reverse("taxi:index")

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CAR_CREATE_URL = reverse("taxi:car-create")
CAR_LIST_URL = reverse("taxi:car-list")

DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_index_page(self):
        res = self.client.get(INDEX_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturers(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_cars(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateIndexViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_index_page(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(
            name="testmodel",
            country="testcountry"
        )
        Manufacturer.objects.create(
            name="testmodel1",
            country="testcountry1"
        )

        res = self.client.get(MANUFACTURER_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(manufacturers),
            list(res.context["manufacturer_list"])
        )
        self.assertTemplateUsed("taxi/manufacturer_list.html")

    def test_manufacturer_create_view(self):

        self.client.post(path=MANUFACTURER_CREATE_URL, data={"name": "testmodel",
                                                             "country": "testcountry"})
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(len(manufacturers), 1)

    def test_manufacturer_delete_view(self):

        manufacturer = Manufacturer.objects.create(name="testmodel",
                                                   country="testcountry")
        self.client.post(path=reverse("taxi:manufacturer-delete", args=[manufacturer.id]))

        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(len(manufacturers), 0)

    def test_manufacturer_update_view(self):
        manufacturer = Manufacturer.objects.create(name="testmodel", country="testcountry")
        self.client.post(path=reverse("taxi:manufacturer-update",
                                      args=[manufacturer.id]),
                         data={"name": "test", "country": "test"})
        manufacturer = Manufacturer.objects.get(id=manufacturer.id)
        self.assertEqual(manufacturer.name, "test")


class PrivateDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="GTR12345"
        )

        res = self.client.get(DRIVER_LIST_URL)

        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(drivers),
            list(res.context["driver_list"])
        )
        self.assertTemplateUsed("taxi/driver_list.html")

    def test_driver_create_view(self):

        self.client.post(path=DRIVER_CREATE_URL, data={"username": "testuser",
                                                       "first_name": "test",
                                                       "last_name": "test1",
                                                       "license_number": "GTR45632",
                                                       "password1": "Test12345678",
                                                       "password2": "Test12345678",
                                                       })
        drivers = list(Driver.objects.all())
        self.assertEqual(len(drivers), 2)

    def test_driver_delete_view(self):

        driver = get_user_model().objects.create_user(username="testmodel",
                                                      password="testpassword",
                                                      license_number="GTE12354")
        self.client.post(path=reverse("taxi:driver-delete", args=[driver.id]))

        drivers = list(Manufacturer.objects.all())
        self.assertEqual(len(drivers), 0)

    def test_license_update_view(self):
        driver = get_user_model().objects.create_user(username="testmodel",
                                                      password="testpassword",
                                                      license_number="GTE12354")
        self.client.post(path=reverse("taxi:license-update",
                                      args=[driver.id]),
                         data={"license_number": "AAA12345"})
        driver = Driver.objects.get(id=driver.id)
        self.assertEqual(driver.license_number, "AAA12345")


class PrivateCarViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.user)

    def test_car_list_view(self):
        manufacturer = Manufacturer.objects.create(name="testmodel",
                                                   country="testcountry")
        user = self.user
        car = Car.objects.create(model="test",
                                 manufacturer=manufacturer)
        car.drivers.add(user)

        res = self.client.get(CAR_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(cars),
            list(res.context["car_list"])
        )
        self.assertTemplateUsed("taxi/car_list.html")

    def test_car_create_view(self):
        Manufacturer.objects.create(name="testmodel",
                                                   country="testcountry")

        self.client.post(path=CAR_CREATE_URL, data={"model": "test",
                                                    "manufacturer": "1",
                                                    "drivers": "1"})
        cars = list(Car.objects.all())
        self.assertEqual(len(cars), 1)

    def test_car_delete_view(self):
        manufacturer = Manufacturer.objects.create(name="testmodel",
                                                   country="testcountry")
        user = self.user
        car = Car.objects.create(model="test",
                                 manufacturer=manufacturer)
        car.drivers.add(user)

        self.client.post(path=reverse("taxi:car-delete", args=[car.id]))

        cars = list(Car.objects.all())
        self.assertEqual(len(cars), 0)

    def test_car_update_view(self):
        manufacturer = Manufacturer.objects.create(name="testmodel",
                                                   country="testcountry")
        user = self.user
        car = Car.objects.create(model="test",
                                 manufacturer=manufacturer)
        car.drivers.add(user)

        self.client.post(path=reverse("taxi:car-update",
                                      args=[car.id]),
                         data={"model": "dfg", "manufacturer": "1", "drivers": "1"})
        car = Car.objects.get(id=car.id)
        self.assertEqual(car.model, "dfg")
