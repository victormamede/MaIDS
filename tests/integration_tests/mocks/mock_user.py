DEFAULT_MOCK_USER = {
  'username': 'mockusertest',
  'real_name': 'Test Mock User',
  'registration_number': 3502,
  'email': 'mockusertest@user.com',
}

class MockUserClient():  
  def __init__(self, roles, parent, mock_data = DEFAULT_MOCK_USER):
    self.roles = roles
    self.parent = parent
    self.client = parent.client
    self.master_header = parent.master_header
    self.mock_data = mock_data.copy()

  def __enter__(self):
    # Creates a user with tested permission
    mock_user = self.mock_data.copy()
    mock_user['roles'] = [role.name for role in self.roles] + ['NONE']
    
    resp = self.client.post('/api/user', data=mock_user, headers=self.master_header)
    self.user_data = resp.get_json()

    login = {
      'username': mock_user['username'],
      'password': mock_user['registration_number']
    }

    resp = self.client.post('/api/auth', data=login)
    token = resp.get_json()['auth-token']

    self.header = { 'auth-token': token }

    return self
  
  def __exit__(self, type, value, tb):
    self.client.delete('api/user/' + str(self.user_data['id']), headers=self.master_header)

  def _get_args(self, kwargs):
    args = kwargs.copy()
    headers = {}

    try:
      headers = args['headers']
      del args['headers']
    except KeyError:
      pass
    
    return {
      'headers': {**self.header, **headers},
      **args
    }

  def get(self, url, **kwargs):
    resp = self.client.get(url, **self._get_args(kwargs))
    return resp

  def post(self, url, **kwargs):
    resp = self.client.post(url, **self._get_args(kwargs))
    return resp

  def put(self, url, **kwargs):
    resp = self.client.put(url, **self._get_args(kwargs))
    return resp

  def delete(self, url, **kwargs):
    resp = self.client.delete(url, **self._get_args(kwargs))
    return resp