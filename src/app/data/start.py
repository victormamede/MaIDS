from .setup import db
from .tables import *

session = db.session

def start_database(app):
  db.init_app(app)
  db.create_all(app=app)