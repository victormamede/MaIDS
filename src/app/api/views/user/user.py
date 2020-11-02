from flask_restful import Resource, abort

from ....data.tables import User as UserTable
from ....data import session

from .parser import build_user_creation_parser, build_user_update_parser

from ..auth import with_auth
from ....util.auth import Role


user_creation_parser = build_user_creation_parser()
user_update_parser = build_user_update_parser()

class User(Resource):
  @with_auth(Role.ACCOUNTS)
  def post(self):
    args = user_creation_parser.parse_args()

    new_user = UserTable(
      **args
    )

    try:
      session.add(new_user)
      session.commit()
    except:
      session.rollback()
      abort(409, message='User already exists')


    return new_user.as_dict(), 201


  @with_auth(Role.ACCOUNTS)
  def get(self):
    users = [user.as_dict() for user in UserTable.query.all()] 

    return users, 200

class UserWithId(Resource):
  @with_auth(Role.ACCOUNTS)
  def get(self, **kw):
    user = UserTable.query.filter_by(id=kw['id']).first_or_404(description='User not found')

    return user.as_dict(), 200

  @with_auth(Role.ACCOUNTS)
  def put(self, **kw):
    user = UserTable.query.filter_by(id=kw['id']).first_or_404(description='User not found')
    args = user_update_parser.parse_args()

    for key in args:
      if args[key] == None:
        continue
        
      setattr(user, key, args[key])

    try:
      session.commit()
    except:
      session.rollback()
      abort(409, message='User already exists')

    return user.as_dict(), 200

  @with_auth(Role.ACCOUNTS)
  def delete(self, **kw):
    user = UserTable.query.filter_by(id=kw['id']).first_or_404(description='User not found')

    session.delete(user)
    session.commit()

    return { 'message': 'deleted' }, 200
