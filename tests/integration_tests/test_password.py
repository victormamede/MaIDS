import unittest

from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT_TYPE, MOCK_EQUIPMENT, MOCK_USER, MOCK_PASSWORD

from src.app.util.auth import Role

API_ROUTE = "/api/password"
API_EQUIP_ROUTE = "/api/equipment/1/password"

MOCK_LEVEL_PASSWORD = MOCK_PASSWORD.copy()
MOCK_LEVEL_PASSWORD["level"] = 5

MOCK_USER_PASSWORD = MOCK_PASSWORD.copy()


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

    def creates_level_password(self, client):
        resp = client.post(API_EQUIP_ROUTE + "/level", data=MOCK_LEVEL_PASSWORD)

        resp_data = resp.get_json()
        self.mock_level_password_id = resp_data["id"]
        del resp_data["id"]

        expected = MOCK_LEVEL_PASSWORD.copy()
        expected["equipment"] = self.mock_equipment

        self.assertDictEqual(resp_data, expected)

    def gets_password(self, client):
        resp = client.get(API_EQUIP_ROUTE)

        expected_level = MOCK_LEVEL_PASSWORD.copy()
        expected_level["equipment"] = self.mock_equipment
        expected_level["id"] = 1

        expected_user = MOCK_USER_PASSWORD.copy()
        del expected_user["user_id"]
        expected_user["equipment"] = self.mock_equipment
        expected_user["user"] = client.user_data
        expected_user["id"] = 2

        actual = resp.get_json()

        self.assertDictEqual(expected_user, actual[0])
        self.assertDictEqual(expected_level, actual[1])

    def gets_password_by_id(self, level_client, user_client):
        level_resp = level_client.get(f"{API_ROUTE}/{self.mock_user_password_id}")
        user_resp = user_client.get(f"{API_ROUTE}/{self.mock_user_password_id}")

        expected = MOCK_USER_PASSWORD.copy()
        del expected["user_id"]
        expected["equipment"] = self.mock_equipment
        expected["user"] = user_client.user_data
        expected["id"] = 2

        level_actual = level_resp.get_json()
        user_actual = user_resp.get_json()

        self.assertDictEqual(level_actual, user_actual)
        self.assertDictEqual(expected, level_actual)

    def cannot_get_others_password_by_id(self, client):
        resp = client.get(f"{API_ROUTE}/{self.mock_user_password_id}")

        self.assertEqual(resp.status_code, 401)

    def creates_user_password(self, admin_client, client):
        MOCK_USER_PASSWORD["user_id"] = client.user_data["id"]

        resp = admin_client.post(API_EQUIP_ROUTE + "/user", data=MOCK_USER_PASSWORD)

        resp_data = resp.get_json()
        self.mock_user_password_id = resp_data["id"]
        del resp_data["id"]

        expected = MOCK_USER_PASSWORD.copy()
        del expected["user_id"]
        expected["equipment"] = self.mock_equipment
        expected["user"] = client.user_data

        self.assertDictEqual(resp_data, expected)

    def can_update_my_password(self, client):
        update = {"password": "new_password"}

        resp = client.put(f"{API_ROUTE}/{self.mock_user_password_id}", data=update)

        self.assertEqual(resp.status_code, 200)

        resp = client.get(f"{API_ROUTE}/{self.mock_user_password_id}")

        self.assertEqual(resp.get_json()["password"], update["password"])

    def cannot_update_others_password(self, client):
        update = {"password": "new_password"}

        resp = client.put(f"{API_ROUTE}/{self.mock_user_password_id}", data=update)

        self.assertEqual(resp.status_code, 401)

    def deletes_password(self, client):
        resp = client.delete(f"{API_ROUTE}/{self.mock_level_password_id}")

        self.assertEqual(resp.status_code, 200)

        client.disable_checking()
        resp = client.get(f"{API_ROUTE}/{self.mock_level_password_id}")

        self.assertEqual(resp.status_code, 404)
        client.enable_checking()

    def test_password(self):
        with self.assertNeedsPermission(Role.PASSWORDS) as client:
            self.creates_level_password(client)

            with self.mockUserClient([]) as regular_client:
                self.creates_user_password(client, regular_client)

                self.gets_password(regular_client)
                self.gets_password_by_id(client, regular_client)
                self.can_update_my_password(regular_client)

                self.deletes_password(client)

        with self.mockUserClient([]) as third_party:
            self.cannot_get_others_password_by_id(third_party)
            self.cannot_update_others_password(third_party)
