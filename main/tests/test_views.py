from django.test import TestCase


class ListViewTest(TestCase):
    """Тесты запросов для ListView объявлений"""
    def test_cars(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_things(self):
        response = self.client.get("/things/")
        self.assertEqual(response.status_code, 200)

    def test_services(self):
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 200)
