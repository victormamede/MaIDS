import unittest
from src.app.util.auth import decode_roles, encode_roles, Role

class TestRoleEncoder(unittest.TestCase):
  def test_encode_empty(self):
    encoded = encode_roles()
    self.assertEqual(encoded, 0)

  def test_encode_roles(self):
    encoded = encode_roles('ACCOUNTS', 'EQUIPMENT')
    self.assertEqual(encoded, 3)

  def test_decode_roles(self):
    decoded = decode_roles(3)
    self.assertSetEqual(decoded, { Role.ACCOUNTS, Role.EQUIPMENT })

  def test_ignores_repeated_roles(self):
    encoded = encode_roles('ACCOUNTS', 'EQUIPMENT', 'ACCOUNTS', 'EQUIPMENT')
    self.assertEqual(encoded, 3)

  def test_ignores_invalid_roles(self): 
    encoded = encode_roles('CHILDREN_TOY', 'ELECTRIC_MOTOR', 'ACCOUNTS', 'DEFAULT', 'EQUIPMENT')
    self.assertEqual(encoded, 3)