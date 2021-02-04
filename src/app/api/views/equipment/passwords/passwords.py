from flask_restful import Resource, abort
from ...auth import with_auth
from .....util.auth import Role

from .parser import (
    build_password_parser,
)

from .....data.tables import Password as PasswordTable
from .....data.tables import Equipment as EquipmentTable
from .....data.tables import User as UserTable
from .....data import session

password_creation_parser = build_password_parser()


class Password(Resource):
    @with_auth()
    def get(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["equip_id"]).first_or_404(
            description="Equipment not found"
        )
        user = UserTable.query.filter_by(id=kw["user_id"]).first_or_404(
            description="User not found"
        )

        passwords = PasswordTable.query.filter(
            PasswordTable.level >= user.password_level
        ).all()

        return [password.as_dict() for password in passwords]

    @with_auth(Role.PASSWORDS)
    def post(self, **kw):
        equipment = EquipmentTable.query.filter_by(id=kw["equip_id"]).first_or_404(
            description="Equipment not found"
        )
        args = password_creation_parser.parse_args()

        if args["user_id"] != None:
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