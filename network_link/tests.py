from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network_link.models import ContactInfo, NetworkNode


class NetworkNodeModelTest(TestCase):
    """
    Тесты для модели NetworkNode.
    Проверяет вычисление уровня и валидацию поставщика.
    """

    def setUp(self):
        """
        Подготовка тестовых данных.
        Создаются уникальные контакты и звенья сети.
        """
        # Создаём уникальные контакты для каждого звена
        self.contact1 = ContactInfo.objects.create(
            email="factory@example.com",
            country="Russia",
            city="Moscow",
            street="Tverskaya",
            house_number="1",
        )
        self.contact2 = ContactInfo.objects.create(
            email="retailer@example.com",
            country="Russia",
            city="SPB",
            street="Nevsky",
            house_number="10",
        )
        self.contact3 = ContactInfo.objects.create(
            email="entrepreneur@example.com",
            country="Russia",
            city="Novosibirsk",
            street="Lenina",
            house_number="5",
        )
        self.factory = NetworkNode.objects.create(
            name="Factory", contact_info=self.contact1, debt=0.00
        )
        self.retailer = NetworkNode.objects.create(
            name="Retailer",
            contact_info=self.contact2,
            supplier=self.factory,
            debt=5000.00,
        )
        self.entrepreneur = NetworkNode.objects.create(
            name="Entrepreneur",
            contact_info=self.contact3,
            supplier=self.retailer,
            debt=1000.00,
        )

    def test_level_calculation(self):
        """
        Проверяет корректность вычисления уровня звена.
        """
        self.assertEqual(self.factory.get_level(), 0)
        self.assertEqual(self.retailer.get_level(), 1)
        self.assertEqual(self.entrepreneur.get_level(), 2)

    def test_supplier_cannot_be_self(self):
        """
        Проверяет, что звено не может быть поставщиком самого себя.
        """
        node = NetworkNode(name="SelfNode", contact_info=self.contact1, debt=0.00)
        node.supplier = node
        with self.assertRaises(ValidationError):
            node.full_clean()


class NetworkNodeAPITest(APITestCase):
    """
    Тесты для API NetworkNode.
    Проверяет создание, получение, фильтрацию и права доступа.
    """

    def setUp(self):
        """
        Подготовка тестового пользователя и начальных данных.
        """
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        contact = ContactInfo.objects.create(
            email="api@example.com",
            country="Russia",
            city="SPB",
            street="Nevsky",
            house_number="10",
        )
        self.factory = NetworkNode.objects.create(
            name="API Factory", contact_info=contact, debt=0.00
        )

    def test_create_node(self):
        """
        Проверяет создание нового звена через API.
        """
        url = reverse("networknode-list")
        data = {
            "name": "New Retailer",
            "contact_info": {
                "email": "new_api@example.com",
                "country": "Russia",
                "city": "SPB",
                "street": "Nevsky",
                "house_number": "10",
            },
            "debt": 1000.00,
        }
        response = self.client.post(url, data, format="json")
        if response.status_code != 201:
            print("Ошибки валидации:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 2)

    def test_get_node_list(self):
        """
        Проверяет получение списка звеньев.
        """
        url = reverse("networknode-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_user_cannot_access_api(self):
        """
        Проверяет, что неавторизованный пользователь не может получить доступ к API.
        """
        self.client.logout()
        url = reverse("networknode-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_country(self):
        """
        Проверяет фильтрацию звеньев по стране.
        """
        contact2 = ContactInfo.objects.create(
            email="foreign_api@example.com",
            country="USA",
            city="New York",
            street="5th Ave",
            house_number="1",
        )
        NetworkNode.objects.create(
            name="Foreign Factory", contact_info=contact2, debt=0.00
        )
        url = reverse("networknode-list") + "?contact_info__country=Russia"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "API Factory")


class NetworkNodeAdminTest(TestCase):
    """
    Тесты для админки NetworkNode.
    Проверяет действие 'сброс задолженности'.
    """

    def setUp(self):
        """
        Подготовка тестовых данных для админ-тестов.
        """
        contact = ContactInfo.objects.create(
            email="admin@example.com",
            country="Russia",
            city="Moscow",
            street="Tverskaya",
            house_number="1",
        )
        self.node = NetworkNode.objects.create(
            name="Test Node", contact_info=contact, debt=5000.00
        )

    def test_reset_debt_action(self):
        """
        Проверяет, что действие 'сброс задолженности' работает корректно.
        """
        from network_link.admin import NetworkNodeAdmin

        admin = NetworkNodeAdmin(NetworkNode, AdminSite())
        queryset = NetworkNode.objects.filter(id=self.node.id)

        admin.reset_debt_action(None, queryset)

        self.node.refresh_from_db()
        self.assertEqual(self.node.debt, 0.00)
