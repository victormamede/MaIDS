import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT, MOCK_EQUIPMENT_TYPE, MOCK_EQUIPMENT_TYPE_2

from src.app.util.auth import Role

API_ROUTE = "/api/equipment/type"


class TestEquipmentType(AppTestCase):
    def setUp(self):
        super().setUp()

        self.client.post(
            API_ROUTE, data=MOCK_EQUIPMENT_TYPE, headers=self.master_header
        )

    def types_are_unique(self, client):
        resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT_TYPE)

        self.assertEqual(resp.status_code, 409)

    def creates_type(self, client):
        resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT_TYPE_2)

        self.mock_type_id = resp.get_json()["id"]

        self.assertEqual(resp.status_code, 201)

    def updates_type_info(self, client):
        update = {"description": "new_description"}

        resp = client.put(API_ROUTE + "/" + str(self.mock_type_id), data=update)
        self.assertEqual(resp.get_json()["description"], update["description"])

        # Set equipment type info back to original state
        resp = client.put(
            API_ROUTE + "/" + str(self.mock_type_id), data=MOCK_EQUIPMENT_TYPE_2
        )

    def cannot_delete_type_if_there_are_children(self, admin_client, regular_client):
        equipment = MOCK_EQUIPMENT.copy()
        equipment["type_id"] = self.mock_type_id

        # Create equipment that uses that type
        resp = admin_client.post("/api/equipment", data=equipment)

        resp2 = admin_client.delete(API_ROUTE + "/" + str(self.mock_type_id))

        self.assertEqual(resp2.status_code, 409)

        admin_client.delete("/api/equipment/" + str(resp.get_json()["id"]))

    def deletes_type(self, admin_client, regular_client):
        admin_client.delete(API_ROUTE + "/" + str(self.mock_type_id))

        resp = regular_client.get(API_ROUTE + "/" + str(self.mock_type_id))
        self.assertEqual(resp.status_code, 404)

    def gets_type(self, client):
        resp = client.get(API_ROUTE + "/" + str(self.mock_type_id))

        equip_type = MOCK_EQUIPMENT_TYPE_2.copy()
        equip_type["id"] = self.mock_type_id

        self.assertDictEqual(resp.get_json(), equip_type)

    def gets_type_list(self, client):
        resp = client.get(API_ROUTE)

        actual = resp.get_json()
        expected = [MOCK_EQUIPMENT_TYPE, MOCK_EQUIPMENT_TYPE_2]

        for i in range(len(expected)):
            # remove ids because they don't come with mock equipment data
            del actual[i]["id"]

            self.assertDictEqual(expected[i], actual[i])

    def test_equipment(self):
        with self.assertNeedsPermission(Role.EQUIPMENT) as client:
            self.creates_type(client)
            self.types_are_unique(client)
            self.updates_type_info(client)

            with self.mockUserClient([]) as regular_client:
                self.gets_type(regular_client)
                self.gets_type_list(regular_client)
                self.cannot_delete_type_if_there_are_children(client, regular_client)
                self.deletes_type(client, regular_client)
