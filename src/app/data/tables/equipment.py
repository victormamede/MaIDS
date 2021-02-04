from ..setup import db
from datetime import datetime


class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("equipment_type.id"), nullable=False)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    series = db.Column(db.String)

    equip_type = db.relationship("EquipmentType")

    def as_dict(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "type": self.equip_type.as_dict(),
            "brand": self.brand,
            "model": self.model,
            "series": self.series,
        }
