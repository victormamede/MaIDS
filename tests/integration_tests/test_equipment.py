import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT

from src.app.util.auth import Role

API_ROUTE = '/api/equipment'

class TestEquipment(AppTestCase):
  def creates_equipment(self, client):
    resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT)
    self.mock_equipment_id = resp.get_json()['id']

    self.assertEqual(resp.status_code, 201)

  def tags_are_unique(self, client):
    resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT)

    self.assertEqual(resp.status_code, 409)
  
  def gets_equipment(self, client):
    resp = client.get(API_ROUTE + '/' + str(self.mock_equipment_id))

    equip = MOCK_EQUIPMENT.copy()
    equip['id'] = self.mock_equipment_id

    self.assertDictEqual(resp.get_json(), equip)


  def test_equipment(self):
    with self.assertNeedsPermission(Role.EQUIPMENT) as client:
      self.creates_equipment(client)
      self.tags_are_unique(client)
 
    with self.mockUserClient([]) as client:
      self.gets_equipment(client)