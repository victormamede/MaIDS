from flask_restful import Resource, abort
from ...auth import with_auth
from .....util.auth import Role

from .parser import (
    build_user_password_parser,
    build_level_password_parser,
)

from .....data.tables import Password as PasswordTable
from .....data.tables import Equipment as EquipmentTable
from .....data.tables import User as UserTable
from .....data import session

user_password_creation_parser = build_user_password_parser()
level_password_creation_parser = build_level_password_parser()


class Password(Resource):
    @with_auth()
    def get(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["equip_id"]).first_or_404(
            description="Equipment not found"
        )
        user = UserTable.query.filter_by(id=kw["user_id"]).first_or_404(
            description="User not found"
        )

        user_passwords = PasswordTable.query.filter_by(user_id=kw["user_id"]).all()
        level_passwords = PasswordTable.query.filter(
            PasswordTable.level >= user.password_level
        ).all()

        return [password.as_dict() for password in [*user_passwords, *level_passwords]]


class UserPassword(Resource):
    @with_auth(Role.PASSWORDS)
    def post(self, **kw):
        args = user_password_creation_parser.parse_args()

        equipment = EquipmentTable.query.filter_by(id=kw["equip_id"]).first_or_404(
            description="Equipment not found"
        )

        UserTable.query.filter_by(id=args["user_id"]).first_or_404(
            description="User not found"
        )

        new_password = PasswordTable(equipment_id=equipment.id, **args)

        try:
            session.add(new_password)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            abort(409, message="Could not create password")

        return new_password.as_dict(), 200


class LevelPassword(Resource):
    @with_auth(Role.PASSWORDS)
    def post(self, **kw):
        args = level_password_creation_parser.parse_args()

        equipment = EquipmentTable.query.filter_by(id=kw["equip_id"]).first_or_404(
            description="Equipment not found"
        )

        new_password = PasswordTable(equipment_id=equipment.id, **args)

        try:
            session.add(new_password)
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not create password")

        return new_password.as_dict(), 200
