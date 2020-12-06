from flask_restful import Resource, abort
from ..auth import with_auth
from ....util.auth import Role

from .parser import build_equipment_parser, build_equipment_update_parser

from ....data.tables import Equipment as EquipmentTable
from ....data import session

equipment_creation_parser = build_equipment_parser()

class Equipment(Resource):
  @with_auth(Role.EQUIPMENT)
  def post(self):
    args = equipment_creation_parser.parse_args()

    new_equipment = EquipmentTable(
      **args
    )

    try:
      session.add(new_equipment)
      session.commit()
    except Exception as e:
      session.rollback()
      abort(409, message='Could not create equipment')


    return new_equipment.as_dict(), 201

equipment_update_parser = build_equipment_update_parser()

class EquipmentWithId(Resource):
  @with_auth()
  def get(self, **kw):
    equipment = EquipmentTable.query.filter_by(id=kw['id']).first_or_404(description='Equipment not found')

    return equipment.as_dict(), 200

  @with_auth(Role.EQUIPMENT)
  def put(self, **kw):
    equipment = EquipmentTable.query.filter_by(id=kw['id']).first_or_404(description='Equipment not found')
    args = equipment_update_parser.parse_args()

    for key in args:
      if args[key] == None:
        continue
        
      setattr(equipment, key, args[key])

    try:
      session.commit()
    except Exception as e:
      session.rollback()
      abort(409, message='Could not update equipment')

    return equipment.as_dict(), 200