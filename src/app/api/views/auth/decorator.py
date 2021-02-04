import os
import jwt
from flask_restful import reqparse, abort
from .util import SECRET_KEY
from ....util.auth import Role, decode_roles

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("auth-token", location="headers")

MASTER_TOKEN = os.getenv("MASTER_TOKEN") or "master"


def with_auth(*required_roles):
    def function_decorator(callback):
        def my_function(*args, **kwargs):
            args = auth_parser.parse_args()

            my_roles = set()
            try:
                user_id, my_roles = get_user_info(args["auth-token"])
            except jwt.ExpiredSignatureError:
                abort(401, message="Expired token")
            except:
                abort(401, message="Invalid or null auth token")

            for role in required_roles:
                if not role in my_roles:
                    abort(401, message="You don't have permission for this")

            try:
                return callback(*args, **kwargs, user_id=user_id)
            except TypeError:
                return callback(*args)

        return my_function

    return function_decorator


def get_user_info(token):
    if token == MASTER_TOKEN:
        return 0, Role.all()

    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    return payload["id"], decode_roles(payload["roles"])
