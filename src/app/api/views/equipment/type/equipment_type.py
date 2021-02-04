from flask_restful import Resource, abort
from ...auth import with_auth
from .....util.auth import Role

from .parser import build_type_parser, build_type_update_parser

from .....data.tables import EquipmentType as TypeTable
from .....data import session

from .helper import equipment_type_is_used

type_creation_parser = build_type_parser()


class EquipmentType(Resource):
    @with_auth()
    def get(self):
        types = [equipment_type.as_dict() for equipment_type in TypeTable.query.all()]

        return types, 200

    @with_auth(Role.EQUIPMENT)
    def post(self):
        args = type_creation_parser.parse_args()

        new_type = TypeTable(**args)

        try:
            session.add(new_type)
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not create type")

        return new_type.as_dict(), 201


type_update_parser = build_type_update_parser()


class EquipmentTypeWithId(Resource):
    @with_auth()
    def get(self, **kw):
        equipment_type = TypeTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment type not found"
        )

        return equipment_type.as_dict(), 200

    @with_auth(Role.EQUIPMENT)
    def put(self, **kw):
        equipment_type = TypeTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment type not found"
        )
        args = type_update_parser.parse_args()

        for key in args:
            if args[key] == None:
                continue

            setattr(equipment_type, key, args[key])

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not update equipment type")

        return equipment_type.as_dict(), 200

    @with_auth(Role.EQUIPMENT)
    def delete(self, **kw):
        equipment_type = TypeTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Equipment type not found"
        )

        if equipment_type_is_used(equipment_type.id):
            abort(409, message="Equipment type is currently in use")

        session.delete(equipment_type)
        session.commit()

        return {"message": "deleted"}, 200
