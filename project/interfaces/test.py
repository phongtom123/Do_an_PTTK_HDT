from controller.unit_controller import get_all_units
from controller.question_controller import get_all_questions
from controller.reading_controller import get_all_readings
from controller.listening_controller import get_all_listenings

print("=== Questions ===")
for q in get_all_questions():
    print(q)

print("\n=== Readings ===")
for r in get_all_readings():
    print(r)

print("\n=== Listenings ===")
for l in get_all_listenings():
    print(l)
