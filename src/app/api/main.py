from src.app.api.views.equipment.passwords.passwords import PasswordWithId
from flask_restful import Api

from .views.user import User, UserWithId
from .views.auth import Auth, PasswordUpdate
from .views.equipment import Equipment, EquipmentWithId
from .views.equipment.type import EquipmentType, EquipmentTypeWithId
from .views.equipment.passwords import (
    Password,
    PasswordWithId,
    LevelPassword,
    UserPassword,
)


def start_api(app):
    api = Api(app)

    def add_resource(res, path):
        api.add_resource(res, "/api" + path)

    add_resource(User, "/user")
    add_resource(UserWithId, "/user/<int:id>")

    add_resource(Auth, "/auth")
    add_resource(PasswordUpdate, "/auth/password")

    add_resource(Equipment, "/equipment")
    add_resource(EquipmentWithId, "/equipment/<int:id>")

    add_resource(EquipmentType, "/equipment/type")
    add_resource(EquipmentTypeWithId, "/equipment/type/<int:id>")

    add_resource(Password, "/equipment/<int:equip_id>/password")
    add_resource(PasswordWithId, "/password/<int:id>")
    add_resource(UserPassword, "/equipment/<int:equip_id>/password/user")
    add_resource(LevelPassword, "/equipment/<int:equip_id>/password/level")
