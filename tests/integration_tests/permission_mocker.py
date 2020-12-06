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
    elif tb is PermissionException:
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
    no_resp = self.client.get(url, **self._get_args(kwargs, False))
    resp = self.client.get(url, **self._get_args(kwargs, True))

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def post(self, url, **kwargs):
    no_resp = self.client.post(url, **self._get_args(kwargs, False))
    resp = self.client.post(url, **self._get_args(kwargs, True))

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def put(self, url, **kwargs):
    no_resp = self.client.put(url, **self._get_args(kwargs, False))
    resp = self.client.put(url, **self._get_args(kwargs, True))

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def delete(self, url, **kwargs):
    no_resp = self.client.delete(url, **self._get_args(kwargs, False))
    resp = self.client.delete(url, **self._get_args(kwargs, True))

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def _check_result(self, with_perm_status_code, no_perm_status_code):
    if with_perm_status_code == 401:
      raise PermissionException(True)
    if no_perm_status_code != 401:
      raise PermissionException(False)


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

class PermissionException(Exception):
  def __init__(self, with_perm_error):
    if with_perm_error:
      message = 'Error while trying to request with required permissions'
    else:
      message = 'Error while trying to request without permission'

    super().__init__(message)