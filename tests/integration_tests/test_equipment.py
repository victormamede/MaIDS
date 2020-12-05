import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT

API_ROUTE = '/api/equipment'

""" class TestEquipment(AppTestCase):
  def creates_equipment(self):
    resp = self.client.post(API_ROUTE, data=MOCK_EQUIPMENT, headers=self.master_header)
    self.mock_equipment_id = resp.get_json()['id']

    self.assertEqual(resp.status_code, 201)
 """