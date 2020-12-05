import os

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env.test')

from src.app import build_app
from unittest import TestCase

class AppTestCase(TestCase):
  def setUp(self):
    self.app = build_app()
    self.app.testing = True
    self.client = self.app.test_client()

    self.master_token = os.getenv('MASTER_TOKEN')
    self.master_header = {'auth-token': self.master_token}

  def assertNeedsPermission(self, roles):
    return PermissionMocker(roles, self)

class PermissionMocker():  
  def __init__(self, role, parent):
    self.role = role
    self.parent = parent
    self.client = parent.client
    self.master_header = parent.master_header

  def __enter__(self):
    # Creates a user with no permission
    resp = self.client.post('/api/user', data=NO_PERMISSION_MOCK_USER, headers=self.master_header)
    self.no_permission_user_data = resp.get_json()

    resp = self.client.post('/api/auth', data=NO_PERMISSION_MOCK_LOGIN)
    token = resp.get_json()['auth-token']

    self.no_permission_header = { 'auth-token': token }

    # Creates a user with tested permission
    permission_mock_user = PERMISSION_MOCK_USER.copy()
    permission_mock_user['roles'] = [self.role.name]
    
    resp = self.client.post('/api/user', data=permission_mock_user, headers=self.master_header)
    self.permission_user_data = resp.get_json()

    resp = self.client.post('/api/auth', data=PERMISSION_MOCK_LOGIN)
    token = resp.get_json()['auth-token']

    self.permission_header = { 'auth-token': token }

    return self
  
  def __exit__(self, type, value, tb):
    if tb is None:
      self.client.delete('api/user/' + str(self.permission_user_data['id']), headers=self.master_header)
      self.client.delete('api/user/' + str(self.no_permission_user_data['id']), headers=self.master_header)
    else:
      self.parent.fail('Error asserting permissions')

  def _get_args(self, kwargs, with_permissions):
    args = kwargs.copy()
    headers = {}

    try:
      headers = args['headers']
      del args['headers']
    except KeyError:
      pass
      
    permission_header = self.permission_header if with_permissions else self.no_permission_header
    
    return {
      'headers': {**permission_header, **headers},
      **args
    }

  def get(self, url, **kwargs):
    resp = self.client.get(url, **self._get_args(kwargs, False))
    self.parent.assertEqual(resp.status_code, 401)

    resp = self.client.get(url, **self._get_args(kwargs, True))
    self.parent.assertNotEqual(resp.status_code, 401)

    return resp

  def post(self, url, **kwargs):
    resp = self.client.post(url, **self._get_args(kwargs, False))
    self.parent.assertEqual(resp.status_code, 401)

    resp = self.client.post(url, **self._get_args(kwargs, True))
    self.parent.assertNotEqual(resp.status_code, 401)

    return resp

  def put(self, url, **kwargs):
    resp = self.client.put(url, **self._get_args(kwargs, False))
    self.parent.assertEqual(resp.status_code, 401)

    resp = self.client.put(url, **self._get_args(kwargs, True))
    self.parent.assertNotEqual(resp.status_code, 401)

    return resp

  def delete(self, url, **kwargs):
    resp = self.client.delete(url, **self._get_args(kwargs, False))
    self.parent.assertEqual(resp.status_code, 401)

    resp = self.client.delete(url, **self._get_args(kwargs, True))
    self.parent.assertNotEqual(resp.status_code, 401)

    return resp


PERMISSION_MOCK_USER = { 
  'username': 'permissiontestuser',
  'real_name': 'Test User',
  'registration_number': 828,
  'email': 'permission_test@user.com',
}
PERMISSION_MOCK_LOGIN = {
  'username': PERMISSION_MOCK_USER['username'],
  'password': PERMISSION_MOCK_USER['registration_number']
}

NO_PERMISSION_MOCK_USER = { 
  'username': 'no_permissiontestuser',
  'real_name': 'No Permission Test User',
  'registration_number': 829,
  'roles': ['NONE'],
  'email': 'no_permission_test@user.com',
}
NO_PERMISSION_MOCK_LOGIN = {
  'username': NO_PERMISSION_MOCK_USER['username'],
  'password': NO_PERMISSION_MOCK_USER['registration_number']
}