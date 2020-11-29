import unittest
from .config import AppTestCase
from .mocks import MOCK_USER, MOCK_LOGIN, MOCK_USER_NO_PERM, MOCK_LOGIN_NO_PERM

API_ROUTE = '/api/auth'

class TestAuth(AppTestCase):
  def setUp(self):
    super().setUp()

    self.client.post('/api/user', data=MOCK_USER, headers=self.master_header)
    self.client.post('/api/user', data=MOCK_USER_NO_PERM, headers=self.master_header)

  def can_authenticate(self):
    resp = self.client.post(API_ROUTE, data=MOCK_LOGIN)
    self.user_header = resp.get_json()

    resp = self.client.post(API_ROUTE, data=MOCK_LOGIN_NO_PERM)
    self.user_header_no_perm = resp.get_json()

    self.assertEqual(resp.status_code, 200)

  def checks_for_permission(self):
    pass

  def cannot_auth_with_wrong_credentials(self):
    WRONG_CREDENTIALS = {
      'username': MOCK_USER['username'],
      'password': 'wrong_password'
    }

    resp = self.client.post(API_ROUTE, data=WRONG_CREDENTIALS)
    self.assertEqual(resp.status_code, 401)

    WRONG_CREDENTIALS = {
      'username': 'wrong_username',
      'password': 'wrong_password'
    }

    resp = self.client.post(API_ROUTE, data=WRONG_CREDENTIALS)
    self.assertEqual(resp.status_code, 404)

  def gets_user_data(self):
    resp = self.client.get(API_ROUTE, headers=self.user_header)
    self.assertEqual(MOCK_USER['username'], resp.get_json()['username'])

  def auth_works(self):
    resp = self.client.get('/api/user', headers=self.user_header)
    self.assertEqual(resp.status_code, 200)

    resp = self.client.get('/api/user', headers=self.user_header_no_perm)
    self.assertEqual(resp.status_code, 401)

  def can_update_password(self):
    resp = update_password(self.client, MOCK_USER_NO_PERM['username'], MOCK_USER_NO_PERM['registration_number'], MOCK_LOGIN_NO_PERM['password'])
    self.assertEqual(resp.status_code, 200)

    resp = update_password(self.client, MOCK_USER['username'], MOCK_USER['registration_number'], MOCK_LOGIN['password'])
    self.assertEqual(resp.status_code, 200)


  def test_auth(self):
    self.can_update_password()
    self.can_authenticate()
    self.cannot_auth_with_wrong_credentials()
    self.gets_user_data()
    self.auth_works()


def update_password(client, username, registration_number, password):
    resp = client.post(API_ROUTE, data={'username': username, 'password': str(registration_number) })
    header = resp.get_json()

    resp = client.post(API_ROUTE + '/password', headers=header, data={'password': password})
    return resp