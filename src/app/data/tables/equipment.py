from ..setup import db
from datetime import datetime

class Equipment(db.Model):
  __tablename__ = 'equipment'

  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String)
  brand = db.Column(db.String)
  model = db.Column(db.String)
  series = db.Column(db.String)
