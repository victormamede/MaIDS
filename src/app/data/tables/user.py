from ..setup import db
from ...util.auth import Role, encode_roles, decode_roles

import bcrypt

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  real_name = db.Column(db.String, nullable=False)
  registration_number = db.Column(db.Integer, nullable=False, unique=True)
  _roles = db.Column(db.Integer, nullable=False)
  email = db.Column(db.String, nullable=False)

  def __init__(self, **kwargs):
    kwargs['_roles'] = encode_roles(*kwargs['roles'])
    del kwargs['roles']

    password = bcrypt.hashpw(
      kwargs['password'].encode('utf-8'), 
      bcrypt.gensalt()
      )

    kwargs['password'] = password

    super().__init__(**kwargs)

  @property
  def roles(self):
    return decode_roles(self._roles)

  @roles.setter
  def roles(self, value):
    self._roles = encode_roles(*value)

  def as_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'real_name': self.real_name,
      'registration_number': self.registration_number,
      'roles': [role.name for role in self.roles],
      'email': self.email
    }

  def check_password(self, password):
    return bcrypt.checkpw(password.encode('utf-8'), self.password)