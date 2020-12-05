from flask_restful import Resource, abort
from datetime import datetime, timedelta
from .decorator import with_auth
from .util import SECRET_KEY
import jwt

from ....data.tables import User as UserTable
from ....data import session
from ....util.auth import encode_roles

from .parser import construct_auth_parser, construct_password_update_parser

auth_parser = construct_auth_parser()

EXPIRATION_TIME = 24

class Auth(Resource):
  def post(self):
    args = auth_parser.parse_args()

    user = UserTable.query.filter_by(username=args['username']).first_or_404(description='User not found')

    if not user.check_password(args['password']):
      abort(401, message='Wrong password')

    payload = {
      'id': user.id,
      'roles': encode_roles(*[role.name for role in user.roles]),
      'exp': datetime.utcnow() + timedelta(hours=EXPIRATION_TIME)
    }
    jwt_encoded = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

    return { 'auth-token': jwt_encoded, 'should_update_password': user.should_update_password }, 200

  @with_auth()
  def get(self, user_id):
    user = UserTable.query.filter_by(id=user_id).first_or_404(description='User not found')

    return user.as_dict()

password_parser = construct_password_update_parser()

class PasswordUpdate(Resource):
  @with_auth()
  def post(self, user_id):
    args = password_parser.parse_args()

    user = UserTable.query.filter_by(id=user_id).first_or_404(description='User not found')

    user.password = args['password']
    
    try:
      session.commit()
    except Exception as e:
      session.rollback()
      abort(400, message='Could not update password')

    return {'success': True}, 200