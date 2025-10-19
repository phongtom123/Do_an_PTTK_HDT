from controller.unit_controller import get_all_units

units = get_all_units()
for u in units:
    print(f"Unit {u.get_Unit_ID()}: {u.get_Unit_Name()}")
