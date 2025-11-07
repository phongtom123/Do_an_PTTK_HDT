# model/unit.py
class Unit:
    def __init__(self, unit_ID=None, unit_name=None, description=None):
        self._unit_ID = unit_ID
        self._unit_name = unit_name
        self._description = description

    # Getter và Setter cho unit_ID
    def get_Unit_ID(self):
        return self._unit_ID

    def set_Unit_ID(self, unit_ID):
        self._unit_ID = unit_ID

    # Getter và Setter cho unit_name
    def get_Unit_Name(self):
        return self._unit_name

    def set_Unit_Name(self, name):
        self._unit_name = name

    # Getter và Setter cho description
    def get_Description(self):
        return self._description

    def set_Description(self, desc):
        self._description = desc

    def __repr__(self):
        return f"Unit(ID={self._unit_ID}, Name='{self._unit_name}')"
