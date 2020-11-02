import unittest
from .config import AppTestCase
from .mocks import MOCK_USER

API_ROUTE = '/api/user'

class TestUser(AppTestCase):
  def creates_user(self):
    resp = self.client.post(API_ROUTE, data=MOCK_USER, headers=self.master_header)
    self.mock_user_id = resp.get_json()['id']

    self.assertEqual(MOCK_USER['username'], resp.get_json()['username'])

  def user_cant_have_same_data(self):
    resp = self.client.post(API_ROUTE, data=MOCK_USER, headers=self.master_header)

    self.assertEqual(resp.status_code, 409)


  def gets_all_users(self):
    resp = self.client.get(API_ROUTE, headers=self.master_header)

    self.assertIn(MOCK_USER['username'], [user['username'] for user in resp.get_json()])

  def gets_user_with_id(self):
    resp = self.client.get(API_ROUTE + '/' + str(self.mock_user_id), headers=self.master_header)
    
    self.assertEqual(MOCK_USER['username'], resp.get_json()['username'])

  def changes_user(self):
    to_change = { 'username': 'changeduser' }

    resp = self.client.put(API_ROUTE + '/' + str(self.mock_user_id), data=to_change, headers=self.master_header)

    self.assertEqual(to_change['username'], resp.get_json()['username'])

  def deletes_user(self):
    resp = self.client.delete(API_ROUTE + '/' + str(self.mock_user_id), headers=self.master_header)

    self.assertEqual(resp.status_code, 200)

    resp = self.client.get(API_ROUTE + '/' + str(self.mock_user_id), headers=self.master_header)

    self.assertEqual(resp.status_code, 404)

  def test_user(self):
    self.creates_user()
    self.user_cant_have_same_data()
    self.gets_all_users()
    self.gets_user_with_id()
    self.changes_user()
    self.deletes_user()



if __name__ == '__main__':
  unittest.main()