# model/unit.py

class Unit:
    """Lớp mô tả một Unit trong hệ thống BLEU."""

    def __init__(self, unit_id=None, unit_name=None):
        self._unit_id = unit_id
        self._unit_name = unit_name

    # ========================
    # Getter / Setter
    # ========================

    def get_unit_id(self):
        return self._unit_id

    def set_unit_id(self, unit_id):
        self._unit_id = unit_id

    def get_unit_name(self):
        return self._unit_name

    def set_unit_name(self, name):
        self._unit_name = name

    def __repr__(self):
        return f"Unit(ID={self._unit_id}, Name='{self._unit_name}')"
