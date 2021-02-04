import unittest
from .config import AppTestCase
from .mocks import MOCK_USER, MOCK_USER_2
from src.app.util.auth import Role

API_ROUTE = "/api/user"


class TestUser(AppTestCase):
    def creates_user(self, client):
        resp = client.post(API_ROUTE, data=MOCK_USER)
        self.mock_user_id = resp.get_json()["id"]

        self.assertEqual(MOCK_USER["username"], resp.get_json()["username"])

    def user_cant_have_same_data(self, client):
        resp = client.post(API_ROUTE, data=MOCK_USER)

        self.assertEqual(resp.status_code, 409)

    def gets_all_users(self, client):
        resp = client.get(API_ROUTE)

        self.assertIn(
            MOCK_USER["username"], [user["username"] for user in resp.get_json()]
        )

    def gets_user_with_id(self, client):
        resp = client.get(API_ROUTE + "/" + str(self.mock_user_id))

        self.assertEqual(MOCK_USER["username"], resp.get_json()["username"])

    def changes_user(self, client):
        to_change = {"username": "changeduser"}

        resp = client.put(API_ROUTE + "/" + str(self.mock_user_id), data=to_change)
        json = resp.get_json()

        self.assertEqual(to_change["username"], json["username"])

    def changes_roles(self, client):
        to_change = {"roles": ["EQUIPMENT"]}

        resp = client.put(API_ROUTE + "/" + str(self.mock_user_id), data=to_change)
        json = resp.get_json()

        self.assertEqual(to_change["roles"], json["roles"])

        resp = client.put(API_ROUTE + "/" + str(self.mock_user_id), data={})
        json = resp.get_json()

        self.assertEqual(to_change["roles"], json["roles"])

        to_change = {"roles": ["NONE"]}

        resp = client.put(API_ROUTE + "/" + str(self.mock_user_id), data=to_change)
        json = resp.get_json()

        self.assertEqual([], json["roles"])

    def deletes_user(self, client):
        resp = client.delete(API_ROUTE + "/" + str(self.mock_user_id))

        self.assertEqual(resp.status_code, 200)

        resp = client.get(API_ROUTE + "/" + str(self.mock_user_id))

        self.assertEqual(resp.status_code, 404)

    def filters_user_list(self, client):
        # new user
        resp = client.post(API_ROUTE, data=MOCK_USER_2)
        new_user_id = resp.get_json()["id"]

        resp = client.get(API_ROUTE, query_string={"username": MOCK_USER_2["username"]})
        actual = resp.get_json()[0]

        self.assertEqual(actual["id"], new_user_id)

    def test_user(self):
        with self.assertNeedsPermission(Role.ACCOUNTS) as client:
            self.creates_user(client)
            self.user_cant_have_same_data(client)
            self.gets_all_users(client)
            self.gets_user_with_id(client)
            self.changes_user(client)
            self.changes_roles(client)
            self.deletes_user(client)
            self.filters_user_list(client)


if __name__ == "__main__":
    unittest.main()
