import os
import sys
sys.path.append(os.path.dirname(__file__))
from curriculum_data import COURSES_DATA, COURSE_CATALOG

print("Total Cursos en Catálogo:", sum(len(g["courses"]) for g in COURSE_CATALOG.values()))
print("Total Cursos en Datos:", len(COURSES_DATA))

total_lessons = 0
for cid, c in COURSES_DATA.items():
    sec_counts = [len(s["lessons"]) for s in c["sections"]]
    total_lessons += sum(sec_counts)
    print(f"-> {cid:20}: {len(c['sections'])} secciones, lecciones: {sec_counts}")

print("=" * 60)
print(f"TOTAL GENERAL DE LECCIONES: {total_lessons}")
print("=" * 60)
