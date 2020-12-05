import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT
from src.app.util.auth import Role

API_ROUTE = '/api/equipment'

class TestEquipment(AppTestCase):
  def creates_equipment(self):
    with self.assertNeedsPermission(Role.EQUIPMENT) as client:
      resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT)
      self.mock_equipment_id = resp.get_json()['id']

      self.assertEqual(resp.status_code, 201)

  def test_equipment(self):
    #self.creates_equipment()
    pass