from flask_restful import Resource, abort
from ...auth import with_auth
from .....util.auth import Role

from .decorator import password_with_id
from .parser import (
    build_user_password_parser,
    build_level_password_parser,
    build_update_password_parser,
)

from .....data.tables import Password as PasswordTable
from .....data.tables import Equipment as EquipmentTable
from .....data.tables import User as UserTable
from .....data import session

user_password_creation_parser = build_user_password_parser()
level_password_creation_parser = build_level_password_parser()
update_password_parser = build_update_password_parser()


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


class PasswordWithId(Resource):
    @password_with_id
    def get(self, **kw):
        return kw["password"].as_dict(), 200

    @password_with_id
    def put(self, **kw):
        password = kw["password"]
        args = update_password_parser.parse_args()

        for key in args:
            if args[key] == None:
                continue

            setattr(password, key, args[key])

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            abort(409, message="Could not update password")

        return password.as_dict(), 200

    @with_auth(Role.PASSWORDS)
    def delete(self, **kw):
        password = PasswordTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Password not found"
        )

        session.delete(password)
        session.commit()

        return {"message": "deleted"}, 200


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
