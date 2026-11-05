# -*- coding: utf-8 -*-
"""
LESSON_MODAL.PY - Ventanas Modales Interactivas para Lecciones y Exámenes Boss
Implementa el flujo pedagógico riguroso de 4 Fases Secuenciales:
1. Fase 1: Extensa Introducción Teórica al Tema (Marco conceptual, anatomía, ejemplos y consejos).
2. Fase 2: Práctica Activa desde Cero (Sin código hecho, el alumno programa o tipea por su cuenta).
3. Fase 3: Larga Fase de Evaluación de Teoría (Batería interactiva de 3 preguntas teóricas profundas).
4. Fase 4: Reto Integrador Acumulativo de todo lo visto hasta el momento en el curso.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from themes import THEMES, DUO_COLORS
from widgets import DuoButton
from ai_tutor import ByteAIEngine
from simulators_bridge import SimulatorsBridge
from pdf_generator import export_section_pdf

class InteractiveLessonWindow(tk.Toplevel):
    def __init__(self, parent, app, course_id, section_data, lesson_data, on_complete_cb=None):
        super().__init__(parent)
        self.app = app
        self.course_id = course_id
        self.section_data = section_data
        self.lesson_data = lesson_data
        self.on_complete_cb = on_complete_cb
        self.ai = ByteAIEngine()
        self.bridge = SimulatorsBridge.get_instance()

        self.title(f"{lesson_data.get('title', 'Lección')} • {course_id} - CodeLingo")
        self.geometry("980x700")
        self.minsize(860, 600)
        self.theme_key = self.app.current_theme
        t = THEMES[self.theme_key]
        self.config(bg=t["bg"])

        # Estado del Asistente Secuencial de 4 Fases
        self.current_step = 1  # 1: Intro, 2: Práctica, 3: Teoría, 4: Integrador
        self.practice_validated = False
        self.theory_q_idx = 0
        self.theory_score = 0
        self.theory_battery = lesson_data.get("theory_battery", [])
        if not self.theory_battery and "quiz" in lesson_data:
            self.theory_battery = [lesson_data["quiz"]]

        # Respuestas del usuario en la teoría
        self.theory_answers = [-1] * len(self.theory_battery)

        self._build_header()
        self._build_step_indicator()

        # Contenedor dinámico de fase
        self.body_container = tk.Frame(self, bg=t["bg"], padx=16, pady=6)
        self.body_container.pack(fill="both", expand=True)

        self._render_current_step()

    def _build_header(self):
        t = THEMES[self.theme_key]
        header = tk.Frame(self, bg=t["card_bg"], padx=18, pady=10, highlightthickness=1, highlightbackground=t["card_border"])
        header.pack(fill="x")

        top_row = tk.Frame(header, bg=t["card_bg"])
        top_row.pack(fill="x")

        sec_title = self.section_data.get("title", "Sección")
        tk.Label(top_row, text=f"{self.course_id.upper()} • {sec_title.upper()}",
                 font=("Segoe UI", 8, "bold"), fg="#58CC02", bg=t["card_bg"]).pack(side="left")

        ai_tag = tk.Label(top_row, text="🤖 Byte (IA Tutor Activo)", font=("Segoe UI", 8, "bold"),
                          fg="#2563EB", bg="#EFF6FF", padx=8, pady=2)
        ai_tag.pack(side="right")

        les_title = self.lesson_data.get("title", "Lección")
        tk.Label(header, text=les_title, font=("Segoe UI", 13, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w", pady=(2, 0))

        # Tarjeta pedagógica de Byte
        byte_card = tk.Frame(self, bg="#EFF6FF", padx=12, pady=6, highlightthickness=1, highlightbackground="#BFDBFE")
        byte_card.pack(fill="x", padx=16, pady=4)

        left_b = tk.Frame(byte_card, bg="#EFF6FF")
        left_b.pack(side="left", fill="both", expand=True)

        tk.Label(left_b, text="💡 Asistencia de la IA Byte:", font=("Segoe UI", 9, "bold"),
                 fg="#1D4ED8", bg="#EFF6FF").pack(anchor="w")
        tk.Label(left_b, text="Byte te acompaña en las 4 fases: te guía con pistas sin revelar la solución directa y evalúa tu código de 1 a 100.",
                 font=("Segoe UI", 8), fg="#1E293B", bg="#EFF6FF").pack(anchor="w")

        btn_box = tk.Frame(byte_card, bg="#EFF6FF")
        btn_box.pack(side="right")

        DuoButton(btn_box, text="💡 Pista IA", width=95, height=32, font_size=8,
                  bg_color="#FFFFFF", shadow_color="#E2E8F0", fg_color="#B45309",
                  command=self._on_ai_hint).pack(side="left", padx=4)

        DuoButton(btn_box, text="📊 Evaluar (1-100)", width=125, height=32, font_size=8,
                  bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                  command=self._on_ai_evaluate).pack(side="left", padx=4)

    def _build_step_indicator(self):
        t = THEMES[self.theme_key]
        self.stepper_frame = tk.Frame(self, bg=t["card_bg"], padx=16, pady=6, highlightthickness=1, highlightbackground=t["card_border"])
        self.stepper_frame.pack(fill="x", padx=16, pady=(4, 2))
        self._update_step_indicator()

    def _update_step_indicator(self):
        t = THEMES[self.theme_key]
        for w in self.stepper_frame.winfo_children():
            w.destroy()

        steps_info = [
            (1, "1. Introducción Teórica"),
            (2, "2. Práctica Activa"),
            (3, "3. Evaluación Teórica"),
            (4, "4. Reto Integrador")
        ]

        bar_box = tk.Frame(self.stepper_frame, bg=t["card_bg"])
        bar_box.pack(fill="x")

        for num, label in steps_info:
            if num < self.current_step:
                color = "#16A34A"
                icon = "✓ "
                bg_pill = "#DCFCE7"
            elif num == self.current_step:
                color = "#2563EB"
                icon = "▶ "
                bg_pill = "#DBEAFE"
            else:
                color = "#94A3B8"
                icon = "🔒 "
                bg_pill = "#F1F5F9"

            pill = tk.Frame(bar_box, bg=bg_pill, padx=8, pady=4, highlightthickness=1, highlightbackground=color)
            pill.pack(side="left", expand=True, fill="x", padx=2)
            tk.Label(pill, text=f"{icon}{label}", font=("Segoe UI", 8, "bold"), fg=color, bg=bg_pill).pack()

    def _clear_body(self):
        for w in self.body_container.winfo_children():
            w.destroy()

    def _render_current_step(self):
        self._clear_body()
        self._update_step_indicator()

        if self.current_step == 1:
            self._render_step_1_intro()
        elif self.current_step == 2:
            self._render_step_2_practice()
        elif self.current_step == 3:
            self._render_step_3_theory()
        elif self.current_step == 4:
            self._render_step_4_challenge()

    # =========================================================================
    # FASE 1: EXTENSA INTRODUCCIÓN TEÓRICA AL TEMA
    # =========================================================================
    def _render_step_1_intro(self):
        t = THEMES[self.theme_key]
        card = tk.Frame(self.body_container, bg=t["card_bg"], padx=18, pady=14,
                        highlightthickness=1, highlightbackground=t["card_border"])
        card.pack(fill="both", expand=True)

        header_row = tk.Frame(card, bg=t["card_bg"])
        header_row.pack(fill="x", pady=(0, 6))

        tk.Label(header_row, text="📖 Fase 1 de 4: Introducción Teórica Extensa",
                 font=("Segoe UI", 12, "bold"), fg="#2563EB", bg=t["card_bg"]).pack(side="left")
        tk.Label(header_row, text="Lee y asimila los conceptos antes de programar",
                 font=("Segoe UI", 8), fg=t["text_muted"], bg=t["card_bg"]).pack(side="right")

        # Área de texto enriquecido scrolleable
        scroll_frame = tk.Frame(card, bg=t["bg"])
        scroll_frame.pack(fill="both", expand=True, pady=6)

        txt_box = tk.Text(scroll_frame, font=("Segoe UI", 9), wrap="word", bg=t["bg"], fg=t["text"],
                          padx=14, pady=12, highlightthickness=1, highlightbackground=t["card_border"])
        sb = ttk.Scrollbar(scroll_frame, orient="vertical", command=txt_box.yview)
        txt_box.config(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        txt_box.pack(side="left", fill="both", expand=True)

        intro_content = self.lesson_data.get("intro", "Contenido introductorio.")
        txt_box.insert("1.0", intro_content)
        txt_box.config(state="disabled")

        # Barra inferior de avance a Fase 2
        bot_bar = tk.Frame(card, bg=t["card_bg"], pady=8)
        bot_bar.pack(fill="x")

        tk.Label(bot_bar, text="Al comprender la teoría, avanza para escribir tu propia solución desde cero.",
                 font=("Segoe UI", 8), fg=t["text_muted"], bg=t["card_bg"]).pack(side="left")

        def _to_step_2():
            self.current_step = 2
            self._render_current_step()

        DuoButton(bot_bar, text="Continuar a la Práctica Activa (Paso 2) ➔", width=250, height=36,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=_to_step_2).pack(side="right")

    # =========================================================================
    # FASE 2: PRÁCTICA ACTIVA (CREACIÓN DESDE CERO - ¡SIN CÓDIGO HECHO!)
    # =========================================================================
    def _render_step_2_practice(self):
        t = THEMES[self.theme_key]
        card = tk.Frame(self.body_container, bg=t["card_bg"], padx=14, pady=10,
                        highlightthickness=1, highlightbackground=t["card_border"])
        card.pack(fill="both", expand=True)

        header_row = tk.Frame(card, bg=t["card_bg"])
        header_row.pack(fill="x", pady=(0, 6))

        tk.Label(header_row, text="💻 Fase 2 de 4: Práctica Activa (Creación desde Cero)",
                 font=("Segoe UI", 12, "bold"), fg="#16A34A", bg=t["card_bg"]).pack(side="left")

        goal = self.lesson_data.get("practice_goal", "Escribe tu solución desde cero.")
        tk.Label(card, text=f"🎯 Objetivo: {goal}", font=("Segoe UI", 8, "bold"),
                 fg="#15803D", bg="#F0FDF4", padx=8, pady=4).pack(fill="x", pady=(0, 6))

        l_type = self.lesson_data.get("type", "language")

        if l_type == "language":
            self._build_code_workspace(card, is_challenge=False)
        elif l_type == "terminal":
            self._build_terminal_workspace(card, is_challenge=False)
        else:
            self._build_hardware_workspace(card, is_challenge=False)

        # Barra inferior de avance a Fase 3
        bot_bar = tk.Frame(card, bg=t["card_bg"], pady=6)
        bot_bar.pack(fill="x")

        def _back_to_1():
            self.current_step = 1
            self._render_current_step()

        DuoButton(bot_bar, text="⬅ Repasar Teoría", width=120, height=34, font_size=8,
                  bg_color="#FFFFFF", shadow_color="#E2E8F0", fg_color="#475569",
                  command=_back_to_1).pack(side="left")

        def _to_step_3():
            if l_type == "language":
                user_code = self.code_text.get("1.0", "end-1c").strip()
                non_comment_lines = [l for l in user_code.split("\n") if l.strip() and not l.strip().startswith(("#", "//", "/*", "<!--", "*"))]
                if len(non_comment_lines) == 0:
                    messagebox.showwarning(
                        "Práctica Requerida",
                        "¡Debes escribir tu propia solución en el editor y probarla antes de avanzar a la evaluación teórica!\n\n"
                        "Si necesitas orientación, usa el botón '💡 Pista IA'."
                    )
                    return
            self.practice_validated = True
            self.current_step = 3
            self._render_current_step()

        DuoButton(bot_bar, text="Validar Práctica y Continuar a la Evaluación (Paso 3) ➔", width=310, height=34,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=_to_step_3).pack(side="right")

    # =========================================================================
    # FASE 3: LARGA FASE DE EVALUACIÓN DE TEORÍA
    # =========================================================================
    def _render_step_3_theory(self):
        t = THEMES[self.theme_key]
        card = tk.Frame(self.body_container, bg=t["card_bg"], padx=18, pady=14,
                        highlightthickness=1, highlightbackground=t["card_border"])
        card.pack(fill="both", expand=True)

        total_q = len(self.theory_battery)
        curr_idx = self.theory_q_idx
        q_obj = self.theory_battery[curr_idx]

        header_row = tk.Frame(card, bg=t["card_bg"])
        header_row.pack(fill="x", pady=(0, 6))

        tk.Label(header_row, text=f"📝 Fase 3 de 4: Evaluación de Teoría ({curr_idx + 1} de {total_q})",
                 font=("Segoe UI", 12, "bold"), fg="#AF72F5", bg=t["card_bg"]).pack(side="left")
        tk.Label(header_row, text=f"Aciertos acumulados: {self.theory_score} / {total_q}",
                 font=("Segoe UI", 9, "bold"), fg="#6D28D9", bg="#F5F3FF", padx=8, pady=2).pack(side="right")

        # Barra de progreso de la batería
        bar_f = tk.Frame(card, bg="#E2E8F0", height=6)
        bar_f.pack(fill="x", pady=6)
        fill_w = int((curr_idx + 1) / total_q * 100)
        tk.Frame(bar_f, bg="#AF72F5", width=fill_w * 8, height=6).pack(side="left", fill="y")

        # Pregunta
        q_text = q_obj.get("question", "¿Pregunta de teoría?")
        tk.Label(card, text=f"Pregunta {curr_idx + 1}: {q_text}", font=("Segoe UI", 11, "bold"),
                 fg=t["text"], bg=t["card_bg"], wraplength=850, justify="left").pack(anchor="w", pady=(10, 12))

        options = q_obj.get("options", ["Opción A", "Opción B", "Opción C", "Opción D"])
        correct_idx = q_obj.get("answer_index", 0)
        explanation = q_obj.get("explanation", "Explicación técnica de Byte.")

        opt_frame = tk.Frame(card, bg=t["card_bg"])
        opt_frame.pack(fill="both", expand=True)

        btn_refs = []
        feedback_lbl = tk.Label(card, text="", font=("Segoe UI", 9, "bold"), bg=t["card_bg"], wraplength=850, justify="left")
        feedback_lbl.pack(fill="x", pady=8)

        nav_box = tk.Frame(card, bg=t["card_bg"], pady=6)
        nav_box.pack(fill="x")

        def _select_option(chosen_idx):
            for b in btn_refs:
                b.config(state="disabled")

            self.theory_answers[curr_idx] = chosen_idx

            if chosen_idx == correct_idx:
                self.theory_score += 1
                btn_refs[chosen_idx].config(bg="#DCFCE7", fg="#15803D")
                feedback_lbl.config(
                    text=f"✓ ¡Correcto! {explanation}",
                    fg="#16A34A"
                )
            else:
                btn_refs[chosen_idx].config(bg="#FEE2E2", fg="#B91C1C")
                btn_refs[correct_idx].config(bg="#DCFCE7", fg="#15803D")
                feedback_lbl.config(
                    text=f"✗ Incorrecto. La respuesta correcta era: '{options[correct_idx]}'.\nExplicación: {explanation}",
                    fg="#DC2626"
                )

            if curr_idx + 1 < total_q:
                def _next_q():
                    self.theory_q_idx += 1
                    self._render_current_step()

                DuoButton(nav_box, text="Siguiente Pregunta ➔", width=180, height=34,
                          bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                          command=_next_q).pack(side="right")
            else:
                def _to_challenge():
                    self.current_step = 4
                    self._render_current_step()

                DuoButton(nav_box, text="Continuar al Reto Integrador (Paso 4) ➔", width=260, height=34,
                          bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                          command=_to_challenge).pack(side="right")

        for idx, opt in enumerate(options):
            b = tk.Button(opt_frame, text=f"{chr(65+idx)}.  {opt}", font=("Segoe UI", 10),
                          anchor="w", padx=14, pady=10, bg=t["bg"], fg=t["text"],
                          relief="flat", activebackground="#E0F2FE", cursor="hand2",
                          command=lambda i=idx: _select_option(i))
            b.pack(fill="x", pady=4)
            btn_refs.append(b)

    # =========================================================================
    # FASE 4: RETO INTEGRADOR ACUMULATIVO
    # =========================================================================
    def _render_step_4_challenge(self):
        t = THEMES[self.theme_key]
        card = tk.Frame(self.body_container, bg=t["card_bg"], padx=14, pady=10,
                        highlightthickness=1, highlightbackground=t["card_border"])
        card.pack(fill="both", expand=True)

        header_row = tk.Frame(card, bg=t["card_bg"])
        header_row.pack(fill="x", pady=(0, 6))

        tk.Label(header_row, text="🚀 Fase 4 de 4: Reto Integrador Acumulativo",
                 font=("Segoe UI", 12, "bold"), fg="#EA580C", bg=t["card_bg"]).pack(side="left")

        challenge_text = self.lesson_data.get("integrated_challenge", "Combina todos los conceptos vistos.")
        tk.Label(card, text=f"🧩 Desafío: {challenge_text}", font=("Segoe UI", 8, "bold"),
                 fg="#9A3412", bg="#FFEDD5", padx=8, pady=4, wraplength=880, justify="left").pack(fill="x", pady=(0, 6))

        l_type = self.lesson_data.get("type", "language")

        if l_type == "language":
            self._build_code_workspace(card, is_challenge=True)
        elif l_type == "terminal":
            self._build_terminal_workspace(card, is_challenge=True)
        else:
            self._build_hardware_workspace(card, is_challenge=True)

        bot_bar = tk.Frame(card, bg=t["card_bg"], pady=6)
        bot_bar.pack(fill="x")

        tk.Label(bot_bar, text="¡Último paso! Completa el reto integrador para ganar +15 XP y desbloquear el siguiente nivel.",
                 font=("Segoe UI", 8), fg=t["text_muted"], bg=t["card_bg"]).pack(side="left")

        DuoButton(bot_bar, text="🎉 Finalizar y Aprobar Lección (+15 XP)", width=260, height=36,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=self._on_complete_lesson).pack(side="right")

    # =========================================================================
    # ESPACIOS DE TRABAJO (EDITOR / TERMINAL / HARDWARE)
    # =========================================================================
    def _build_code_workspace(self, parent, is_challenge=False):
        t = THEMES[self.theme_key]
        paned = tk.PanedWindow(parent, orient="horizontal", bg="#E2E8F0", sashwidth=4)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg=t["editor_bg"])
        paned.add(left, minsize=420)

        ed_bar = tk.Frame(left, bg=t["editor_bg"], padx=8, pady=4)
        ed_bar.pack(fill="x")
        mode_title = "Editor: Reto Integrador" if is_challenge else "Editor de Código (Escribe tu Solución)"
        tk.Label(ed_bar, text=mode_title, font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg=t["editor_bg"]).pack(side="left")

        sym_bar = tk.Frame(left, bg="#1E293B", padx=4, pady=2)
        sym_bar.pack(fill="x")
        symbols = ["{", "}", "(", ")", "[", "]", ";", "=", '"', "'", "<", ">", ":", "+", "-"]
        for s in symbols:
            btn = tk.Button(sym_bar, text=s, width=2, font=("Consolas", 8, "bold"), bg="#334155", fg="#F8FAFC",
                            relief="flat", activebackground="#475569", activeforeground="#FFFFFF",
                            command=lambda char=s: self.code_text.insert("insert", char))
            btn.pack(side="left", padx=1)

        self.code_text = tk.Text(left, bg=t["editor_bg"], fg=t["editor_fg"],
                                 insertbackground="#FFFFFF", font=("Consolas", 10),
                                 wrap="none", padx=10, pady=10, undo=True)
        self.code_text.pack(fill="both", expand=True)

        if is_challenge:
            template = (
                f"# =======================================================\n"
                f"# RETO INTEGRADOR: {self.lesson_data.get('title')}\n"
                f"# Combina este concepto con lo aprendido en lecciones previas.\n"
                f"# =======================================================\n\n"
            )
        else:
            template = self.lesson_data.get("code_template", "# Escribe tu solución aquí desde cero:\n")

        self.code_text.insert("1.0", template)

        right = tk.Frame(paned, bg=t["terminal_bg"])
        paned.add(right, minsize=320)

        c_bar = tk.Frame(right, bg=t["terminal_bg"], padx=8, pady=4)
        c_bar.pack(fill="x")
        tk.Label(c_bar, text="Consola de Salida / Ejecución en Vivo", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg=t["terminal_bg"]).pack(side="left")

        self.console_text = tk.Text(right, bg=t["terminal_bg"], fg=t["terminal_fg"],
                                    font=("Consolas", 9), wrap="word", padx=8, pady=8, state="disabled")
        self.console_text.pack(fill="both", expand=True)

        run_box = tk.Frame(left, bg=t["editor_bg"], padx=8, pady=6)
        run_box.pack(fill="x")
        DuoButton(run_box, text="▶ Ejecutar y Probar", width=140, height=32, font_size=8,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=self._execute_code).pack(side="right")

    def _execute_code(self):
        code = self.code_text.get("1.0", "end-1c")
        res = self.bridge.run_code(code, self.course_id)
        out = res.get("output", "")
        err = res.get("error", "")

        self.console_text.config(state="normal")
        self.console_text.delete("1.0", "end")
        if err:
            self.console_text.insert("end", f"⚠️ Error detectado:\n{err}\n")
        if out:
            self.console_text.insert("end", f"✓ Salida del programa:\n{out}\n")
        if not out and not err:
            self.console_text.insert("end", "✓ Código ejecutado sin salida en consola.\n")
        self.console_text.config(state="disabled")

    def _build_terminal_workspace(self, parent, is_challenge=False):
        t = THEMES[self.theme_key]
        tk.Label(parent, text=f"🖥️ Consola Virtual de {self.course_id}", font=("Segoe UI", 11, "bold"),
                 fg=t["text"], bg=t["card_bg"]).pack(anchor="w", pady=(0, 4))

        term_box = tk.Frame(parent, bg=t["terminal_bg"], padx=8, pady=8)
        term_box.pack(fill="both", expand=True, pady=(0, 8))

        self.term_display = tk.Text(term_box, bg=t["terminal_bg"], fg=t["terminal_fg"],
                                    font=("Consolas", 10), wrap="word", state="normal")
        self.term_display.pack(fill="both", expand=True)

        os_type = "windows" if "Windows" in self.course_id else "linux"
        prompt = self.bridge.get_terminal_prompt(os_type)
        mode_txt = "MODO RETO INTEGRADOR" if is_challenge else "PRÁCTICA ACTIVA"
        self.term_display.insert("end", f"CodeLingo Virtual Terminal [{self.course_id} - {mode_txt}]\nEscribe 'help' para ver comandos disponibles.\n\n{prompt}")

        input_bar = tk.Frame(parent, bg=t["card_bg"])
        input_bar.pack(fill="x")

        self.cmd_entry = ttk.Entry(input_bar, font=("Consolas", 10))
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.cmd_entry.bind("<Return>", lambda e: self._execute_terminal_cmd())

        DuoButton(input_bar, text="▶ Ejecutar Comando", width=140, height=32, font_size=8,
                  bg_color="#1CB0F6", shadow_color="#1899D6", fg_color="#FFFFFF",
                  command=self._execute_terminal_cmd).pack(side="right")

    def _execute_terminal_cmd(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        os_type = "windows" if "Windows" in self.course_id else "linux"
        output = self.bridge.execute_terminal_cmd(cmd, os_type)
        prompt = self.bridge.get_terminal_prompt(os_type)

        self.term_display.insert("end", f"{cmd}\n")
        if output:
            self.term_display.insert("end", f"{output}\n")
        self.term_display.insert("end", prompt)
        self.term_display.see("end")
        self.cmd_entry.delete(0, "end")

    def _build_hardware_workspace(self, parent, is_challenge=False):
        t = THEMES[self.theme_key]
        info_frame = tk.Frame(parent, bg="#F8FAFC", padx=12, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        info_frame.pack(fill="x", pady=(0, 8))

        if "placement" in self.lesson_data:
            tk.Label(info_frame, text="📍 Ubicación en el Chasis/Placa:", font=("Segoe UI", 9, "bold"), fg="#1E293B", bg="#F8FAFC").pack(anchor="w")
            tk.Label(info_frame, text=self.lesson_data["placement"], font=("Segoe UI", 8), fg="#475569", bg="#F8FAFC", wraplength=850, justify="left").pack(anchor="w", pady=(1, 4))

        sim_box = tk.Frame(parent, bg=t["card_bg"], pady=6)
        sim_box.pack(fill="both", expand=True)

        mode_lab = "Reto Integrador de Hardware: Ensamble y Verificación" if is_challenge else "Laboratorio de Ensamble y Compatibilidad"
        tk.Label(sim_box, text=mode_lab, font=("Segoe UI", 9, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w")

        sel_row = tk.Frame(sim_box, bg=t["card_bg"], pady=6)
        sel_row.pack(fill="x")

        tk.Label(sel_row, text="Componente:", font=("Segoe UI", 8, "bold"), fg=t["text"], bg=t["card_bg"]).pack(side="left", padx=4)
        comp_cb = ttk.Combobox(sel_row, values=["CPU LGA1700 / AM5", "Memoria RAM DDR5 DIMM", "SSD NVMe M.2 2280", "GPU PCIe 5.0 x16", "Memoria SO-DIMM Laptop"], width=26)
        comp_cb.current(0)
        comp_cb.pack(side="left", padx=6)

        tk.Label(sel_row, text="Ranura de Destino:", font=("Segoe UI", 8, "bold"), fg=t["text"], bg=t["card_bg"]).pack(side="left", padx=4)
        slot_cb = ttk.Combobox(sel_row, values=["Socket CPU", "Ranura DIMM A2", "Slot PCIe 16x", "Zócalo M.2 NVMe", "Conector SATA"], width=22)
        slot_cb.current(0)
        slot_cb.pack(side="left", padx=6)

        status_lbl = tk.Label(sim_box, text="Listo para validar ensamble.", font=("Segoe UI", 9, "bold"), fg="#2563EB", bg=t["card_bg"])
        status_lbl.pack(pady=6)

        def _validate_placement():
            c = comp_cb.get()
            s = slot_cb.get()
            valid = (("CPU" in c and "Socket" in s) or
                     ("RAM" in c and "DIMM" in s) or
                     ("SSD" in c and "M.2" in s) or
                     ("GPU" in c and "PCIe" in s) or
                     ("SO-DIMM" in c and "DIMM" in s))
            if valid:
                status_lbl.config(text=f"✓ Montaje Correcto: '{c}' encajó perfectamente en '{s}'. Muescas y pestillos asegurados.", fg="#16A34A")
            else:
                status_lbl.config(text=f"✗ Error de Montaje: No puedes colocar '{c}' en '{s}'. Incompatibilidad mecánica y de zócalo.", fg="#DC2626")

        DuoButton(sim_box, text="⚙️ Validar Montaje", width=140, height=32, font_size=8,
                  bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                  command=_validate_placement).pack()

    # =========================================================================
    # ACCIONES DE LA IA TUTORA "BYTE"
    # =========================================================================
    def _on_ai_hint(self):
        user_code = ""
        if hasattr(self, "code_text"):
            user_code = self.code_text.get("1.0", "end-1c")
        elif hasattr(self, "cmd_entry"):
            user_code = self.cmd_entry.get()

        hint = self.ai.get_pedagogical_hint(self.course_id, self.lesson_data, user_code)
        messagebox.showinfo("🤖 Pista Pedagógica de Byte", hint)

    def _on_ai_evaluate(self):
        user_code = ""
        has_error = False
        if hasattr(self, "code_text"):
            user_code = self.code_text.get("1.0", "end-1c")
            res = self.bridge.run_code(user_code, self.course_id)
            has_error = bool(res.get("error"))
        elif hasattr(self, "cmd_entry"):
            user_code = self.cmd_entry.get()

        eval_data = self.ai.evaluate_submission(self.course_id, self.lesson_data, user_code, has_error)
        msg = f"📊 Puntuación de Código: {eval_data['score']}/100\n"
        msg += f"Rango: {eval_data['badge']}\n\n"
        msg += f"Resumen: {eval_data['summary']}\n\n"
        msg += "Fortalezas Detectadas:\n" + "\n".join(f"  ✓ {s}" for s in eval_data["strengths"]) + "\n\n"
        msg += "Sugerencias de Mejora:\n" + "\n".join(f"  ➜ {i}" for i in eval_data["improvements"])
        messagebox.showinfo("🤖 Evaluación de Calidad de Byte", msg)

    def _on_complete_lesson(self):
        # Otorgar recompensas en progress_manager
        self.app.progress.complete_lesson(self.course_id, self.section_data["id"], self.lesson_data["id"])

        messagebox.showinfo(
            "🎉 ¡Lección Aprobada con Éxito!",
            f"¡Felicitaciones! Has atravesado las 4 fases de aprendizaje:\n"
            f"  1. Introducción Teórica Extensa ✓\n"
            f"  2. Práctica Activa desde Cero ✓\n"
            f"  3. Batería de Evaluación Teórica ({self.theory_score}/{len(self.theory_battery)}) ✓\n"
            f"  4. Reto Integrador Acumulativo ✓\n\n"
            f"Has ganado +15 XP y +5 Gemas. ¡El siguiente nivel en tu camino ha sido desbloqueado!"
        )
        if self.on_complete_cb:
            self.on_complete_cb()
        self.destroy()


class BossEvaluationWindow(tk.Toplevel):
    """
    Examen Boss de Sección. Evalúa todo lo visto hasta el momento.
    - Si aprueba (>= 80%): Desbloquea siguiente sección y PDF de apuntes oficiales.
    - Si no aprueba (< 80%): Byte genera niveles de refuerzo adaptativos en la sección.
    """
    def __init__(self, parent, app, course_id, section_idx, section_data, on_eval_finished=None):
        super().__init__(parent)
        self.app = app
        self.course_id = course_id
        self.section_idx = section_idx
        self.section_data = section_data
        self.on_eval_finished = on_eval_finished
        self.ai = ByteAIEngine()

        self.title(f"Examen de Sección (Boss) • {course_id} - CodeLingo")
        self.geometry("900x640")
        self.minsize(800, 560)
        self.theme_key = self.app.current_theme
        t = THEMES[self.theme_key]
        self.config(bg=t["bg"])

        self.boss_eval = section_data.get("boss_evaluation", {})
        self.questions = self.boss_eval.get("questions", [])
        self.selected_answers = [tk.IntVar(value=-1) for _ in self.questions]

        self._build_ui()

    def _build_ui(self):
        t = THEMES[self.theme_key]

        banner = tk.Frame(self, bg="#AF72F5", padx=20, pady=16)
        banner.pack(fill="x")

        tk.Label(banner, text="👑 EVALUACIÓN DE SECCIÓN (BOSS EXAM)", font=("Segoe UI", 9, "bold"),
                 fg="#F3E8FF", bg="#AF72F5").pack(anchor="w")
        tk.Label(banner, text=f"{self.section_data.get('title', 'Sección')} - {self.course_id}",
                 font=("Segoe UI", 15, "bold"), fg="#FFFFFF", bg="#AF72F5").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text="Nota mínima requerida: 80% (4 de 5 preguntas correctas). Evalúa todos los temas vistos.",
                 font=("Segoe UI", 9), fg="#F5F3FF", bg="#AF72F5").pack(anchor="w", pady=(2, 0))

        scroll_frame = tk.Frame(self, bg=t["card_bg"], padx=20, pady=16, highlightthickness=1, highlightbackground=t["card_border"])
        scroll_frame.pack(fill="both", expand=True, padx=16, pady=12)

        canvas = tk.Canvas(scroll_frame, bg=t["card_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        q_container = tk.Frame(canvas, bg=t["card_bg"])

        q_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=q_container, anchor="nw", width=820)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for idx, q_obj in enumerate(self.questions):
            q_box = tk.Frame(q_container, bg=t["card_bg"], pady=8)
            q_box.pack(fill="x")

            q_num = idx + 1
            tk.Label(q_box, text=f"Pregunta {q_num}: {q_obj['q']}", font=("Segoe UI", 10, "bold"),
                     fg=t["text"], bg=t["card_bg"], wraplength=800, justify="left").pack(anchor="w", pady=(0, 4))

            for o_idx, opt in enumerate(q_obj["options"]):
                rb = tk.Radiobutton(q_box, text=f"  {opt}", variable=self.selected_answers[idx], value=o_idx,
                                    font=("Segoe UI", 9), bg=t["card_bg"], fg=t["text"],
                                    selectcolor=t["card_bg"], activebackground=t["card_bg"])
                rb.pack(anchor="w", pady=2)

        bottom_bar = tk.Frame(self, bg=t["card_bg"], padx=20, pady=12, highlightthickness=1, highlightbackground=t["card_border"])
        bottom_bar.pack(fill="x", side="bottom")

        DuoButton(bottom_bar, text="Cancelar", width=110, height=36, font_size=9,
                  bg_color="#FFFFFF", shadow_color="#E2E8F0", fg_color="#64748B",
                  command=self.destroy).pack(side="left")

        DuoButton(bottom_bar, text="📝 Enviar y Calificar Examen", width=220, height=36,
                  bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                  command=self._grade_evaluation).pack(side="right")

    def _grade_evaluation(self):
        unanswered = [i + 1 for i, v in enumerate(self.selected_answers) if v.get() == -1]
        if unanswered:
            messagebox.showwarning("Examen Incompleto", f"Por favor responde todas las preguntas antes de enviar.\nFaltan responder: {unanswered}")
            return

        total = len(self.questions)
        correct_count = 0
        missed_topics = []

        for idx, q_obj in enumerate(self.questions):
            ans = self.selected_answers[idx].get()
            if ans == q_obj["answer_idx"]:
                correct_count += 1
            else:
                missed_topics.append(q_obj.get("topic", f"Tema {idx+1}"))

        score = int((correct_count / total) * 100)
        passed = score >= 80

        if passed:
            sec_id = self.section_data.get("id")
            pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"apuntes_{self.course_id.lower().replace(' ', '_')}_sec_{self.section_idx+1}.pdf")

            pdf_notes = self.section_data.get("pdf_notes", {
                "course": self.course_id,
                "section": self.section_data.get("title"),
                "overview": "Resumen técnico oficial.",
                "key_points": ["Conceptos completados"],
                "code_example": "// Notas",
                "tips": ["Buen trabajo"]
            })
            export_section_pdf(self.course_id, self.section_data.get("title"), pdf_notes, pdf_path)

            self.app.progress.approve_section(self.course_id, self.section_idx, sec_id, pdf_path)

            messagebox.showinfo(
                "🎉 ¡EVALUACIÓN BOSS SUPERADA!",
                f"¡Sobresaliente! Obtuviste {score}% ({correct_count}/{total} correctas).\n\n"
                f"✓ Desbloqueaste la siguiente sección.\n"
                f"✓ Se ha generado tu PDF oficial de Apuntes y Resumen:\n   '{os.path.basename(pdf_path)}'\n"
                f"Puedes descargarlo o consultarlo en cualquier momento desde la pestaña 'Apuntes PDF'."
            )
        else:
            remedials = self.ai.generate_remedial_lessons(self.course_id, self.section_data, missed_topics)
            self.app.progress.set_remedial_lessons(self.course_id, self.section_data.get("id"), remedials)

            messagebox.showwarning(
                "🔄 EVALUACIÓN NO APROBADA",
                f"Puntaje obtenido: {score}% ({correct_count}/{total} correctas). Mínimo necesario: 80%.\n\n"
                f"La IA 'Byte' analizó tus debilidades en:\n"
                + "\n".join(f"  • {t}" for t in missed_topics) + "\n\n"
                f"Se han desbloqueado {len(remedials)} niveles de ejercitación de refuerzo adaptativo "
                f"en esta sección para reforzar tus conocimientos antes de volver a intentar el Boss."
            )

        if self.on_eval_finished:
            self.on_eval_finished()
        self.destroy()
