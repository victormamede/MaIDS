from ..setup import db
from datetime import datetime

class Equipment(db.Model):
  __tablename__ = 'equipment'

  id = db.Column(db.Integer, primary_key=True)
  last_updated = db.Column(db.DateTime, default=datetime.utcnow)
  tag = db.Column(db.String)
  brand = db.Column(db.String)
  model = db.Column(db.String)
  series = db.Column(db.String)
