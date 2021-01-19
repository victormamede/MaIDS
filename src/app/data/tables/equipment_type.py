from ..setup import db


class EquipmentType(db.Model):
    __tablename__ = 'equipment_type'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, unique=True)

    def as_dict(self):
        return {'id': self.id, 'description': self.description}
