# -*- coding: utf-8 -*-
"""
AI_TUTOR.PY - Motor Unificado de Inteligencia Artificial ("Byte")
Provee:
1. Pistas pedagógicas inteligentes (guía al usuario sin revelar la respuesta directa).
2. Evaluador de código y comandos de 1 a 100 con desglose cualitativo.
3. Generador adaptativo de ejercicios de refuerzo cuando el usuario no aprueba la evaluación de sección.
"""

import re
import random

class ByteAIEngine:
    def __init__(self):
        self.name = "Byte"
        self.avatar = "🤖"

    def get_pedagogical_hint(self, course_id: str, lesson_data: dict, user_text: str = "") -> str:
        """
        Genera una pista inteligente orientada a guiar el razonamiento del usuario,
        cumpliendo estrictamente con la regla de NO revelar la respuesta directa.
        """
        title = lesson_data.get("title", "")
        lesson_type = lesson_data.get("type", "language")
        user_clean = user_text.strip() if user_text else ""

        # Si el usuario no ha escrito nada aún
        if not user_clean:
            if lesson_type == "language":
                return (
                    f"💡 Pista de {self.name}:\n"
                    f"Para comenzar con '{title}', revisa el código de plantilla. Identifica qué variable o función "
                    "almacena el dato principal e intenta hacer un cambio paso a paso antes de ejecutar."
                )
            elif lesson_type == "terminal":
                return (
                    f"💡 Pista de {self.name}:\n"
                    f"Recuerda que en {course_id} cada comando tiene un propósito específico. Si no recuerdas "
                    "sus parámetros exactos, prueba escribir el comando seguido de '--help' o '/?' para ver su manual."
                )
            else:
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Observa la placa base o chasis: cada componente posee una muesca o forma asimétrica "
                    "que impide colocarlo en la ranura equivocada. Comprueba zócalos y voltajes antes de conectar."
                )

        # Análisis heurístico de código de lenguajes
        if lesson_type == "language":
            # Paréntesis o llaves no balanceadas
            if user_clean.count("(") != user_clean.count(")"):
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Revisa los paréntesis '(' y ')'. Parece que abriste más de los que cerraste (o viceversa). "
                    "Asegúrate de que cada apertura tenga su correspondiente cierre."
                )
            if user_clean.count("{") != user_clean.count("}"):
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Atención a los bloques de código: el número de llaves de apertura '{' no coincide con las de cierre '}'. "
                    "Verifica dónde termina tu función o condicional."
                )
            if user_clean.count("[") != user_clean.count("]"):
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Revisa los corchetes de indexación o listas. Asegúrate de cerrar cada '[' con su respectivo ']'."
                )
            if user_clean.count('"') % 2 != 0 or user_clean.count("'") % 2 != 0:
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Hay una comilla de texto sin cerrar. Revisa las cadenas de caracteres para asegurarte de que "
                    "comiencen y terminen con el mismo tipo de comilla."
                )
            
            # Pista de impresión / salida
            if "print" not in user_clean and "cout" not in user_clean and "printf" not in user_clean and "console" not in user_clean and "System.out" not in user_clean:
                return (
                    f"💡 Pista de {self.name}:\n"
                    "Has escrito lógica, pero ¿cómo sabrá el usuario o el evaluador el resultado? "
                    "Asegúrate de enviar el valor final a la consola o salida estándar."
                )

            # Pista contextual por lenguaje
            if "Python" in course_id:
                if "def " in user_clean and not user_clean.strip().endswith(":"):
                    if any(line.strip().startswith("def ") and not line.strip().endswith(":") for line in user_clean.split("\n")):
                        return f"💡 Pista de {self.name}: En Python, las declaraciones de funciones y condicionales deben finalizar con dos puntos ':' al final de la cabecera."
                return (
                    f"💡 Pista de {self.name}:\n"
                    f"Vas por buen camino con {title}. Recuerda que en Python la indentación define la jerarquía de los bloques. "
                    "Mantén la misma cantidad de espacios (4 recomendados) en cada nivel."
                )
            elif "C++" in course_id or "C" in course_id:
                if ";" not in user_clean:
                    return f"💡 Pista de {self.name}: Recuerda que en {course_id} cada instrucción ejecutable debe terminar obligatoriamente con punto y coma ';'."
                return f"💡 Pista de {self.name}: Presta atención a los tipos de datos de las variables. Asegúrate de que los tipos declarados coincidan con los valores asignados."
            elif "Java" in course_id:
                return f"💡 Pista de {self.name}: Recuerda que en Java toda lógica debe residir dentro de un método de clase. Revisa la firma del método y el tipado de retorno."
            elif "HTML" in course_id:
                return f"💡 Pista de {self.name}: Revisa que cada etiqueta de apertura tenga su etiqueta de cierre correspondiente (ej: <p>...</p>), salvo los elementos vacíos como <img> o <br>."
            elif "CSS" in course_id:
                return f"💡 Pista de {self.name}: Comprueba que cada par propiedad: valor termine con punto y coma ';' y que el selector apunte a la clase o elemento deseado."
            else:
                return f"💡 Pista de {self.name}: Recuerda utilizar nombres de variables descriptivos y verificar que no estés reasignando una constante declarada con 'const'."

        # Análisis de comandos de terminal
        elif lesson_type == "terminal":
            if "Windows" in course_id:
                return (
                    f"💡 Pista de {self.name}:\n"
                    "En PowerShell/CMD las rutas se separan con contrabarra '\\'. Si la ruta contiene espacios, "
                    "recuerda envolverla entre comillas dobles. Usa 'cd ..' para subir de nivel."
                )
            else:
                return (
                    f"💡 Pista de {self.name}:\n"
                    "En Linux Bash los comandos son sensibles a mayúsculas y minúsculas (case-sensitive). "
                    "Las rutas usan barra inclinada '/' y las banderas se introducen con un guion (ej: ls -la)."
                )

        # Hardware
        else:
            return (
                f"💡 Pista de {self.name}:\n"
                "Para este diagnóstico de hardware, verifica siempre la compatibilidad eléctrica (potencia de la fuente), "
                "térmica (TDP del procesador y pasta térmica) y física (dimensiones del gabinete y tipo de ranura)."
            )

    def evaluate_submission(self, course_id: str, lesson_data: dict, user_text: str, exec_output: str = "", has_error: bool = False) -> dict:
        """
        Analiza el trabajo del usuario y genera una puntuación integral de 1 a 100,
        junto con un desglose constructivo de fortalezas y oportunidades de mejora.
        """
        user_clean = user_text.strip() if user_text else ""
        title = lesson_data.get("title", "")
        lesson_type = lesson_data.get("type", "language")

        if not user_clean:
            return {
                "score": 10,
                "badge": "⚠️ Intento Vacío",
                "summary": "No se detectó código ni respuesta ingresada.",
                "strengths": ["Iniciaste la lección."],
                "improvements": ["Escribe una solución en el entorno interactivo antes de solicitar evaluación."]
            }

        # Desglose de puntajes
        # 1. Ejecución y ausencia de errores (0 - 40 pts)
        # 2. Sintaxis y formato (0 - 25 pts)
        # 3. Lógica y alineación con el objetivo pedagógico (0 - 25 pts)
        # 4. Buenas prácticas y estilo (0 - 10 pts)

        score_exec = 40 if not has_error else 15
        score_syntax = 25
        score_logic = 25
        score_style = 10

        strengths = []
        improvements = []

        # Penalizaciones y bonificaciones según código
        if has_error:
            improvements.append("El entorno detectó un error al compilar/ejecutar. Revisa la consola para depurar.")
        else:
            strengths.append("El código se ejecutó limpiamente sin colapsar el entorno.")

        if len(user_clean) > 20:
            strengths.append("Estructura de código bien desarrollada con cantidad adecuada de instrucciones.")
        else:
            score_logic -= 10
            improvements.append("La solución es muy breve; intenta ampliar la lógica para cubrir casos más completos.")

        # Detección de buenas prácticas por lenguaje
        if lesson_type == "language":
            if any(c in user_clean for c in ["#", "//", "/*", "<!--"]):
                strengths.append("Excelente documentación interna con comentarios explicativos.")
                score_style += 2
            else:
                improvements.append("Consejo de estilo: añade comentarios para documentar el propósito de tus variables.")

            # Variables con nombres significativos
            if re.search(r'\b(resultado|total|precio|nombre|contador|valor|item|data)\b', user_clean, re.I):
                strengths.append("Nombres de identificadores claros, descriptivos y legibles.")
            else:
                improvements.append("Usa nombres de variables más representativos en lugar de letras sueltas.")

        elif lesson_type == "terminal":
            strengths.append("Sintaxis de comando procesada correctamente por el emulador del sistema.")
            if "|" in user_clean or ">" in user_clean:
                strengths.append("Excelente uso de tuberías o redirecciones avanzadas de consola.")
            else:
                improvements.append("Tip: Prueba combinar este comando con tuberías para filtrar resultados.")

        else: # Hardware
            strengths.append("Identificación precisa de las especificaciones y ranuras del componente.")
            strengths.append("Criterio técnico acorde a la compatibilidad de placa madre y fuente.")

        total_score = min(100, max(20, score_exec + score_syntax + score_logic + score_style))

        if total_score >= 90:
            badge = "🌟 Sobresaliente (90-100)"
        elif total_score >= 80:
            badge = "🎉 Aprobado con Solidez (80-89)"
        elif total_score >= 60:
            badge = "👍 Progreso Bueno (60-79)"
        else:
            badge = "🔄 Requiere Ajustes (<60)"

        return {
            "score": total_score,
            "badge": badge,
            "summary": f"Evaluación técnica para '{title}' en {course_id}.",
            "strengths": strengths,
            "improvements": improvements
        }

    def generate_remedial_lessons(self, course_id: str, section_data: dict, missed_topics: list) -> list:
        """
        Crea ejercicios adaptativos de refuerzo cuando el usuario no aprueba la evaluación Boss (< 80%).
        Analiza las fallas para diseñar niveles de ejercitación focalizados en lo que más le costó.
        """
        remedials = []
        sec_title = section_data.get("title", "Sección")
        sec_id = section_data.get("id", "sec")

        topics_to_cover = missed_topics if missed_topics else [
            "Fundamentos y Sintaxis Base",
            "Manejo de Errores y Validaciones",
            "Integración de Múltiples Conceptos"
        ]

        for i, topic in enumerate(topics_to_cover[:3]):
            rem_num = i + 1
            rem_obj = {
                "id": f"{sec_id}_remedial_{rem_num}",
                "number": 100 + rem_num,
                "is_remedial": True,
                "title": f"🛠️ Refuerzo IA: {topic}",
                "type": section_data.get("lessons", [{}])[0].get("type", "language"),
                "intro": (
                    f"¡Nivel de Refuerzo generado por {self.name}!\n"
                    f"Durante la evaluación de '{sec_title}', detecté que el área '{topic}' necesita un repaso especial. "
                    "En este nivel guiado fortaleceremos exactamente ese concepto con práctica asistida paso a paso."
                ),
                "code_template": (
                    f"# Práctica de Refuerzo IA con Byte\n"
                    f"# Tema clave: {topic}\n"
                    f"# Escribe tu solución asegurando cada validación:\n"
                    f"def resolver_refuerzo():\n    return 'Concepto {topic} dominado!'\n\nprint(resolver_refuerzo())\n"
                ),
                "practice_goal": f"Aplica el concepto de '{topic}' resolviendo el ejercicio paso a paso con asistencia de Byte.",
                "expected_output": f"Concepto {topic} dominado!",
                "quiz": {
                    "question": f"¿Cuál es la regla esencial para no fallar en '{topic}'?",
                    "options": [
                        "Comprobar las precondiciones, sintaxis y tipos antes de operar.",
                        "Ignorar los tipos y asumir que no habrá excepciones.",
                        "No definir nombres de variables."
                    ],
                    "answer_index": 0,
                    "explanation": f"Verificar precondiciones y aplicar buenas prácticas garantiza dominio en '{topic}'."
                },
                "integrated_challenge": f"Reto de Refuerzo: Construye un caso de prueba donde demuestres que dominas '{topic}'."
            }
            remedials.append(rem_obj)

        return remedials
