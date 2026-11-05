# -*- coding: utf-8 -*-
"""
Componentes visuales personalizados de Tkinter con estilo Duolingo 2D
- DuoButton: Botón con relieve 3D táctil
- DuoNode: Nodo circular del camino de aprendizaje (Stepping Stone)
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
        points = [
            x + r, y,
            x + w - r, y,
            x + w, y + r,
            x + w, y + h - r,
            x + w - r, y + h,
            x + r, y + h,
            x, y + h - r,
            x, y + r
        ]
        return self.create_polygon(points, fill=color, smooth=True)


class DuoNode(tk.Canvas):
    """Nodo circular del camino estilo Duolingo con estrellas, corona o candado."""
    def __init__(self, parent, node_num, label, status="locked", icon="⭐", command=None, size=76):
        super().__init__(parent, width=size, height=size + 24, bg=parent.cget("bg"),
                         highlightthickness=0)
        self.node_num = node_num
        self.label = label
        self.status = status
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

    def draw(self):
        self.delete("all")
        self.config(bg=self.master.cget("bg"))
        cx = self.size / 2
        cy = self.size / 2
        r = (self.size - 12) / 2
        offset = 6 if not self.is_pressed else 2

        if self.status == "completed":
            bg = DUO_COLORS["yellow"]
            shadow = DUO_COLORS["yellow_shadow"]
            badge = "👑 1/1"
        elif self.status == "active":
            bg = DUO_COLORS["green"]
            shadow = DUO_COLORS["green_shadow"]
            badge = "¡AQUÍ!"
        elif self.status == "boss":
            bg = DUO_COLORS["purple"]
            shadow = DUO_COLORS["purple_shadow"]
            badge = "BOSS"
        else:
            bg = "#E2E8F0"
            shadow = "#94A3B8"
            badge = "🔒"

        # Sombra 3D
        if not self.is_pressed:
            self.create_oval(cx - r, cy - r + offset, cx + r, cy + r + offset, fill=shadow, outline="")

        y_center = cy if not self.is_pressed else cy + 4
        self.create_oval(cx - r, y_center - r, cx + r, y_center + r, fill=bg,
                         outline="#FFFFFF" if self.status != "locked" else "#CBD5E1", width=2)

        self.create_text(cx, y_center, text=self.icon, font=("Segoe UI Emoji", 20), anchor="center")

        if self.status in ["active", "completed", "boss"]:
            badge_y = y_center - r - 4
            self.create_oval(cx - 24, badge_y - 8, cx + 24, badge_y + 8,
                             fill="#FFC800" if self.status == "completed" else "#58CC02", outline="#FFFFFF", width=1.5)
            self.create_text(cx, badge_y, text=badge, fill="#000000" if self.status == "completed" else "#FFFFFF",
                             font=("Segoe UI", 7, "bold"), anchor="center")

        self.create_text(cx, self.size + 10, text=self.label, fill="#475569",
                         font=("Segoe UI", 8, "bold"), anchor="center")
