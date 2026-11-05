# -*- coding: utf-8 -*-
"""
PROGRESS_MANAGER.PY - Administrador de Progreso y Persistencia Multi-Curso
Permite:
- Realizar múltiples cursos al mismo tiempo sin perder el avance de ninguno.
- Rastrear secciones desbloqueadas, lecciones completadas, evaluaciones aprobadas.
- Rastrear niveles de refuerzo generados por la IA al no aprobar una evaluación.
- Desbloquear y listar los apuntes y resúmenes en PDF de cada sección.
- Persistencia automática en archivo JSON (codelingo_progress.json).
"""

import os
import json

class ProgressManager:
    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(os.path.dirname(__file__), "codelingo_progress.json")
        self.storage_path = storage_path
        self.data = self._load()

    def _default_state(self):
        return {
            "user": {
                "name": "Coder",
                "email": "coder@codelingo.dev",
                "avatar": "🤖",
                "theme": "light",
                "gems": 0,
                "streak_days": 0,
                "hearts": 5,
                "xp": 0
            },
            "active_group": "languages",
            "active_course": "Python",
            # Estado por curso independiente (permite hacer varios cursos a la vez)
            "courses_progress": {}
        }

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Aviso al cargar progreso: {e}. Inicializando estado por defecto.")
        return self._default_state()

    def save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar progreso: {e}")

    def get_course_data(self, course_id):
        if "courses_progress" not in self.data:
            self.data["courses_progress"] = {}
        if course_id not in self.data["courses_progress"]:
            self.data["courses_progress"][course_id] = {
                "current_section_idx": 0,
                "completed_lessons": [],         # IDs de lecciones terminadas
                "unlocked_sections": [0],         # Índices de secciones accesibles (0 es Secc 1)
                "passed_evaluations": [],        # IDs de secciones con evaluación aprobada
                "remedial_lessons": {},          # sec_id -> [lista de lecciones generadas por IA]
                "unlocked_pdfs": []              # sec_id -> apuntes oficiales desbloqueados
            }
        return self.data["courses_progress"][course_id]

    def is_lesson_completed(self, course_id, lesson_id):
        cdata = self.get_course_data(course_id)
        return lesson_id in cdata["completed_lessons"]

    def complete_lesson(self, course_id, lesson_id, xp_gain=15, gems_gain=5):
        cdata = self.get_course_data(course_id)
        if lesson_id not in cdata["completed_lessons"]:
            cdata["completed_lessons"].append(lesson_id)
            self.data["user"]["xp"] += xp_gain
            self.data["user"]["gems"] += gems_gain
            self.save()

    def is_section_unlocked(self, course_id, sec_idx):
        cdata = self.get_course_data(course_id)
        return sec_idx in cdata["unlocked_sections"]

    def is_section_passed(self, course_id, sec_id):
        cdata = self.get_course_data(course_id)
        return sec_id in cdata["passed_evaluations"]

    def record_evaluation_passed(self, course_id, sec_idx, sec_id):
        cdata = self.get_course_data(course_id)
        if sec_id not in cdata["passed_evaluations"]:
            cdata["passed_evaluations"].append(sec_id)
        # Desbloquear siguiente sección si existe
        next_sec = sec_idx + 1
        if next_sec not in cdata["unlocked_sections"]:
            cdata["unlocked_sections"].append(next_sec)
        # Desbloquear PDF de apuntes oficiales de esa sección
        if sec_id not in cdata["unlocked_pdfs"]:
            cdata["unlocked_pdfs"].append(sec_id)
        # Recompensas
        self.data["user"]["xp"] += 100
        self.data["user"]["gems"] += 50
        self.save()

    def record_evaluation_failed(self, course_id, sec_id, remedial_lessons):
        """Guarda los niveles de refuerzo generados por la IA en la sección reprobada."""
        cdata = self.get_course_data(course_id)
        cdata["remedial_lessons"][sec_id] = remedial_lessons
        self.save()

    def get_remedials_for_section(self, course_id, sec_id):
        cdata = self.get_course_data(course_id)
        return cdata.get("remedial_lessons", {}).get(sec_id, [])

    def is_pdf_unlocked(self, course_id, sec_id):
        cdata = self.get_course_data(course_id)
        return sec_id in cdata["unlocked_pdfs"]

    def get_all_unlocked_pdfs(self):
        """Retorna una lista de todas las secciones cuyos apuntes PDF han sido desbloqueados."""
        results = []
        for course_id, cdata in self.data.get("courses_progress", {}).items():
            for sec_id in cdata.get("unlocked_pdfs", []):
                results.append((course_id, sec_id))
        return results
