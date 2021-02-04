from ..setup import db
from datetime import datetime


class Password(db.Model):
    __tablename__ = "password"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    user = db.relationship("User")
    equipment = db.relationship("Equipment")

    def as_dict(self):
        dict = {
            "id": self.id,
            "equipment": self.equipment.as_dict(),
            "username": self.username,
            "password": self.password,
            "level": self.level,
        }

        if self.user:
            dict["user"] = self.user.as_dict()

        return dict
