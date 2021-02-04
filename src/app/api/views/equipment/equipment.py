from src.app.api.views.equipment.passwords.passwords import Password
from flask_restful import Resource, abort
from ..auth import with_auth
from ....util.auth import Role

from .parser import (
    build_equipment_parser,
    build_equipment_update_parser,
    build_equipment_filter_parser,
)

from ....data.tables import Equipment as EquipmentTable
from ....data.tables import Password as PasswordTable
from ....data import session

equipment_creation_parser = build_equipment_parser()
equipment_filter_parser = build_equipment_filter_parser()


class Equipment(Resource):
    @with_auth()
    def get(self):
        args = equipment_filter_parser.parse_args()

        filters = {}
        for key in args:
            if args[key] is None:
                continue

            search = "%{}%".format(args[key])
            filters[key] = search

        results = EquipmentTable.query.filter(
            *[getattr(EquipmentTable, key).like(filters[key]) for key in filters]
        )

        equips = [equipment.as_dict() for equipment in results]

        return equips, 200

    @with_auth(Role.EQUIPMENT)
    def post(self):
        args = equipment_creation_parser.parse_args()

        new_equipment = EquipmentTable(**args)

        try:
            session.add(new_equipment)
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not create equipment")

        return new_equipment.as_dict(), 201


equipment_update_parser = build_equipment_update_parser()


class EquipmentWithId(Resource):
    @with_auth()
    def get(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment not found"
        )

        return equipment.as_dict(), 200

    @with_auth(Role.EQUIPMENT)
    def put(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment not found"
        )
        args = equipment_update_parser.parse_args()

        for key in args:
            if args[key] == None:
                continue

            setattr(equipment, key, args[key])

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not update equipment")

        return equipment.as_dict(), 200

    @with_auth(Role.EQUIPMENT)
    def delete(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment not found"
        )

        session.delete(equipment)

        ## TODO don't forget to test if it actually deletes passwords
        # Also deletes passwords so we don't clutter the database
        PasswordTable.query.filter_by(equipment_id=equipment.id).delete()
        session.commit()

        return {"message": "deleted"}, 200
