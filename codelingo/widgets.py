# -*- coding: utf-8 -*-
"""
WIDGETS.PY - Componentes Visuales Táctiles Estilo Duolingo 2D en Tkinter
Incluye:
- DuoButton: Botón con relieve 3D táctil que se hunde al presionar.
- DuoNode: Nodo circular del camino de aprendizaje con coronas, estrellas, gemas,
           estados (activo, completado, bloqueado, refuerzo IA, boss examen).
"""

import tkinter as tk
from themes import DUO_COLORS

class DuoButton(tk.Canvas):
    """Botón con relieve 3D táctil estilo Duolingo que se hunde al presionar."""
    def __init__(self, parent, text, command=None, bg_color="#58CC02", shadow_color="#46A302",
                 fg_color="#FFFFFF", width=140, height=42, font_size=10, radius=12, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"),
                         highlightthickness=0, **kwargs)
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.fg_color = fg_color
        self.width = width
        self.height = height
        self.radius = radius
        self.font = ("Segoe UI", font_size, "bold")
        self.is_pressed = False

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
        self.draw()

    def set_colors(self, bg_color, shadow_color, fg_color):
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.fg_color = fg_color
        self.draw()

    def _on_press(self, event):
        self.is_pressed = True
        self.draw()

    def _on_release(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.draw()
            if self.command:
                self.command()

    def draw(self):
        self.delete("all")
        parent_bg = self.master.cget("bg")
        self.config(bg=parent_bg)

        pad = 2
        w = self.width - pad * 2
        h = self.height - pad * 2
        offset = 4 if not self.is_pressed else 1
        depth = 4

        # Sombra 3D
        if not self.is_pressed:
            self._draw_rounded_rect(pad, pad + offset, w, h - depth, self.radius, self.shadow_color)

        # Superficie del botón
        y_top = pad if not self.is_pressed else pad + depth - 1
        self._draw_rounded_rect(pad, y_top, w, h - depth, self.radius, self.bg_color)

        ty = (y_top + (h - depth) / 2)
        self.create_text(self.width / 2, ty, text=self.text, fill=self.fg_color,
                         font=self.font, anchor="center")

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        r = min(r, int(w // 2), int(h // 2))
        d = 2 * r
        # Esquinas perfectamente redondeadas
        self.create_arc(x, y, x + d, y + d, start=90, extent=90, fill=color, outline=color)
        self.create_arc(x + w - d, y, x + w, y + d, start=0, extent=90, fill=color, outline=color)
        self.create_arc(x + w - d, y + h - d, x + w, y + h, start=270, extent=90, fill=color, outline=color)
        self.create_arc(x, y + h - d, x + d, y + h, start=180, extent=90, fill=color, outline=color)
        # Rellenos centrales ortogonales
        self.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
        self.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


class DuoNode(tk.Canvas):
    """Nodo circular del camino pedagógico de Duolingo (Stepping Stone)."""
    def __init__(self, parent, node_num, label, status="locked", icon="⭐", command=None, size=76):
        super().__init__(parent, width=size, height=size + 24, bg=parent.cget("bg"),
                         highlightthickness=0)
        self.node_num = node_num
        self.label = label
        self.status = status # 'locked', 'active', 'completed', 'remedial', 'boss'
        self.icon = icon
        self.command = command
        self.size = size
        self.is_pressed = False

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2" if self.status != "locked" else ""))
        self.draw()

    def _on_press(self, event):
        if self.status != "locked":
            self.is_pressed = True
            self.draw()

    def _on_release(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.draw()
            if self.command:
                self.command()

    def set_status(self, status):
        self.status = status
        self.draw()

    def draw(self):
        self.delete("all")
        self.config(bg=self.master.cget("bg"))
        cx = self.size / 2
        cy = self.size / 2
        r = (self.size - 14) / 2
        offset = 6 if not self.is_pressed else 2

        if self.status == "completed":
            bg = DUO_COLORS["yellow"]
            shadow = DUO_COLORS["yellow_shadow"]
            badge = "👑 1/1"
            badge_bg = "#FFC800"
            badge_fg = "#000000"
        elif self.status == "active":
            bg = DUO_COLORS["green"]
            shadow = DUO_COLORS["green_shadow"]
            badge = "¡AQUÍ!"
            badge_bg = "#58CC02"
            badge_fg = "#FFFFFF"
        elif self.status == "remedial":
            bg = DUO_COLORS["orange"]
            shadow = DUO_COLORS["orange_shadow"]
            badge = "REFUERZO"
            badge_bg = "#FF9600"
            badge_fg = "#FFFFFF"
        elif self.status == "boss":
            bg = DUO_COLORS["purple"]
            shadow = DUO_COLORS["purple_shadow"]
            badge = "EXAMEN"
            badge_bg = "#AF72F5"
            badge_fg = "#FFFFFF"
        else: # locked
            bg = "#E2E8F0"
            shadow = "#94A3B8"
            badge = "🔒"
            badge_bg = "#CBD5E1"
            badge_fg = "#64748B"

        # Sombra 3D inferior
        if not self.is_pressed:
            self.create_oval(cx - r, cy - r + offset, cx + r, cy + r + offset, fill=shadow, outline="")

        # Disco principal
        y_center = cy if not self.is_pressed else cy + 4
        self.create_oval(cx - r, y_center - r, cx + r, y_center + r, fill=bg,
                         outline="#FFFFFF" if self.status != "locked" else "#CBD5E1", width=2)

        # Ícono central del nodo
        self.create_text(cx, y_center, text=self.icon, font=("Segoe UI Emoji", 18), anchor="center")

        # Badge flotante superior
        if self.status != "locked":
            badge_y = y_center - r - 3
            self.create_oval(cx - 26, badge_y - 8, cx + 26, badge_y + 8,
                             fill=badge_bg, outline="#FFFFFF", width=1.5)
            self.create_text(cx, badge_y, text=badge, fill=badge_fg,
                             font=("Segoe UI", 7, "bold"), anchor="center")

        # Etiqueta de texto debajo del nodo
        self.create_text(cx, self.size + 10, text=self.label, fill="#475569",
                         font=("Segoe UI", 8, "bold"), anchor="center")
