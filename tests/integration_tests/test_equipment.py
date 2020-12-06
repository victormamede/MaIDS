import unittest
from .config import AppTestCase
from .mocks import MOCK_EQUIPMENT, MOCK_EQUIPMENT_2, MOCK_EQUIPMENT

from src.app.util.auth import Role

API_ROUTE = '/api/equipment'

class TestEquipment(AppTestCase):
  def creates_equipment(self, client):
    resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT)
    client.post(API_ROUTE, data=MOCK_EQUIPMENT_2) # this will be used in later tests

    self.mock_equipment_id = resp.get_json()['id']

    self.assertEqual(resp.status_code, 201)

  def tags_are_unique(self, client):
    resp = client.post(API_ROUTE, data=MOCK_EQUIPMENT)

    self.assertEqual(resp.status_code, 409)

  def updates_equipment_info(self, client):
    update = {
      'brand': 'NewBrand'
    }

    resp = client.put(API_ROUTE + '/' + str(self.mock_equipment_id), data=update)
    self.assertEqual(resp.get_json()['brand'], update['brand'])

    # Set equipment info back to original state
    resp = client.put(API_ROUTE + '/' + str(self.mock_equipment_id), data=MOCK_EQUIPMENT)

  def deletes_equipment(self, admin_client, regular_client):
    admin_client.delete(API_ROUTE + '/' + str(self.mock_equipment_id))

    resp = regular_client.get(API_ROUTE + '/' + str(self.mock_equipment_id))
    self.assertEqual(resp.status_code, 404)
    
  
  def gets_equipment(self, client):
    resp = client.get(API_ROUTE + '/' + str(self.mock_equipment_id))

    equip = MOCK_EQUIPMENT.copy()
    equip['id'] = self.mock_equipment_id

    self.assertDictEqual(resp.get_json(), equip)
  
  def gets_equipment_list(self, client):
    resp = client.get(API_ROUTE)

    actual = resp.get_json()
    expected = [MOCK_EQUIPMENT, MOCK_EQUIPMENT_2]

    for i in range(len(expected)):
      # remove ids because they don't come with mock equipment data
      del actual[i]['id']

      self.assertDictEqual(expected[i], actual[i])

  def filters_equipment_list(self, client):
    resp = client.get(API_ROUTE, query_string={'tag': '02'})
    actual = resp.get_json()

    # remove ids because they don't come with mock equipment data
    del actual[0]['id']

    self.assertDictEqual(MOCK_EQUIPMENT_2, actual[0])


  def test_equipment(self):
    with self.assertNeedsPermission(Role.EQUIPMENT) as client:
      self.creates_equipment(client)
      self.tags_are_unique(client)
      self.updates_equipment_info(client)

      with self.mockUserClient([]) as regular_client:
        self.gets_equipment(regular_client)
        self.gets_equipment_list(regular_client)
        self.filters_equipment_list(regular_client)
        self.deletes_equipment(client, regular_client)

 