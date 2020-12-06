from .mock_user import MockUserClient

class PermissionMocker():  
  def __init__(self, role, parent):
    self.role = role
    self.parent = parent
    self.client = parent.client
    self.master_header = parent.master_header

  def __enter__(self):
    self.perm_user = MockUserClient([self.role], self.parent, PERMISSION_MOCK_USER).__enter__()
    self.no_perm_user = MockUserClient([], self.parent, NO_PERMISSION_MOCK_USER).__enter__()

    return self
  
  def __exit__(self, type, value, tb):
    if tb is PermissionException:
      self.parent.fail('Error asserting permissions')

    self.perm_user.__exit__(type, value, tb)
    self.no_perm_user.__exit__(type, value, tb)

  def get(self, url, **kwargs):
    resp = self.perm_user.get(url, **kwargs)
    no_resp = self.no_perm_user.get(url, **kwargs)

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def post(self, url, **kwargs):
    resp = self.perm_user.post(url, **kwargs)
    no_resp = self.no_perm_user.post(url, **kwargs)

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def put(self, url, **kwargs):
    resp = self.perm_user.put(url, **kwargs)
    no_resp = self.no_perm_user.put(url, **kwargs)

    self._check_result(resp.status_code, no_resp.status_code)

    return resp

  def delete(self, url, **kwargs):
    resp = self.perm_user.delete(url, **kwargs)
    no_resp = self.no_perm_user.delete(url, **kwargs)

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

NO_PERMISSION_MOCK_USER = { 
  'username': 'no_permissiontestuser',
  'real_name': 'No Permission Test User',
  'registration_number': 829,
  'email': 'no_permission_test@user.com',
}

class PermissionException(Exception):
  def __init__(self, with_perm_error):
    if with_perm_error:
      message = 'Error while trying to request with required permissions'
    else:
      message = 'Error while trying to request without permission'

    super().__init__(message)