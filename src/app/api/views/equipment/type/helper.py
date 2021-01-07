from .....data.tables import Equipment as EquipmentTable


def equipment_type_is_used(type_id):
    empty = EquipmentTable.query.filter_by(type_id=type_id).first() is None

    return not empty