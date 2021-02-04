import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT_TYPE, MOCK_EQUIPMENT, MOCK_USER, MOCK_PASSWORD

from src.app.util.auth import Role

API_ROUTE = "/api/equipment/1/passwords"


class TestEquipment(AppTestCase):
    def setUp(self):
        super().setUp()

        resp = self.client.post(
            "/api/equipment/type", data=MOCK_EQUIPMENT_TYPE, headers=self.master_header
        )
        resp = self.client.post(
            "/api/equipment", data=MOCK_EQUIPMENT, headers=self.master_header
        )

        self.mock_equipment = resp.get_json()

    def creates_password(self, client):
        resp = client.post(API_ROUTE, data=MOCK_PASSWORD)

        resp_data = resp.get_json()
        self.mock_password_id = resp_data["id"]
        del resp_data["id"]

        expected = MOCK_PASSWORD.copy()

        self.assertDictEqual(resp_data, expected)

    def test_password(self):
        with self.assertNeedsPermission(Role.PASSWORDS) as client:
            self.creates_password(client)
