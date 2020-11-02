from flask_restful import Api

from .views.user import User, UserWithId
from .views.auth import Auth

def start_api(app):
  api = Api(app)

  def add_resource(res, path):
    api.add_resource(res, '/api' + path)

  add_resource(User, '/user')
  add_resource(UserWithId, '/user/<int:id>')
  add_resource(Auth, '/auth')
