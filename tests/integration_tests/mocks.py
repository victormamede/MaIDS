from src.app.util.auth import Role

MOCK_USER = {
  'username': 'testuser',
  'real_name': 'Test User',
  'registration_number': 123,
  'roles': [role.name for role in Role.all()],
  'email': 'test@user.com',
  'password': 'testpass'
}

MOCK_LOGIN = {
  'username': 'testuser',
  'password': 'testpass'
}