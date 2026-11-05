# -*- coding: utf-8 -*-
"""
GUI_MAIN.PY - Interfaz Gráfica Principal de CodeLingo (Estilo Duolingo 2D)
Orquesta todas las vistas, cursos, secciones (>= 25 lecciones), camino de aprendizaje sinuoso,
evaluaciones Boss, asistente IA Byte, biblioteca de PDFs desbloqueados y perfil.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import subprocess

from themes import THEMES, DUO_COLORS
from widgets import DuoButton, DuoNode
from curriculum_data import COURSE_CATALOG, COURSES_DATA
from progress_manager import ProgressManager
from simulators_bridge import SimulatorsBridge
from lesson_modal import InteractiveLessonWindow, BossEvaluationWindow
from pdf_generator import export_section_pdf

def enable_high_dpi():
    """Activa el modo de alta definición (HiDPI) en Windows para evitar que se vea pixelado o borroso."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        except Exception:
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    import ctypes
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)
                except Exception:
                    try:
                        import ctypes
                        ctypes.windll.user32.SetProcessDPIAware()
                    except Exception:
                        pass

enable_high_dpi()

class CodeLingoApp(tk.Tk):
    def __init__(self):
        enable_high_dpi()
        super().__init__()
        self.title("CodeLingo - Plataforma Educativa de Programación, Terminales y Hardware")
        self.geometry("1100x760")
        self.minsize(980, 660)
        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        # Gestor de progreso y simuladores
        self.progress = ProgressManager()
        self.bridge = SimulatorsBridge.get_instance()

        # Estado inicial
        self.current_theme = self.progress.data["user"].get("theme", "light")
        self.current_group = self.progress.data.get("active_group", "languages")
        self.current_course = self.progress.data.get("active_course", "Python")
        self.current_section_idx = self.progress.get_course_data(self.current_course).get("current_section_idx", 0)
        self.current_tab = "learn"  # 'learn', 'pdfs', 'profile'

        self._configure_ttk_styles()
        self.apply_theme(self.current_theme)

        # Construir UI
        self._build_header()
        self._build_course_selector_bar()
        self._build_main_container()

        # Render inicial
        self.select_group(self.current_group)

    def _configure_ttk_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

    def apply_theme(self, theme_key):
        self.current_theme = theme_key
        t = THEMES[theme_key]
        self.config(bg=t["bg"])
        self.progress.data["user"]["theme"] = theme_key
        self.progress.save()

        self.style.configure("TNotebook", background=t["card_bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=t["card_bg"], foreground=t["text"],
                             padding=[14, 6], font=("Segoe UI", 9, "bold"))
        self.style.map("TNotebook.Tab",
                       background=[("selected", "#58CC02")],
                       foreground=[("selected", "#FFFFFF")])

    def toggle_theme(self):
        target = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(target)
        self.switch_tab(self.current_tab)

    # -------------------------------------------------------------------------
    # ENCABEZADO SUPERIOR (STATS Y ACCIONES)
    # -------------------------------------------------------------------------
    def _build_header(self):
        t = THEMES[self.current_theme]
        self.header_frame = tk.Frame(self, bg=t["header_bg"], height=64,
                                     highlightthickness=1, highlightbackground=t["header_border"])
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        # Lado Izquierdo: Marca y Logo
        brand_frame = tk.Frame(self.header_frame, bg=t["header_bg"], padx=18)
        brand_frame.pack(side="left", fill="y")

        logo_lbl = tk.Label(brand_frame, text="CodeLingo", font=("Segoe UI", 16, "bold"),
                            fg="#58CC02", bg=t["header_bg"])
        logo_lbl.pack(side="left", anchor="center")

        badge = tk.Label(brand_frame, text="PRO", font=("Segoe UI", 8, "bold"),
                         fg="#FFFFFF", bg="#1CB0F6", padx=6, pady=2)
        badge.pack(side="left", padx=8, anchor="center")

        # Lado Derecho: Acciones globales y Stats
        actions_frame = tk.Frame(self.header_frame, bg=t["header_bg"], padx=16)
        actions_frame.pack(side="right", fill="y")

        # Botón Lanzar Suite Web/Móvil
        DuoButton(actions_frame, text="📱 Celular / Web", width=125, height=36, font_size=8,
                  bg_color="#1CB0F6", shadow_color="#1899D6", fg_color="#FFFFFF",
                  command=self._launch_web_mobile).pack(side="left", padx=4)

        # Botón Biblioteca de Apuntes PDF
        DuoButton(actions_frame, text="📄 Apuntes PDF", width=120, height=36, font_size=8,
                  bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                  command=lambda: self.switch_tab("pdfs")).pack(side="left", padx=4)

        # Botón Perfil
        DuoButton(actions_frame, text="⚙️ Perfil", width=95, height=36, font_size=8,
                  bg_color="#64748B", shadow_color="#475569", fg_color="#FFFFFF",
                  command=lambda: self.switch_tab("profile")).pack(side="left", padx=4)

        # Botón Modo Claro/Oscuro
        theme_icon = "🌙 Modo Oscuro" if self.current_theme == "light" else "☀️ Modo Claro"
        self.btn_theme = DuoButton(actions_frame, text=theme_icon, width=120, height=36, font_size=8,
                                   bg_color="#FFC800", shadow_color="#D9A300", fg_color="#000000",
                                   command=self.toggle_theme)
        self.btn_theme.pack(side="left", padx=4)

        # Stats en el centro-derecha
        self.stats_frame = tk.Frame(self.header_frame, bg=t["header_bg"], padx=10)
        self.stats_frame.pack(side="right", fill="y")
        self._update_header_stats()

    def _update_header_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]
        u = self.progress.data["user"]

        items = [
            ("🔥", f"{u['streak_days']} días", "#FF9600"),
            ("💎", f"{u['gems']}", "#1CB0F6"),
            ("💖", f"{u['hearts']}/5", "#FF4B4B"),
            ("⚡", f"{u['xp']} XP", "#FFC800")
        ]

        for icon, text, color in items:
            f = tk.Frame(self.stats_frame, bg=t["header_bg"], padx=8)
            f.pack(side="left", anchor="center")
            tk.Label(f, text=icon, font=("Segoe UI Emoji", 12), fg=color, bg=t["header_bg"]).pack(side="left")
            tk.Label(f, text=text, font=("Segoe UI", 9, "bold"), fg=t["text"], bg=t["header_bg"]).pack(side="left", padx=3)

    # -------------------------------------------------------------------------
    # SELECTOR DE CURSOS Y GRUPOS
    # -------------------------------------------------------------------------
    def _build_course_selector_bar(self):
        t = THEMES[self.current_theme]
        self.course_bar_frame = tk.Frame(self, bg=t["card_bg"],
                                         highlightthickness=1, highlightbackground=t["card_border"])
        self.course_bar_frame.pack(fill="x")

        # Fila 1: Los 4 Grupos Principales
        self.groups_frame = tk.Frame(self.course_bar_frame, bg=t["card_bg"], padx=18, pady=8)
        self.groups_frame.pack(fill="x")

        self.group_buttons = {}
        for group_key, group_data in COURSE_CATALOG.items():
            btn = tk.Button(
                self.groups_frame,
                text=f"{group_data['icon']}  {group_data['name']}",
                font=("Segoe UI", 10, "bold"),
                relief="flat", cursor="hand2", padx=14, pady=6,
                command=lambda gk=group_key: self.select_group(gk)
            )
            btn.pack(side="left", padx=(0, 8))
            self.group_buttons[group_key] = btn

        # Fila 2: Pastillas Dinámicas de Cursos
        self.pills_frame = tk.Frame(self.course_bar_frame, bg=t["card_bg"], padx=18, pady=6)
        self.pills_frame.pack(fill="x")

    def select_group(self, group_key):
        self.current_group = group_key
        self.progress.data["active_group"] = group_key
        t = THEMES[self.current_theme]

        # Resaltar botón de grupo activo
        for gk, btn in self.group_buttons.items():
            if gk == group_key:
                btn.config(bg="#58CC02", fg="#FFFFFF", activebackground="#46A302", activeforeground="#FFFFFF")
            else:
                btn.config(bg=t["pill_bg"], fg=t["pill_fg"], activebackground=t["pill_bg"], activeforeground=t["text"])

        # Actualizar pastillas de cursos según el grupo seleccionado
        self.render_course_pills()

        # Si el curso actual no pertenece a este grupo, cambiar al primer curso disponible
        current_courses = [c["id"] for c in COURSE_CATALOG[group_key]["courses"]]
        if self.current_course not in current_courses:
            self.select_course(current_courses[0])
        else:
            self.select_course(self.current_course)

    def render_course_pills(self):
        for w in self.pills_frame.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]
        courses = COURSE_CATALOG[self.current_group]["courses"]

        tk.Label(self.pills_frame, text="Curso Activo:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(side="left", padx=(0, 8))

        for c in courses:
            is_active = (c["id"] == self.current_course)
            bg_col = t["pill_active_bg"] if is_active else t["pill_bg"]
            fg_col = t["pill_active_fg"] if is_active else t["pill_fg"]
            bd_col = t["pill_active_border"] if is_active else t["pill_border"]

            btn = tk.Button(
                self.pills_frame,
                text=f"{c['icon']} {c['name']}",
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                bg=bg_col, fg=fg_col,
                relief="solid", bd=1, highlightthickness=0,
                padx=12, pady=4, cursor="hand2",
                command=lambda cid=c["id"]: self.select_course(cid)
            )
            btn.pack(side="left", padx=4)

    def select_course(self, course_id):
        self.current_course = course_id
        self.progress.data["active_course"] = course_id
        self.progress.save()

        # Cargar sección guardada de este curso
        cdata = self.progress.get_course_data(course_id)
        self.current_section_idx = cdata.get("current_section_idx", 0)

        self.render_course_pills()
        if self.current_tab == "learn":
            self.render_learn_roadmap()

    # -------------------------------------------------------------------------
    # CONTENEDOR PRINCIPAL Y VISTAS
    # -------------------------------------------------------------------------
    def _build_main_container(self):
        t = THEMES[self.current_theme]
        self.main_container = tk.Frame(self, bg=t["bg"])
        self.main_container.pack(fill="both", expand=True)

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        for w in self.main_container.winfo_children():
            w.destroy()

        self._update_header_stats()
        self.header_frame.config(bg=THEMES[self.current_theme]["header_bg"])
        self.course_bar_frame.config(bg=THEMES[self.current_theme]["card_bg"])

        if tab_name == "learn":
            self.render_learn_roadmap()
        elif tab_name == "pdfs":
            self.render_pdfs_screen()
        elif tab_name == "profile":
            self.render_profile_screen()

    # -------------------------------------------------------------------------
    # VISTA 1: EL CAMINO DE APRENDIZAJE (DUOLINGO ROADMAP CON >= 25 LECCIONES)
    # -------------------------------------------------------------------------
    def render_learn_roadmap(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]
        course_obj = COURSES_DATA.get(self.current_course)
        if not course_obj:
            tk.Label(self.main_container, text=f"Curso '{self.current_course}' no encontrado.").pack()
            return

        sections = course_obj.get("sections", [])
        if not sections:
            return

        # Barra de Selección de Sección (Secciones 1 a 4)
        sec_bar = tk.Frame(self.main_container, bg=t["card_bg"], padx=18, pady=8,
                           highlightthickness=1, highlightbackground=t["card_border"])
        sec_bar.pack(fill="x")

        tk.Label(sec_bar, text="SECCIONES DEL CURSO:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(side="left", padx=(0, 10))

        for idx, sec in enumerate(sections):
            is_unlocked = self.progress.is_section_unlocked(self.current_course, idx)
            is_passed = self.progress.is_section_passed(self.current_course, sec.get("id"))
            is_selected = (idx == self.current_section_idx)

            if is_passed:
                icon = "⭐"
            elif is_unlocked:
                icon = "🔓"
            else:
                icon = "🔒"

            btn_txt = f"{icon} {sec.get('title').split(':')[0]} ({sec.get('lesson_count')} Lecciones)"
            bg_col = "#58CC02" if is_selected else (t["pill_bg"] if is_unlocked else "#E2E8F0")
            fg_col = "#FFFFFF" if is_selected else (t["text"] if is_unlocked else "#94A3B8")

            btn = tk.Button(
                sec_bar, text=btn_txt, font=("Segoe UI", 8, "bold" if is_selected else "normal"),
                bg=bg_col, fg=fg_col, relief="flat", cursor="hand2" if is_unlocked else "",
                padx=10, pady=4,
                command=lambda s_idx=idx: self._select_section(s_idx)
            )
            btn.pack(side="left", padx=4)

        # Banner informativo de la sección activa
        active_sec = sections[self.current_section_idx]
        banner = tk.Frame(self.main_container, bg="#58CC02", padx=20, pady=12)
        banner.pack(fill="x", padx=16, pady=(10, 6))

        tk.Label(banner, text=f"{self.current_course.upper()} • {active_sec.get('title').upper()}",
                 font=("Segoe UI", 9, "bold"), fg="#ECFDF5", bg="#58CC02").pack(anchor="w")
        tk.Label(banner, text=active_sec.get("desc", ""), font=("Segoe UI", 12, "bold"),
                 fg="#FFFFFF", bg="#58CC02").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text=f"Completa las {active_sec.get('lesson_count')} lecciones y vence al Boss para desbloquear la siguiente sección y el PDF oficial.",
                 font=("Segoe UI", 8), fg="#F0FDF4", bg="#58CC02").pack(anchor="w", pady=(2, 0))

        # Canvas con Scroll para el camino sinuoso estilo Duolingo
        path_canvas_frame = tk.Frame(self.main_container, bg=t["card_bg"],
                                     highlightthickness=1, highlightbackground=t["card_border"])
        path_canvas_frame.pack(fill="both", expand=True, padx=16, pady=6)

        canvas = tk.Canvas(path_canvas_frame, bg=t["card_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(path_canvas_frame, orient="vertical", command=canvas.yview)

        # Ancho del contenedor del camino para cálculo simétrico
        ROADMAP_WIDTH = 480
        scroll_frame = tk.Frame(canvas, bg=t["card_bg"], width=ROADMAP_WIDTH)

        # Ventana incrustada en el Canvas anclada en el norte ('n')
        window_item = canvas.create_window((450, 0), window=scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_canvas_configure(event):
            # Centrar dinámicamente el camino de aprendizaje exactamente en la pantalla
            canvas_w = event.width
            canvas.coords(window_item, canvas_w / 2, 0)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _on_canvas_configure)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll con rueda de ratón en toda el área de estudio
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Nodos pedagógicos: Lecciones base + Refuerzos IA (si los hay) + Boss
        lessons = active_sec.get("lessons", [])
        sec_id = active_sec.get("id")
        remedials = self.progress.get_remedials_for_section(self.current_course, sec_id)

        all_nodes = list(lessons)
        # Si hay lecciones de refuerzo generadas por la IA, insertarlas en el camino
        if remedials:
            all_nodes.extend(remedials)

        completed_ids = self.progress.get_course_data(self.current_course).get("completed_lessons", [])

        # Dibujar nodos en zig-zag sinuoso perfectamente centrado
        for i, l_data in enumerate(all_nodes):
            l_id = l_data.get("id")
            is_comp = (l_id in completed_ids)
            is_remedial = l_data.get("is_remedial", False)

            # El primer nodo incompleto está activo; los siguientes bloqueados
            if is_comp:
                st = "completed"
            elif is_remedial:
                st = "remedial"
            elif i == 0 or (i > 0 and all_nodes[i - 1].get("id") in completed_ids):
                st = "active"
            else:
                st = "locked"

            # Offset sinuoso horizontal estilo Duolingo
            sin_offset = int(math.sin(i * 0.75) * 85)
            node_row = tk.Frame(scroll_frame, bg=t["card_bg"], width=ROADMAP_WIDTH, height=96)
            node_row.pack_propagate(False)
            node_row.pack(pady=4)

            # Iconos
            if is_remedial:
                n_icon = "🛠️"
            elif course_obj["category"] == "terminal":
                n_icon = "🖥️"
            elif course_obj["category"] == "hardware":
                n_icon = "⚙️"
            else:
                n_icon = "💻"

            node_btn = DuoNode(
                node_row,
                node_num=l_data.get("number", i + 1),
                label=l_data.get("title", f"Lección {i+1}")[:26],
                status=st,
                icon=n_icon,
                command=lambda ld=l_data, s=active_sec, status=st: self._launch_lesson(ld, s, status)
            )
            # Centrado exacto respecto a ROADMAP_WIDTH:
            node_x = int((ROADMAP_WIDTH - 76) / 2 + sin_offset)
            node_btn.place(x=node_x, y=0)

            # Cofre de recompensa cada 10 lecciones
            if (i + 1) % 10 == 0:
                c_row = tk.Frame(scroll_frame, bg=t["card_bg"], width=ROADMAP_WIDTH, height=52)
                c_row.pack_propagate(False)
                c_row.pack(pady=6)
                chest_w = 210
                chest_x = int((ROADMAP_WIDTH - chest_w) / 2)
                c_btn = DuoButton(c_row, text="🎁 Cofre Secreto +20 Gemas", width=chest_w, height=36, font_size=8,
                                  bg_color="#FFC800", shadow_color="#D9A300", fg_color="#000000",
                                  command=self._claim_chest)
                c_btn.place(x=chest_x, y=0)

        # Boss Evaluación al final de las 25 lecciones
        boss_row = tk.Frame(scroll_frame, bg=t["card_bg"], width=ROADMAP_WIDTH, height=124)
        boss_row.pack_propagate(False)
        boss_row.pack(pady=16)
        boss_size = 86
        boss_x = int((ROADMAP_WIDTH - boss_size) / 2)
        boss_node = DuoNode(
            boss_row,
            node_num="BOSS",
            label="👑 EXAMEN DE SECCIÓN",
            status="boss",
            icon="👑",
            size=boss_size,
            command=lambda s=active_sec, s_idx=self.current_section_idx: self._open_boss_exam(s, s_idx)
        )
        boss_node.place(x=boss_x, y=0)

    def _select_section(self, sec_idx):
        if not self.progress.is_section_unlocked(self.current_course, sec_idx):
            messagebox.showinfo("🔒 Sección Bloqueada", "Debes completar la sección anterior y aprobar la evaluación Boss para desbloquear esta sección.")
            return
        self.current_section_idx = sec_idx
        cdata = self.progress.get_course_data(self.current_course)
        cdata["current_section_idx"] = sec_idx
        self.progress.save()
        self.render_learn_roadmap()

    def _launch_lesson(self, lesson_data, section_data, status):
        if status == "locked":
            messagebox.showinfo("🔒 Nivel Bloqueado", "Completa la lección anterior del camino para desbloquear esta lección.")
            return

        InteractiveLessonWindow(
            self,
            app=self,
            course_id=self.current_course,
            section_data=section_data,
            lesson_data=lesson_data,
            on_complete_cb=self.render_learn_roadmap
        )

    def _open_boss_exam(self, section_data, sec_idx):
        BossEvaluationWindow(
            self,
            app=self,
            course_id=self.current_course,
            section_idx=sec_idx,
            section_data=section_data,
            on_eval_finished=self.render_learn_roadmap
        )

    def _claim_chest(self):
        self.progress.data["user"]["gems"] += 20
        self.progress.data["user"]["streak_days"] += 1
        self.progress.save()
        self._update_header_stats()
        messagebox.showinfo("🎁 ¡Cofre Reclamado!", "¡Has conseguido +20 Gemas y tu racha de días ha aumentado!")

    # -------------------------------------------------------------------------
    # VISTA 2: BIBLIOTECA DE APUNTES PDF DESBLOQUEADOS
    # -------------------------------------------------------------------------
    def render_pdfs_screen(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]

        banner = tk.Frame(self.main_container, bg="#AF72F5", padx=20, pady=16)
        banner.pack(fill="x", padx=16, pady=(10, 8))

        tk.Label(banner, text="BIBLIOTECA OFICIAL DE APUNTES Y RESÚMENES PDF",
                 font=("Segoe UI", 9, "bold"), fg="#F3E8FF", bg="#AF72F5").pack(anchor="w")
        tk.Label(banner, text="Documentos Desbloqueados por Sección",
                 font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#AF72F5").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text="Al completar una sección de 25 lecciones y aprobar su evaluación Boss, desbloqueas su PDF oficial con resumen, chuletas y buenas prácticas.",
                 font=("Segoe UI", 9), fg="#F5F3FF", bg="#AF72F5").pack(anchor="w", pady=(2, 0))

        # Cuadrícula de tarjetas
        scroll_frame = tk.Frame(self.main_container, bg=t["bg"])
        scroll_frame.pack(fill="both", expand=True, padx=16, pady=8)

        canvas = tk.Canvas(scroll_frame, bg=t["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        card_grid = tk.Frame(canvas, bg=t["bg"])

        card_grid.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=card_grid, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        col = 0
        row = 0

        # Recorrer todos los cursos y secciones
        for cid, cobj in COURSES_DATA.items():
            for s_idx, sec in enumerate(cobj.get("sections", [])):
                sec_id = sec.get("id")
                is_unlocked = self.progress.is_pdf_unlocked(cid, sec_id)

                card = tk.Frame(card_grid, bg=t["card_bg"], padx=14, pady=14, width=300, height=180,
                                highlightthickness=1, highlightbackground=t["card_border"])
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                card.pack_propagate(False)

                top_f = tk.Frame(card, bg=t["card_bg"])
                top_f.pack(fill="x")

                tk.Label(top_f, text=cobj.get("icon", "📄"), font=("Segoe UI Emoji", 14), bg=t["card_bg"]).pack(side="left")
                tk.Label(top_f, text=f" {cid}", font=("Segoe UI", 10, "bold"), fg="#58CC02", bg=t["card_bg"]).pack(side="left")

                badge_txt = "DESBLOQUEADO ✓" if is_unlocked else "BLOQUEADO 🔒"
                badge_col = "#16A34A" if is_unlocked else "#94A3B8"
                tk.Label(top_f, text=badge_txt, font=("Segoe UI", 7, "bold"), fg=badge_col, bg=t["card_bg"]).pack(side="right")

                tk.Label(card, text=sec.get("title"), font=("Segoe UI", 9, "bold"),
                         fg=t["text"], bg=t["card_bg"], wraplength=270, justify="left").pack(anchor="w", pady=(6, 4))
                tk.Label(card, text=sec.get("desc", ""), font=("Segoe UI", 8),
                         fg=t["text_muted"], bg=t["card_bg"], wraplength=270, justify="left").pack(anchor="w")

                bot_f = tk.Frame(card, bg=t["card_bg"])
                bot_f.pack(fill="x", side="bottom")

                if is_unlocked:
                    DuoButton(bot_f, text="⬇️ Descargar PDF", width=130, height=32, font_size=8,
                              bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                              command=lambda c=cid, s=sec: self._download_pdf(c, s)).pack(side="right")
                else:
                    tk.Label(bot_f, text="Aprueba el Boss para desbloquear", font=("Segoe UI", 7, "italic"),
                             fg="#94A3B8", bg=t["card_bg"]).pack(side="left")

                col += 1
                if col >= 3:
                    col = 0
                    row += 1

    def _download_pdf(self, course_name, sec_data):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Documento PDF", "*.pdf"), ("Archivo de Texto", "*.txt")],
            initialfile=f"Apuntes_{course_name}_{sec_data.get('id')}.pdf",
            title=f"Guardar Apuntes Oficiales de {course_name}"
        )
        if file_path:
            export_section_pdf(course_name, sec_data.get("title"), sec_data.get("pdf_notes", {}), file_path)
            messagebox.showinfo("📄 Descarga Exitosa", f"Los apuntes oficiales de {course_name} han sido generados con éxito en:\n{file_path}")

    # -------------------------------------------------------------------------
    # VISTA 3: PERFIL Y AJUSTES
    # -------------------------------------------------------------------------
    def render_profile_screen(self):
        for w in self.main_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]
        u = self.progress.data["user"]

        banner = tk.Frame(self.main_container, bg="#2563EB", padx=20, pady=16)
        banner.pack(fill="x", padx=16, pady=(10, 8))

        tk.Label(banner, text="CONFIGURACIÓN DE CUENTA Y PERFIL", font=("Segoe UI", 9, "bold"), fg="#DBEAFE", bg="#2563EB").pack(anchor="w")
        tk.Label(banner, text="Progreso Global y Ajustes de Usuario", font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#2563EB").pack(anchor="w", pady=(2, 0))

        content_frame = tk.Frame(self.main_container, bg=t["card_bg"], padx=20, pady=20,
                                 highlightthickness=1, highlightbackground=t["card_border"])
        content_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Avatar y datos
        top_p = tk.Frame(content_frame, bg=t["card_bg"])
        top_p.pack(fill="x", pady=(0, 16))

        tk.Label(top_p, text=u.get("avatar", "🤖"), font=("Segoe UI Emoji", 32), bg=t["card_bg"]).pack(side="left", padx=(0, 16))

        info_box = tk.Frame(top_p, bg=t["card_bg"])
        info_box.pack(side="left")

        tk.Label(info_box, text=u.get("name", "Coder"), font=("Segoe UI", 14, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w")
        tk.Label(info_box, text=f"Correo: {u.get('email', 'coder@codelingo.dev')}", font=("Segoe UI", 9), fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w")
        tk.Label(info_box, text=f"Total XP: {u.get('xp', 0)} • Gemas: {u.get('gems', 0)} • Racha: {u.get('streak_days', 0)} días",
                 font=("Segoe UI", 9, "bold"), fg="#58CC02", bg=t["card_bg"]).pack(anchor="w", pady=(4, 0))

        # Selector de Tema
        tk.Label(content_frame, text="Tema de Interfaz:", font=("Segoe UI", 10, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w", pady=(8, 4))
        theme_row = tk.Frame(content_frame, bg=t["card_bg"])
        theme_row.pack(fill="x", pady=(0, 14))

        DuoButton(theme_row, text="☀️ Modo Claro", width=130, height=36, font_size=8,
                  bg_color="#FFFFFF" if self.current_theme == "light" else "#CBD5E1",
                  shadow_color="#E2E8F0" if self.current_theme == "light" else "#94A3B8",
                  fg_color="#0F172A",
                  command=lambda: self._set_theme("light")).pack(side="left", padx=4)

        DuoButton(theme_row, text="🌙 Modo Oscuro", width=130, height=36, font_size=8,
                  bg_color="#1E293B" if self.current_theme == "dark" else "#64748B",
                  shadow_color="#0F172A" if self.current_theme == "dark" else "#334155",
                  fg_color="#FFFFFF",
                  command=lambda: self._set_theme("dark")).pack(side="left", padx=4)

        # Resumen de Cursos Activos
        tk.Label(content_frame, text="Estado de tus Cursos (Progreso Multi-Curso):", font=("Segoe UI", 10, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w", pady=(12, 6))

        summary_box = tk.Text(content_frame, height=8, font=("Consolas", 9), bg=t["bg"], fg=t["text"],
                              padx=10, pady=10, highlightthickness=1, highlightbackground=t["card_border"])
        summary_box.pack(fill="both", expand=True, pady=(0, 14))

        prog = self.progress.data.get("courses_progress", {})
        summary_lines = []
        for cid in COURSES_DATA.keys():
            c_info = prog.get(cid, {})
            comp_count = len(c_info.get("completed_lessons", []))
            unlocked_sec = len(c_info.get("unlocked_sections", [0]))
            passed_evals = len(c_info.get("passed_evaluations", []))
            summary_lines.append(f"• {cid:22} | Lecciones completadas: {comp_count:3d} | Secciones desbloqueadas: {unlocked_sec}/4 | Boss superados: {passed_evals}")

        summary_box.insert("1.0", "\n".join(summary_lines))
        summary_box.config(state="disabled")

        # Botón volver al camino
        DuoButton(content_frame, text="Volver al Camino de Aprendizaje", width=240, height=40, font_size=9,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=lambda: self.switch_tab("learn")).pack(side="right")

    def _set_theme(self, theme_key):
        self.apply_theme(theme_key)
        self.switch_tab("profile")

    def _launch_web_mobile(self):
        ok, msg = self.bridge.launch_mobile_web_server(port=8080)
        messagebox.showinfo("📱 Simulador Web / Móvil", f"{msg}\n\nConéctate desde tu celular o tablet en la misma red Wi-Fi ingresando al puerto :8080.")


def main():
    app = CodeLingoApp()
    app.mainloop()

if __name__ == "__main__":
    main()
