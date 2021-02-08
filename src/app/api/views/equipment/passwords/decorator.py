from flask_restful import abort

from ...auth.decorator import with_auth

from .....util.auth import Role
from .....data.tables import Password as PasswordTable
from .....data.tables import Equipment as EquipmentTable
from .....data.tables import User as UserTable

### This is messy, but it should decorate a function in the
## form of function(id={password_id})
## the password data will be passed as a kw['password']
def password_with_id(callback):
    @with_auth()
    def my_function(*args, **kw):
        user = UserTable.query.filter_by(id=kw["user_id"]).first_or_404(
            description="User not found"
        )

        password = PasswordTable.query.filter_by(id=kw["id"]).first_or_404(
            description="Password not found"
        )

        if not Role.PASSWORDS in user.roles:
            if not password.user is None:
                if not password.user.id == user.id:
                    abort(401, message="You don't have permission for this")
            else:
                if not password.level >= user.password_level:
                    abort(401, message="You don't have permission for this")

        try:
            return callback(*args, **kw, password=password)
        except TypeError:
            return callback(*args)

    return my_function
