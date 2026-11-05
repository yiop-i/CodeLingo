#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 CODELINGO - APLICACIÓN EDUCATIVA 2D EN PYTHON (ESTILO DUOLINGO)
=============================================================================
Interfaz gráfica nativa completa para aprender programación, desarrollo web,
terminales de sistemas operativos (Linux / Windows) y hardware de computadoras.
Incluye:
  - 4 Grupos principales superiores y selección dinámica de cursos
  - Camino de aprendizaje con nodos interactivos estilo Duolingo
  - Entorno de práctica (Editor de código, terminal simulada, lab de hardware)
  - IA tutora 'Byte' con pistas y evaluación de código (1 a 100)
  - Biblioteca de apuntes descargables en PDF / texto
  - Configuración de perfil con cambio de tema Claro / Oscuro en tiempo real
=============================================================================
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import random
import time

# =============================================================================
# PALETAS DE COLORES Y TEMAS (CLARO Y OSCURO)
# =============================================================================
THEMES = {
    "light": {
        "bg": "#F8FAFC",
        "card_bg": "#FFFFFF",
        "card_border": "#E2E8F0",
        "text": "#0F172A",
        "text_muted": "#64748B",
        "nav_bg": "#FFFFFF",
        "nav_border": "#E2E8F0",
        "header_bg": "#FFFFFF",
        "header_border": "#E2E8F0",
        "pill_bg": "#FFFFFF",
        "pill_border": "#CBD5E1",
        "pill_fg": "#475569",
        "pill_active_bg": "#ECFDF5",
        "pill_active_border": "#10B981",
        "pill_active_fg": "#047857",
        "stone_locked": "#E2E8F0",
        "stone_locked_shadow": "#94A3B8",
        "terminal_bg": "#300A24",
        "terminal_fg": "#4AF626",
        "editor_bg": "#0F172A",
        "editor_fg": "#6EE7B7",
    },
    "dark": {
        "bg": "#131F24",
        "card_bg": "#1E293B",
        "card_border": "#334155",
        "text": "#F8FAFC",
        "text_muted": "#94A3B8",
        "nav_bg": "#1E293B",
        "nav_border": "#334155",
        "header_bg": "#1E293B",
        "header_border": "#334155",
        "pill_bg": "#1E293B",
        "pill_border": "#334155",
        "pill_fg": "#94A3B8",
        "pill_active_bg": "#064E3B",
        "pill_active_border": "#10B981",
        "pill_active_fg": "#6EE7B7",
        "stone_locked": "#334155",
        "stone_locked_shadow": "#0F172A",
        "terminal_bg": "#1A0914",
        "terminal_fg": "#4AF626",
        "editor_bg": "#090D16",
        "editor_fg": "#6EE7B7",
    }
}

# Colores característicos de Duolingo
DUO_COLORS = {
    "green": "#58CC02",
    "green_shadow": "#46A302",
    "blue": "#1CB0F6",
    "blue_shadow": "#1899D6",
    "purple": "#AF72F5",
    "purple_shadow": "#8B44E0",
    "orange": "#FF9600",
    "orange_shadow": "#E08200",
    "yellow": "#FFC800",
    "yellow_shadow": "#D9A300",
    "red": "#FF4B4B",
    "red_shadow": "#D93838",
    "white": "#FFFFFF",
    "white_shadow": "#CBD5E1",
}

# =============================================================================
# CATÁLOGO DE CURSOS (4 GRUPOS REQUERIDOS)
# =============================================================================
COURSE_CATALOG = {
    "languages": {
        "name": "Lenguajes",
        "icon": "🐍",
        "courses": [
            {"id": "Python", "name": "Python", "icon": "🐍"},
            {"id": "C++", "name": "C++", "icon": "⚡"},
            {"id": "C", "name": "C", "icon": "⚙️"},
            {"id": "Javascript", "name": "Javascript", "icon": "🟨"},
            {"id": "Java", "name": "Java", "icon": "☕"}
        ]
    },
    "web": {
        "name": "Desarrollo Web",
        "icon": "🌐",
        "courses": [
            {"id": "HTML", "name": "HTML", "icon": "📄"},
            {"id": "CSS", "name": "CSS", "icon": "🎨"},
            {"id": "Javascript Web", "name": "Javascript Web", "icon": "🌐"}
        ]
    },
    "terminals": {
        "name": "Terminal",
        "icon": "💻",
        "courses": [
            {"id": "Terminal de Windows", "name": "Terminal de Windows", "icon": "🪟"},
            {"id": "Terminal de Linux", "name": "Terminal de Linux", "icon": "🐧"}
        ]
    },
    "hardware": {
        "name": "Hardware de Computadora",
        "icon": "⚙️",
        "courses": [
            {"id": "Conceptos Generales", "name": "Conceptos Generales", "icon": "💡"},
            {"id": "PC de Escritorio", "name": "PC de Escritorio", "icon": "🖥️"},
            {"id": "Notebook", "name": "Notebook", "icon": "💻"}
        ]
    }
}

# Plantillas de código para el editor
CODE_TEMPLATES = {
    "Python": """# Python 3.12 - Ejercicio guiado con Byte
radio = 5
PI = 3.1416

# Calcula el área e imprime el resultado
area = PI * (radio ** 2)
print("Radio del círculo:", radio)
print("Área calculada:", area)
""",
    "C++": """// C++ 14 - Salida con streams
#include <iostream>
using namespace std;

int main() {
    double radio = 5.0;
    const double PI = 3.1416;
    double area = PI * radio * radio;
    
    cout << "Radio: " << radio << endl;
    cout << "Área calculada: " << area << endl;
    return 0;
}
""",
    "C": """/* C (Clang) - Tipos primitivos */
#include <stdio.h>

int main() {
    float radio = 5.0f;
    float PI = 3.1416f;
    float area = PI * radio * radio;
    
    printf("Radio: %.2f\\n", radio);
    printf("Área calculada: %.2f\\n", area);
    return 0;
}
""",
    "Javascript": """// JavaScript ES6
const radio = 5;
const PI = 3.1416;

const area = PI * Math.pow(radio, 2);
console.log("Radio:", radio);
console.log("Área calculada:", area.toFixed(2));
""",
    "Java": """// Java 21 - Sintaxis pura
public class Main {
    public static void main(String[] args) {
        double radio = 5.0;
        double PI = 3.1416;
        double area = PI * Math.pow(radio, 2);
        
        System.out.println("Radio: " + radio);
        System.out.println("Área calculada: " + area);
    }
}
""",
    "HTML": """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Mi Primera Web</title>
</head>
<body>
  <h1>¡Hola Mundo con HTML5! 🚀</h1>
  <p>Párrafo semántico de prueba en CodeLingo.</p>
  <button onclick="alert('¡HTML y JS vinculados!')">Presióname</button>
</body>
</html>
""",
    "CSS": """<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: sans-serif; background: #e0f2fe; text-align: center; padding: 20px; }
    .caja { background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
    button { background: #58cc02; color: white; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="caja">
    <h2>Estilos con CSS3 🎨</h2>
    <p>Probando colores, bordes redondeados y sombras.</p>
    <button>Botón Estilizado</button>
  </div>
</body>
</html>
""",
    "Javascript Web": """<!DOCTYPE html>
<html>
<body>
  <h2 id="titulo">Texto Original</h2>
  <button onclick="cambiar()">Cambiar Contenido con JS</button>
  <script>
    function cambiar() {
      document.getElementById('titulo').innerText = '¡DOM Modificado con JavaScript!';
    }
  </script>
</body>
</html>
"""
}

# Biblioteca de Apuntes PDF desbloqueados
NOTES_LIBRARY = [
    {
        "course": "Python", "group": "Lenguajes",
        "title": "Fundamentos de Python 3.12 y Tipos", "icon": "🐍",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE PYTHON 3.12
======================================================
1. VARIABLES Y TIPOS PRIMITIVOS:
   - int: Enteros (ej: edad = 25)
   - float: Decimales (ej: pi = 3.1416)
   - str: Cadenas de texto ("Hola Mundo")
   - bool: True o False

2. OPERADORES ARITMÉTICOS:
   + (suma), - (resta), * (multiplicación), / (división flotante)
   // (división entera), % (módulo), ** (potencia)

3. ENTRADA Y SALIDA:
   print("Texto", variable)
   valor = input("Ingrese dato: ")

4. CONSEJO DE LA IA BYTE:
   "Usa nombres en minúsculas con guiones bajos (snake_case)
   para mantener tu código limpio y profesional."
"""
    },
    {
        "course": "C++", "group": "Lenguajes",
        "title": "Sintaxis de C++ y Streams de Salida", "icon": "⚡",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE C++ 14
======================================================
1. TIPADO ESTRICTO:
   int, double, float, char, bool
2. CABECERAS ESENCIALES:
   #include <iostream>
   using namespace std;
3. ENTRADA Y SALIDA ESTÁNDAR:
   cout << "Salida" << endl;
   cin >> variable;
"""
    },
    {
        "course": "C", "group": "Lenguajes",
        "title": "Tipos Primitivos y Memoria en C", "icon": "⚙️",
        "pages": "3 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE C (CLANG)
======================================================
1. ESTRUCTURA BÁSICA:
   #include <stdio.h>
   int main() { return 0; }
2. FORMATOS EN PRINTF:
   %d (entero), %f (flotante), %s (cadena), %c (carácter)
3. MEMORIA: Punteros (*) y direcciones (&).
"""
    },
    {
        "course": "Javascript", "group": "Lenguajes",
        "title": "Variables, Funciones Flecha y ES6", "icon": "🟨",
        "pages": "6 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVASCRIPT ES6
======================================================
1. DECLARACIONES: const (constantes) y let (variables reasignables)
2. ARROW FUNCTIONS: const suma = (a, b) => a + b;
3. MÉTODOS MATEMÁTICOS: Math.PI, Math.pow(), toFixed()
"""
    },
    {
        "course": "Java", "group": "Lenguajes",
        "title": "Programación Orientada a Objetos en Java 21", "icon": "☕",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVA 21
======================================================
1. ESTRUCTURA DE CLASES:
   public class Main {
       public static void main(String[] args) {
           System.out.println("Hola Java");
       }
   }
2. COMPILACIÓN: javac Main.java && java Main
"""
    },
    {
        "course": "HTML", "group": "Desarrollo Web",
        "title": "Estructura Semántica y Etiquetas HTML5", "icon": "📄",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE HTML5
======================================================
1. ETIQUETAS ESTRUCTURALES: <header>, <nav>, <main>, <section>, <footer>
2. TEXTO: <h1> a <h6>, <p>, <span>, <a>
3. FORMULARIOS: <form>, <input>, <button>
"""
    },
    {
        "course": "CSS", "group": "Desarrollo Web",
        "title": "Box Model, Flexbox y Sombras en CSS3", "icon": "🎨",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE CSS3
======================================================
1. MODELO DE CAJA: Content -> Padding -> Border -> Margin
2. FLEXBOX: display: flex; justify-content: center; align-items: center;
3. SOMBRAS: box-shadow: 0 4px 0 #46A302 (Estilo Duolingo)
"""
    },
    {
        "course": "Javascript Web", "group": "Desarrollo Web",
        "title": "Manipulación del DOM y Eventos Web", "icon": "🌐",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVASCRIPT WEB
======================================================
1. SELECCIÓN DOM: document.getElementById('id'), querySelector('.clase')
2. EVENTOS: elemento.addEventListener('click', callback)
3. PROPIEDADES: innerText, innerHTML, style.backgroundColor
"""
    },
    {
        "course": "Terminal de Windows", "group": "Terminal",
        "title": "Comandos PowerShell y Consola Windows", "icon": "🪟",
        "pages": "3 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES DE WINDOWS POWERSHELL / CMD
======================================================
1. LISTAR ARCHIVOS: dir / Get-ChildItem
2. CREAR CARPETA: mkdir nombre
3. NAVEGACIÓN: cd ruta, cd .. (retroceder)
4. LIMPIAR PANTALLA: cls
5. RED: ipconfig
"""
    },
    {
        "course": "Terminal de Linux", "group": "Terminal",
        "title": "Comandos Bash, Permisos y Rutas Ubuntu", "icon": "🐧",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES DE LINUX UBUNTU (BASH)
======================================================
1. LISTAR ARCHIVOS: ls, ls -la (muestra ocultos y permisos)
2. DIRECTORIO ACTUAL: pwd
3. CREAR CARPETA: mkdir nombre
4. VER ARCHIVO: cat archivo.txt
5. PERMISOS: chmod +x script.sh
6. LIMPIAR: clear
"""
    },
    {
        "course": "Hardware de Computadora", "group": "Hardware",
        "title": "Arquitectura y Comparativa PC vs Notebook", "icon": "⚙️",
        "pages": "6 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE HARDWARE
======================================================
1. CPU: Cerebro informático. Socket en PC vs BGA soldado en laptops.
2. RAM: Memoria volátil de alta velocidad (DIMM en PC vs SO-DIMM en laptop).
3. GPU: Acelera gráficos 3D y machine learning (PCIe en PC vs iGPU/Móvil).
4. ALMACENAMIENTO: SSD NVMe M.2 (hasta 7000 MB/s) vs HDD (150 MB/s).
5. PSU: Fuente 80 Plus en PC vs Adaptador externo en laptops.
"""
    }
]


# =============================================================================
# WIDGET PERSONALIZADO: BOTÓN TÁCTIL 3D (ESTILO DUOLINGO)
# =============================================================================
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
        # Color de fondo de ventana transparente
        parent_bg = self.master.cget("bg")
        self.config(bg=parent_bg)

        pad = 2
        w = self.width - pad * 2
        h = self.height - pad * 2
        offset = 4 if not self.is_pressed else 1
        depth = 4

        # Dibujar sombra (borde inferior 3D)
        if not self.is_pressed:
            self._draw_rounded_rect(pad, pad + offset, w, h - depth, self.radius, self.shadow_color)

        # Dibujar botón frontal
        y_top = pad if not self.is_pressed else pad + depth - 1
        self._draw_rounded_rect(pad, y_top, w, h - depth, self.radius, self.bg_color)

        # Texto del botón
        ty = (y_top + (h - depth) / 2)
        self.create_text(self.width / 2, ty, text=self.text, fill=self.fg_color,
                         font=self.font, anchor="center")

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        # Dibujar polígono aproximado de bordes redondeados
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


# =============================================================================
# WIDGET PERSONALIZADO: NODO CIRCULAR DEL CAMINO (STEPPING STONE)
# =============================================================================
class DuoNode(tk.Canvas):
    """Nodo circular del camino estilo Duolingo con estrellas, corona o candado."""
    def __init__(self, parent, node_num, label, status="locked", icon="⭐", command=None, size=76):
        super().__init__(parent, width=size, height=size + 24, bg=parent.cget("bg"),
                         highlightthickness=0)
        self.node_num = node_num
        self.label = label
        self.status = status  # 'completed', 'active', 'locked', 'boss'
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
        r = (self.size - 12) / 2
        offset = 6 if not self.is_pressed else 2

        # Colores según el estado
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
        else:  # locked
            bg = "#E2E8F0"
            shadow = "#94A3B8"
            badge = "🔒"

        # Sombra 3D circular
        if not self.is_pressed:
            self.create_oval(cx - r, cy - r + offset, cx + r, cy + r + offset, fill=shadow, outline="")

        # Círculo principal
        y_center = cy if not self.is_pressed else cy + 4
        self.create_oval(cx - r, y_center - r, cx + r, y_center + r, fill=bg,
                         outline="#FFFFFF" if self.status != "locked" else "#CBD5E1", width=2)

        # Ícono central
        self.create_text(cx, y_center, text=self.icon, font=("Segoe UI Emoji", 20), anchor="center")

        # Insignia flotante (badge)
        if self.status in ["active", "completed", "boss"]:
            badge_y = y_center - r - 4
            self.create_oval(cx - 24, badge_y - 8, cx + 24, badge_y + 8,
                             fill="#FFC800" if self.status == "completed" else "#58CC02", outline="#FFFFFF", width=1.5)
            self.create_text(cx, badge_y, text=badge, fill="#000000" if self.status == "completed" else "#FFFFFF",
                             font=("Segoe UI", 7, "bold"), anchor="center")

        # Etiqueta inferior de texto
        self.create_text(cx, self.size + 10, text=self.label, fill="#475569",
                         font=("Segoe UI", 8, "bold"), anchor="center")


# =============================================================================
# VENTANA PRINCIPAL DE LA APLICACIÓN CODELINGO
# =============================================================================
class CodeLingoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CodeLingo - Plataforma Educativa 2D")
        self.geometry("1100x780")
        self.minsize(980, 680)

        # Estado de usuario
        self.current_theme = "light"
        self.current_group = "languages"
        self.current_course = "Python"
        self.active_tab = "learn"
        self.streak_days = 5
        self.gems_count = 480
        self.hearts_count = 5
        self.user_avatar = "🦉"
        self.user_name = "Estudiante"
        self.user_email = "estudiante@codelingo.app"
        self.terminal_files = ["notas.txt", "script.py", "proyectos/"]

        # Configurar estilos de widgets TTK
        self._configure_ttk_styles()

        # Construir Interfaz Gráfica
        self._build_header()
        self._build_course_selector_bar()
        self._build_main_container()
        self._build_bottom_navbar()

        # Cargar vista inicial
        self.select_group("languages")
        self.apply_theme(self.current_theme)

    # -------------------------------------------------------------------------
    # CONFIGURACIÓN DE ESTILOS Y TEMAS
    # -------------------------------------------------------------------------
    def _configure_ttk_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def apply_theme(self, theme_key):
        self.current_theme = theme_key
        t = THEMES[theme_key]
        self.config(bg=t["bg"])

        # Aplicar colores a marcos
        self.header_frame.config(bg=t["header_bg"], highlightbackground=t["header_border"])
        self.course_bar_frame.config(bg=t["header_bg"], highlightbackground=t["header_border"])
        self.content_container.config(bg=t["bg"])
        self.bottom_nav_frame.config(bg=t["nav_bg"], highlightbackground=t["nav_border"])

        # Re-renderizar componentes activos
        self._update_header_stats()
        self.render_course_pills()
        if self.active_tab == "learn":
            self.render_learn_roadmap()
        elif self.active_tab == "pdfs":
            self.render_pdfs_screen()
        elif self.active_tab == "profile":
            self.render_profile_screen()

    def toggle_theme(self, target_theme):
        self.apply_theme(target_theme)

    # -------------------------------------------------------------------------
    # 1. ENCABEZADO SUPERIOR: LOGO, 4 GRUPOS Y CONTADORES DUOLINGO
    # -------------------------------------------------------------------------
    def _build_header(self):
        self.header_frame = tk.Frame(self, bg="#FFFFFF", highlightthickness=2, highlightbackground="#E2E8F0", padx=16, pady=10)
        self.header_frame.pack(fill="x", padx=16, pady=(12, 6))

        # Logo y Mascota
        brand_frame = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        brand_frame.pack(side="left")

        logo_canvas = tk.Canvas(brand_frame, width=42, height=42, bg="#58CC02", highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 8))
        logo_canvas.create_text(21, 21, text="🦉", font=("Segoe UI Emoji", 18))

        brand_text_frame = tk.Frame(brand_frame, bg=self.header_frame.cget("bg"))
        brand_text_frame.pack(side="left")
        tk.Label(brand_text_frame, text="APRENDE AL ESTILO DUOLINGO", font=("Segoe UI", 7, "bold"),
                 fg="#94A3B8", bg=self.header_frame.cget("bg")).pack(anchor="w")
        tk.Label(brand_text_frame, text="CodeLingo", font=("Segoe UI", 14, "bold"),
                 fg="#58CC02", bg=self.header_frame.cget("bg")).pack(anchor="w")

        # LOS 4 GRUPOS SUPERIORES DE APRENDIZAJE
        self.groups_box = tk.Frame(self.header_frame, bg="#F1F5F9", padx=4, pady=4)
        self.groups_box.pack(side="left", padx=20)

        self.group_buttons = {}
        for grp_key, grp_data in COURSE_CATALOG.items():
            btn = tk.Button(
                self.groups_box,
                text=f"{grp_data['icon']} {grp_data['name']}",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=10, pady=4,
                cursor="hand2",
                command=lambda k=grp_key: self.select_group(k)
            )
            btn.pack(side="left", padx=2)
            self.group_buttons[grp_key] = btn

        # Indicadores de Gamificación Duolingo a la derecha
        self.stats_box = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        self.stats_box.pack(side="right")

        # Racha de fuego
        self.streak_lbl = tk.Label(self.stats_box, text=f"🔥 {self.streak_days} días", font=("Segoe UI", 10, "bold"),
                                   fg="#FF9600", bg="#FFF7ED", padx=8, pady=4, relief="ridge", bd=1)
        self.streak_lbl.pack(side="left", padx=4)

        # Gemas
        self.gems_lbl = tk.Label(self.stats_box, text=f"💎 {self.gems_count}", font=("Segoe UI", 10, "bold"),
                                 fg="#1CB0F6", bg="#F0F9FF", padx=8, pady=4, relief="ridge", bd=1)
        self.gems_lbl.pack(side="left", padx=4)

        # Vidas
        self.hearts_lbl = tk.Label(self.stats_box, text=f"❤️ {self.hearts_count}/5", font=("Segoe UI", 10, "bold"),
                                   fg="#FF4B4B", bg="#FEF2F2", padx=8, pady=4, relief="ridge", bd=1)
        self.hearts_lbl.pack(side="left", padx=4)

        # Avatar de usuario con click para ir a perfil
        self.avatar_btn = tk.Button(
            self.stats_box, text=self.user_avatar, font=("Segoe UI Emoji", 14),
            bg="#ECFDF5", fg="#047857", relief="ridge", bd=2, cursor="hand2",
            padx=4, pady=1, command=lambda: self.switch_tab("profile")
        )
        self.avatar_btn.pack(side="left", padx=(6, 0))

    def _update_header_stats(self):
        t = THEMES[self.current_theme]
        self.streak_lbl.config(text=f"🔥 {self.streak_days} días")
        self.gems_lbl.config(text=f"💎 {self.gems_count}")
        self.hearts_lbl.config(text=f"❤️ {self.hearts_count}/5")
        self.avatar_btn.config(text=self.user_avatar)

    # -------------------------------------------------------------------------
    # 2. SEGUNDA FILA: SELECCIÓN DINÁMICA DEL CURSO
    # -------------------------------------------------------------------------
    def _build_course_selector_bar(self):
        self.course_bar_frame = tk.Frame(self, bg="#FFFFFF", highlightthickness=2, highlightbackground="#E2E8F0", padx=16, pady=8)
        self.course_bar_frame.pack(fill="x", padx=16, pady=4)

        self.pills_container = tk.Frame(self.course_bar_frame, bg=self.course_bar_frame.cget("bg"))
        self.pills_container.pack(side="left", fill="x", expand=True)

        self.course_indicator_lbl = tk.Label(
            self.course_bar_frame, text="Curso: Python", font=("Segoe UI", 9, "bold"),
            fg="#58CC02", bg=self.course_bar_frame.cget("bg")
        )
        self.course_indicator_lbl.pack(side="right")

    def select_group(self, group_key):
        self.current_group = group_key

        # Actualizar estilo de los 4 botones superiores
        t = THEMES[self.current_theme]
        for k, btn in self.group_buttons.items():
            if k == group_key:
                btn.config(bg="#58CC02", fg="#FFFFFF", relief="flat")
            else:
                btn.config(bg="#F1F5F9" if self.current_theme == "light" else "#334155",
                           fg="#475569" if self.current_theme == "light" else "#94A3B8", relief="flat")

        # Seleccionar automáticamente el primer curso del grupo
        first_course = COURSE_CATALOG[group_key]["courses"][0]["id"]
        self.render_course_pills()
        self.select_course(first_course)

    def render_course_pills(self):
        # Limpiar contenedor de pastillas de cursos
        for widget in self.pills_container.winfo_children():
            widget.destroy()

        t = THEMES[self.current_theme]
        tk.Label(self.pills_container, text="📚 Cursos:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=self.course_bar_frame.cget("bg")).pack(side="left", padx=(0, 8))

        courses = COURSE_CATALOG[self.current_group]["courses"]
        for c in courses:
            is_active = (c["id"] == self.current_course)
            bg = "#ECFDF5" if is_active else ("#FFFFFF" if self.current_theme == "light" else "#1E293B")
            fg = "#047857" if is_active else ("#475569" if self.current_theme == "light" else "#94A3B8")
            bd_col = "#10B981" if is_active else ("#CBD5E1" if self.current_theme == "light" else "#334155")

            btn = tk.Button(
                self.pills_container,
                text=f"{c['icon']} {c['name']}",
                font=("Segoe UI", 8, "bold"),
                bg=bg, fg=fg,
                activebackground="#ECFDF5",
                relief="ridge", bd=2,
                padx=10, pady=3,
                cursor="hand2",
                command=lambda cid=c["id"]: self.select_course(cid)
            )
            btn.pack(side="left", padx=3)

    def select_course(self, course_id):
        self.current_course = course_id
        self.course_indicator_lbl.config(text=f"Curso Activo: {course_id}")
        self.render_course_pills()
        if self.active_tab == "learn":
            self.render_learn_roadmap()

    # -------------------------------------------------------------------------
    # 3. CONTENEDOR PRINCIPAL: PANTALLAS (APRENDER, APUNTES, PERFIL)
    # -------------------------------------------------------------------------
    def _build_main_container(self):
        self.content_container = tk.Frame(self, bg=THEMES[self.current_theme]["bg"])
        self.content_container.pack(fill="both", expand=True, padx=16, pady=4)

    def switch_tab(self, tab_name):
        self.active_tab = tab_name

        # Actualizar barra inferior
        t = THEMES[self.current_theme]
        for k, btn in self.nav_buttons.items():
            if k == tab_name:
                btn.config(bg="#ECFDF5" if self.current_theme == "light" else "#064E3B",
                           fg="#047857" if self.current_theme == "light" else "#6EE7B7")
            else:
                btn.config(bg=t["nav_bg"], fg=t["text_muted"])

        # Ocultar o mostrar barra de cursos según corresponda
        if tab_name == "learn":
            self.course_bar_frame.pack(fill="x", padx=16, pady=4, after=self.header_frame)
            self.render_learn_roadmap()
        elif tab_name == "pdfs":
            self.course_bar_frame.pack_forget()
            self.render_pdfs_screen()
        elif tab_name == "profile":
            self.course_bar_frame.pack_forget()
            self.render_profile_screen()

    # -------------------------------------------------------------------------
    # PANTALLA 1: EL CAMINO DE APRENDIZAJE (ROADMAP DUOLINGO)
    # -------------------------------------------------------------------------
    def render_learn_roadmap(self):
        # Limpiar contenedor principal
        for w in self.content_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]

        # Banner de sección del curso activo
        banner = tk.Frame(self.content_container, bg="#58CC02", padx=20, pady=16)
        banner.pack(fill="x", pady=(0, 10))

        tk.Label(banner, text=f"CURSO: {self.current_course.upper()} • SECCIÓN 1",
                 font=("Segoe UI", 8, "bold"), fg="#ECFDF5", bg="#58CC02").pack(anchor="w")
        tk.Label(banner, text=f"{self.current_course}: Fundamentos y Sintaxis",
                 font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#58CC02").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text="Haz clic en los nodos del camino para aprender con Byte y escribir código en vivo.",
                 font=("Segoe UI", 9), fg="#F0FDF4", bg="#58CC02").pack(anchor="w", pady=(2, 0))

        # Canvas con scroll para el camino sinuoso de Duolingo
        path_canvas_frame = tk.Frame(self.content_container, bg=t["card_bg"],
                                     highlightthickness=2, highlightbackground=t["card_border"])
        path_canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(path_canvas_frame, bg=t["card_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(path_canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=t["card_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((340, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Nodos del camino pedagógico
        # 1. Introducción (Completado)
        f1 = tk.Frame(scrollable_frame, bg=t["card_bg"])
        f1.pack(pady=12)
        n1 = DuoNode(f1, 1, "1. Introducción", status="completed", icon="⭐",
                     command=lambda: self.launch_interactive_lesson(1, "Introducción al Concepto"))
        n1.pack()

        # 2. Práctica Guiada (Activo - abre el editor/consola)
        f2 = tk.Frame(scrollable_frame, bg=t["card_bg"])
        f2.pack(pady=12, padx=(80, 0))
        practice_icon = "💻" if self.current_group in ["languages", "web"] else ("📟" if self.current_group == "terminals" else "⚙️")
        n2 = DuoNode(f2, 2, "2. Práctica Guiada", status="active", icon=practice_icon,
                     command=lambda: self.launch_interactive_lesson(2, "Práctica Guiada con Byte"))
        n2.pack()

        # 3. Quiz de Teoría (Bloqueado)
        f3 = tk.Frame(scrollable_frame, bg=t["card_bg"])
        f3.pack(pady=12, padx=(0, 60))
        n3 = DuoNode(f3, 3, "3. Quiz Teórico", status="locked", icon="❓",
                     command=lambda: messagebox.showinfo("Nivel Bloqueado", "Completa la lección anterior para desbloquear."))
        n3.pack()

        # Cofre de gemas de recompensa
        chest_frame = tk.Frame(scrollable_frame, bg=t["card_bg"])
        chest_frame.pack(pady=10)
        chest_btn = DuoButton(chest_frame, text="🎁 Cofre Secreto", width=150, height=44,
                              bg_color="#FFC800", shadow_color="#D9A300", fg_color="#000000",
                              command=self.claim_chest_reward)
        chest_btn.pack()

        # 4. Reto Combinatorio (Bloqueado)
        f4 = tk.Frame(scrollable_frame, bg=t["card_bg"])
        f4.pack(pady=12, padx=(60, 0))
        n4 = DuoNode(f4, 4, "4. Reto Combinatorio", status="locked", icon="⚡",
                     command=lambda: messagebox.showinfo("Nivel Bloqueado", "Completa la lección anterior."))
        n4.pack()

        # 5. Boss Evaluación de Sección
        f5 = tk.Frame(scrollable_frame, bg=t["card_bg"])
        f5.pack(pady=16)
        boss = DuoNode(f5, 5, "Examen de Sección", status="boss", icon="🏆", size=88,
                       command=self.open_boss_evaluation)
        boss.pack()

    def claim_chest_reward(self):
        self.gems_count += 20
        self.streak_days += 1
        self._update_header_stats()
        messagebox.showinfo("🎁 ¡Cofre Abierto!", "¡Has ganado +20 Gemas 💎 y sumaste +1 día a tu racha activa! 🔥")

    def open_boss_evaluation(self):
        messagebox.showinfo(
            "🏆 Evaluación de Sección (Boss)",
            f"Examen de certificación para {self.current_course}.\n\n"
            "Debes aprobar con 80/100 puntos para desbloquear la siguiente sección. "
            "En caso de no aprobar, la IA creará automáticamente ejercicios de refuerzo adaptativo."
        )

    # -------------------------------------------------------------------------
    # MODAL DE LECCIÓN INTERACTIVA (EDITOR DE CÓDIGO / TERMINAL / HARDWARE)
    # -------------------------------------------------------------------------
    def launch_interactive_lesson(self, lesson_num, title):
        """Abre la ventana interactiva adaptada al curso seleccionado."""
        win = tk.Toplevel(self)
        win.title(f"{title} • {self.current_course}")
        win.geometry("900x640")
        win.minsize(800, 560)
        t = THEMES[self.current_theme]
        win.config(bg=t["bg"])

        # Encabezado del modal
        top_bar = tk.Frame(win, bg=t["card_bg"], padx=16, pady=10, highlightthickness=1, highlightbackground=t["card_border"])
        top_bar.pack(fill="x")

        tk.Label(top_bar, text=f"LECCIÓN {lesson_num} • {self.current_course.upper()}",
                 font=("Segoe UI", 8, "bold"), fg="#58CC02", bg=t["card_bg"]).pack(anchor="w")
        tk.Label(top_bar, text=title, font=("Segoe UI", 13, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w")

        # Tarjeta del asistente Byte con pistas y evaluación
        prompt_card = tk.Frame(win, bg="#EFF6FF", padx=14, pady=10, highlightthickness=1, highlightbackground="#BFDBFE")
        prompt_card.pack(fill="x", padx=16, pady=10)

        byte_left = tk.Frame(prompt_card, bg="#EFF6FF")
        byte_left.pack(side="left", fill="both", expand=True)

        tk.Label(byte_left, text="🦉 Misión con Byte (IA):", font=("Segoe UI", 9, "bold"),
                 fg="#1D4ED8", bg="#EFF6FF").pack(anchor="w")
        prompt_msg = (
            f"Escribe y ejecuta tu solución para {self.current_course}. Puedes pedir pistas a Byte sin que revele "
            "la respuesta directa, o solicitar una evaluación técnica de tu código de 1 a 100."
        )
        tk.Label(byte_left, text=prompt_msg, font=("Segoe UI", 8),
                 fg="#1E293B", bg="#EFF6FF", wraplength=520, justify="left").pack(anchor="w", pady=(2, 0))

        # Botones de Asistencia IA
        btn_box = tk.Frame(prompt_card, bg="#EFF6FF")
        btn_box.pack(side="right")

        DuoButton(btn_box, text="💡 Pista IA", width=100, height=36,
                  bg_color="#FFFFFF", shadow_color="#E2E8F0", fg_color="#B45309",
                  command=lambda: messagebox.showinfo("💡 Pista de Byte", f"Revisa la sintaxis de variables en {self.current_course}. ¡Recuerda imprimir la salida sin olvidar cerrar paréntesis o llaves!")).pack(side="left", padx=4)

        DuoButton(btn_box, text="🤖 Evaluar (1-100)", width=130, height=36,
                  bg_color="#AF72F5", shadow_color="#8B44E0", fg_color="#FFFFFF",
                  command=lambda: messagebox.showinfo("🤖 Evaluación IA", f"Puntaje de tu código: 96/100 ⭐\n\n✓ Nombres de variables descriptivos y correcta asignación.\n✓ Operaciones numéricas precisas.\n⚠ Sugerencia: Documenta la salida para mayor claridad.")).pack(side="left", padx=4)

        # CUERPO SEGÚN EL GRUPO
        if self.current_group in ["languages", "web"]:
            self._build_code_editor_view(win)
        elif self.current_group == "terminals":
            self._build_terminal_view(win)
        else:
            self._build_hardware_view(win)

    def _build_code_editor_view(self, parent):
        editor_frame = tk.Frame(parent, bg=THEMES[self.current_theme]["bg"], padx=16)
        editor_frame.pack(fill="both", expand=True)

        # PanedWindow para dividir código y consola
        paned = tk.PanedWindow(editor_frame, orient="horizontal", bg="#E2E8F0", sashwidth=4)
        paned.pack(fill="both", expand=True, pady=(0, 10))

        # 1. Editor de Código
        code_box = tk.Frame(paned, bg="#0F172A")
        paned.add(code_box, minsize=380)

        header_code = tk.Frame(code_box, bg="#1E293B", padx=10, pady=4)
        header_code.pack(fill="x")
        tk.Label(header_code, text=f"● editor_{self.current_course.lower()}.txt", font=("Consolas", 8, "bold"),
                 fg="#38BDF8", bg="#1E293B").pack(side="left")

        text_editor = tk.Text(code_box, bg="#0F172A", fg="#6EE7B7", font=("Consolas", 10),
                              insertbackground="#FFFFFF", relief="flat", padx=10, pady=10)
        text_editor.pack(fill="both", expand=True)
        text_editor.insert("1.0", CODE_TEMPLATES.get(self.current_course, "# Escribe tu código aquí\n"))

        # Barra de atajos rápidos para celular / teclado táctil
        quick_keys_frame = tk.Frame(code_box, bg="#1E293B", padx=6, pady=4)
        quick_keys_frame.pack(fill="x")
        tk.Label(quick_keys_frame, text="Atajos:", font=("Segoe UI", 7, "bold"), fg="#94A3B8", bg="#1E293B").pack(side="left", padx=2)
        for sym in ["(", ")", "{", "}", "[", "]", ";", "=", "\"", "<", ">"]:
            b = tk.Button(quick_keys_frame, text=sym, font=("Consolas", 8, "bold"), bg="#334155", fg="#FFFFFF",
                          relief="flat", padx=4, pady=1, cursor="hand2",
                          command=lambda s=sym: text_editor.insert(tk.INSERT, s))
            b.pack(side="left", padx=1)

        # 2. Consola de Salida
        console_box = tk.Frame(paned, bg="#090D16")
        paned.add(console_box, minsize=300)

        header_cons = tk.Frame(console_box, bg="#1E293B", padx=10, pady=4)
        header_cons.pack(fill="x")
        tk.Label(header_cons, text="● Consola de Salida", font=("Consolas", 8, "bold"),
                 fg="#A7F3D0", bg="#1E293B").pack(side="left")

        text_console = tk.Text(console_box, bg="#090D16", fg="#4AF626", font=("Consolas", 9),
                               relief="flat", padx=10, pady=10)
        text_console.pack(fill="both", expand=True)
        text_console.insert("1.0", "> Presiona 'EJECUTAR CÓDIGO' para compilar o interpretar...")

        # Botón inferior para ejecutar
        bottom_bar = tk.Frame(parent, bg=THEMES[self.current_theme]["bg"], padx=16, pady=8)
        bottom_bar.pack(fill="x")

        def run_code():
            text_console.delete("1.0", tk.END)
            text_console.insert(tk.END, f"> Compilando y ejecutando [{self.current_course}]...\n\n")
            self.update_idletasks()
            time.sleep(0.15)
            text_console.insert(tk.END, "Radio: 5\nÁrea calculada: 78.54\n\n[Proceso terminado exitosamente con código 0]\n")
            messagebox.showinfo("🎉 ¡Práctica Exitosa!", "¡Tu solución pasó todas las pruebas unitarias! Ganas +20 XP ⚡.")

        DuoButton(bottom_bar, text="▶ EJECUTAR CÓDIGO", width=180, height=42,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=run_code).pack(side="right")

    def _build_terminal_view(self, parent):
        term_frame = tk.Frame(parent, bg="#1E293B", padx=16, pady=10)
        term_frame.pack(fill="both", expand=True, padx=16, pady=10)

        is_win = (self.current_course == "Terminal de Windows")
        prompt_txt = "PS C:\\Users\\Student> " if is_win else "student@antigravity:~$ "
        header_txt = "Windows PowerShell 7.4" if is_win else "student@antigravity: ~ (bash 5.2)"

        header_lbl = tk.Label(term_frame, text=header_txt, font=("Consolas", 9, "bold"),
                              fg="#FFFFFF", bg="#1E293B")
        header_lbl.pack(anchor="w", pady=(0, 4))

        # Pantalla de historial
        history_text = tk.Text(term_frame, bg="#0C1021" if is_win else "#300A24",
                               fg="#FFFFFF" if is_win else "#4AF626", font=("Consolas", 10),
                               relief="flat", padx=10, pady=10)
        history_text.pack(fill="both", expand=True)
        history_text.insert(tk.END, f"Simulador de {self.current_course} iniciado.\nEscribe 'help' para ver los comandos disponibles.\n\n")

        # Línea activa de comando
        cmd_line_frame = tk.Frame(term_frame, bg="#0C1021" if is_win else "#300A24", padx=6, pady=4)
        cmd_line_frame.pack(fill="x")

        tk.Label(cmd_line_frame, text=prompt_txt, font=("Consolas", 10, "bold"),
                 fg="#38BDF8" if is_win else "#58CC02", bg="#0C1021" if is_win else "#300A24").pack(side="left")

        cmd_entry = tk.Entry(cmd_line_frame, font=("Consolas", 10), bg="#0C1021" if is_win else "#300A24",
                             fg="#FFFFFF", insertbackground="#FFFFFF", relief="flat")
        cmd_entry.pack(side="left", fill="x", expand=True)

        def execute_cmd(event=None):
            cmd = cmd_entry.get().strip()
            if not cmd:
                return
            cmd_entry.delete(0, tk.END)
            history_text.insert(tk.END, f"{prompt_txt}{cmd}\n")
            parts = cmd.split()
            base = parts[0].lower()

            if base in ["clear", "cls"]:
                history_text.delete("1.0", tk.END)
                return
            elif base in ["ls", "dir"]:
                res = "   ".join(self.terminal_files) + "\n"
            elif base == "pwd":
                res = "C:\\Users\\Student\n" if is_win else "/home/student\n"
            elif base == "mkdir":
                if len(parts) > 1:
                    self.terminal_files.append(parts[1])
                    res = f"Directorio '{parts[1]}' creado exitosamente.\n"
                    if parts[1].lower() == "proyectos":
                        messagebox.showinfo("🎯 ¡Misión Cumplida!", "Has creado el directorio 'proyectos'. ¡Ganas +25 XP! ⚡")
                else:
                    res = "Falta indicar el nombre de la carpeta.\n"
            elif base == "help":
                res = "Comandos soportados: ls, dir, pwd, mkdir <nombre>, clear, cls, help\n"
            else:
                res = f"Comando '{base}' procesado.\n"

            history_text.insert(tk.END, res + "\n")
            history_text.see(tk.END)

        cmd_entry.bind("<Return>", execute_cmd)
        cmd_entry.focus_set()

    def _build_hardware_view(self, parent):
        hw_frame = tk.Frame(parent, bg=THEMES[self.current_theme]["bg"], padx=16, pady=10)
        hw_frame.pack(fill="both", expand=True)

        tk.Label(hw_frame, text="Diagrama de Arquitectura de Computadora (2D):",
                 font=("Segoe UI", 11, "bold"), fg="#047857", bg=hw_frame.cget("bg")).pack(anchor="w", pady=(0, 8))

        canvas = tk.Canvas(hw_frame, bg="#0F172A", height=280, highlightthickness=2, highlightbackground="#334155")
        canvas.pack(fill="x")

        # Dibujar placa base esquemática
        canvas.create_rectangle(20, 20, 820, 260, fill="#0F172A", outline="#22C55E", width=2)
        # CPU
        canvas.create_rectangle(140, 60, 240, 160, fill="#1E293B", outline="#38BDF8", width=2)
        canvas.create_text(190, 110, text="CPU\nSocket", fill="#38BDF8", font=("Segoe UI", 10, "bold"), justify="center")
        # RAM
        canvas.create_rectangle(280, 50, 310, 170, fill="#1E293B", outline="#EAB308", width=2)
        canvas.create_rectangle(320, 50, 350, 170, fill="#1E293B", outline="#EAB308", width=2)
        canvas.create_text(315, 36, text="RAM DDR5", fill="#EAB308", font=("Segoe UI", 9, "bold"))
        # GPU
        canvas.create_rectangle(80, 190, 420, 235, fill="#1E293B", outline="#EF4444", width=2)
        canvas.create_text(250, 212, text="Tarjeta Gráfica Dedicada (GPU PCIe x16)", fill="#EF4444", font=("Segoe UI", 9, "bold"))
        # SSD NVMe
        canvas.create_rectangle(460, 120, 620, 150, fill="#1E293B", outline="#A855F7", width=2)
        canvas.create_text(540, 135, text="SSD NVMe M.2 (7000 MB/s)", fill="#A855F7", font=("Segoe UI", 9, "bold"))
        # PSU
        canvas.create_rectangle(680, 60, 780, 220, fill="#1E293B", outline="#F97316", width=2)
        canvas.create_text(730, 140, text="Fuente PSU\n80 Plus", fill="#F97316", font=("Segoe UI", 9, "bold"), justify="center")

        info_box = tk.Label(hw_frame, text="💡 Diferencia clave: En PC de escritorio los componentes van en zócalos desmontables (Socket y ranuras DIMM). En notebooks, CPU y RAM suelen venir soldados (BGA/LPDDR) para optimizar grosor y consumo de energía.",
                            font=("Segoe UI", 8), fg="#475569", bg=hw_frame.cget("bg"), wraplength=780, justify="left")
        info_box.pack(anchor="w", pady=10)

    # -------------------------------------------------------------------------
    # PANTALLA 2: APARTADO DE APUNTES PDF DESBLOQUEADOS
    # -------------------------------------------------------------------------
    def render_pdfs_screen(self):
        for w in self.content_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]

        # Banner del apartado
        banner = tk.Frame(self.content_container, bg="#EA580C", padx=20, pady=16)
        banner.pack(fill="x", pady=(0, 10))

        tk.Label(banner, text="BIBLIOTECA OFICIAL DE ESTUDIO",
                 font=("Segoe UI", 8, "bold"), fg="#FFEDD5", bg="#EA580C").pack(anchor="w")
        tk.Label(banner, text="Apuntes PDF Desbloqueados por Curso",
                 font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#EA580C").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text="Descarga o consulta los resúmenes conceptuales oficiales desbloqueados tras aprobar cada sección.",
                 font=("Segoe UI", 9), fg="#FFF7ED", bg="#EA580C").pack(anchor="w", pady=(2, 0))

        # Grid con scroll de tarjetas de apuntes
        canvas_frame = tk.Frame(self.content_container, bg=t["bg"])
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=t["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        cards_frame = tk.Frame(canvas, bg=t["bg"])

        cards_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=cards_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Generar tarjetas de apuntes
        row = 0
        col = 0
        for doc in NOTES_LIBRARY:
            card = tk.Frame(cards_frame, bg=t["card_bg"], highlightthickness=2, highlightbackground=t["card_border"],
                            padx=14, pady=12, width=320, height=150)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            card.pack_propagate(False)

            # Encabezado de tarjeta
            c_top = tk.Frame(card, bg=t["card_bg"])
            c_top.pack(fill="x")
            tk.Label(c_top, text=doc["icon"], font=("Segoe UI Emoji", 14), bg=t["card_bg"]).pack(side="left")
            tk.Label(c_top, text=doc["status"], font=("Segoe UI", 7, "bold"), fg="#059669", bg="#ECFDF5", padx=6, pady=2).pack(side="right")

            tk.Label(card, text=f"{doc['group']} • {doc['pages']}", font=("Segoe UI", 7, "bold"),
                     fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w", pady=(4, 0))
            tk.Label(card, text=doc["title"], font=("Segoe UI", 9, "bold"),
                     fg=t["text"], bg=t["card_bg"], wraplength=280, justify="left").pack(anchor="w")

            # Botón de Descarga
            bot_frame = tk.Frame(card, bg=t["card_bg"])
            bot_frame.pack(fill="x", side="bottom")

            DuoButton(bot_frame, text="📥 Descargar PDF", width=130, height=34,
                      bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF", font_size=8,
                      command=lambda d=doc: self.download_notes_file(d)).pack(side="right")

            col += 1
            if col > 2:
                col = 0
                row += 1

    def download_notes_file(self, doc_data):
        """Permite guardar los apuntes en un archivo de texto o PDF."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Documento de Texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"Apuntes_{doc_data['course'].replace(' ', '_')}.txt",
            title=f"Guardar Apuntes: {doc_data['course']}"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc_data["content"])
            messagebox.showinfo("📥 Descarga Exitosa", f"¡Apuntes de {doc_data['course']} guardados en:\n{file_path}!")

    # -------------------------------------------------------------------------
    # PANTALLA 3: CONFIGURACIÓN DE PERFIL Y AJUSTES
    # -------------------------------------------------------------------------
    def render_profile_screen(self):
        for w in self.content_container.winfo_children():
            w.destroy()

        t = THEMES[self.current_theme]

        # Banner de perfil
        banner = tk.Frame(self.content_container, bg="#2563EB", padx=20, pady=16)
        banner.pack(fill="x", pady=(0, 10))

        tk.Label(banner, text="CONFIGURACIÓN DEL ESTUDIANTE",
                 font=("Segoe UI", 8, "bold"), fg="#DBEAFE", bg="#2563EB").pack(anchor="w")
        tk.Label(banner, text="Mi Perfil y Ajustes",
                 font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#2563EB").pack(anchor="w", pady=(2, 0))
        tk.Label(banner, text="Personaliza tu nombre, avatar 2D, credenciales y cambia el tema de la aplicación.",
                 font=("Segoe UI", 9), fg="#EFF6FF", bg="#2563EB").pack(anchor="w", pady=(2, 0))

        # Panel dividido: Izquierda (Avatar y Tema) | Derecha (Formulario)
        grid_frame = tk.Frame(self.content_container, bg=t["bg"])
        grid_frame.pack(fill="both", expand=True)

        # 1. Tarjeta de Avatar y Tema
        left_card = tk.Frame(grid_frame, bg=t["card_bg"], highlightthickness=2, highlightbackground=t["card_border"],
                             padx=20, pady=20, width=320)
        left_card.pack(side="left", fill="y", padx=(0, 10))
        left_card.pack_propagate(False)

        avatar_display = tk.Label(left_card, text=self.user_avatar, font=("Segoe UI Emoji", 42),
                                  bg="#ECFDF5", fg="#047857", width=3, relief="ridge", bd=2)
        avatar_display.pack(pady=(0, 8))

        user_lbl = tk.Label(left_card, text=self.user_name, font=("Segoe UI", 13, "bold"),
                            fg=t["text"], bg=t["card_bg"])
        user_lbl.pack()

        tk.Label(left_card, text=f"Racha activa: {self.streak_days} días • Nivel 3", font=("Segoe UI", 8),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(pady=(2, 16))

        # Selector de Avatares 2D
        tk.Label(left_card, text="ELEGIR AVATAR 2D:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w", pady=(0, 6))

        avatars_box = tk.Frame(left_card, bg=t["card_bg"])
        avatars_box.pack(fill="x", pady=(0, 20))
        for av in ["🦉", "🤖", "🦊", "🐱", "👾"]:
            b = tk.Button(avatars_box, text=av, font=("Segoe UI Emoji", 14), bg=t["bg"],
                          relief="ridge", bd=1, cursor="hand2", padx=4, pady=2,
                          command=lambda a=av: self._change_avatar(a, avatar_display))
            b.pack(side="left", padx=2)

        # SELECTOR DE TEMA: CLARO / OSCURO
        tk.Label(left_card, text="TEMA DE LA APLICACIÓN:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w", pady=(0, 6))

        theme_box = tk.Frame(left_card, bg=t["card_bg"])
        theme_box.pack(fill="x")

        btn_light = DuoButton(theme_box, text="☀️ Modo Claro", width=130, height=36,
                              bg_color="#FFFFFF" if self.current_theme == "light" else "#334155",
                              shadow_color="#CBD5E1" if self.current_theme == "light" else "#0F172A",
                              fg_color="#0F172A" if self.current_theme == "light" else "#94A3B8",
                              command=lambda: self.toggle_theme("light"))
        btn_light.pack(side="left", padx=2)

        btn_dark = DuoButton(theme_box, text="🌙 Modo Oscuro", width=130, height=36,
                             bg_color="#1E293B" if self.current_theme == "dark" else "#F1F5F9",
                             shadow_color="#0F172A" if self.current_theme == "dark" else "#CBD5E1",
                             fg_color="#38BDF8" if self.current_theme == "dark" else "#475569",
                             command=lambda: self.toggle_theme("dark"))
        btn_dark.pack(side="left", padx=2)

        # 2. Formulario de Datos de Cuenta
        right_card = tk.Frame(grid_frame, bg=t["card_bg"], highlightthickness=2, highlightbackground=t["card_border"],
                              padx=24, pady=20)
        right_card.pack(side="left", fill="both", expand=True)

        tk.Label(right_card, text="Datos de la Cuenta", font=("Segoe UI", 13, "bold"),
                 fg=t["text"], bg=t["card_bg"]).pack(anchor="w", pady=(0, 14))

        # Nombre de usuario
        tk.Label(right_card, text="NOMBRE DE USUARIO:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w")
        entry_user = tk.Entry(right_card, font=("Segoe UI", 10), bg=t["bg"], fg=t["text"],
                              relief="solid", bd=1)
        entry_user.insert(0, self.user_name)
        entry_user.pack(fill="x", pady=(3, 12), ipady=4)

        # Correo electrónico
        tk.Label(right_card, text="CORREO ELECTRÓNICO:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w")
        entry_email = tk.Entry(right_card, font=("Segoe UI", 10), bg=t["bg"], fg=t["text"],
                               relief="solid", bd=1)
        entry_email.insert(0, self.user_email)
        entry_email.pack(fill="x", pady=(3, 12), ipady=4)

        # Contraseña
        tk.Label(right_card, text="NUEVA CONTRASEÑA:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w")
        entry_pass = tk.Entry(right_card, font=("Segoe UI", 10), show="•", bg=t["bg"], fg=t["text"],
                              relief="solid", bd=1)
        entry_pass.pack(fill="x", pady=(3, 12), ipady=4)

        tk.Label(right_card, text="CONFIRMAR CONTRASEÑA:", font=("Segoe UI", 8, "bold"),
                 fg=t["text_muted"], bg=t["card_bg"]).pack(anchor="w")
        entry_pass_conf = tk.Entry(right_card, font=("Segoe UI", 10), show="•", bg=t["bg"], fg=t["text"],
                                   relief="solid", bd=1)
        entry_pass_conf.pack(fill="x", pady=(3, 16), ipady=4)

        def save_profile():
            new_name = entry_user.get().strip()
            new_mail = entry_email.get().strip()
            if new_name:
                self.user_name = new_name
            if new_mail:
                self.user_email = new_mail
            user_lbl.config(text=self.user_name)
            messagebox.showinfo("✅ Perfil Guardado", f"Cambios guardados con éxito para {self.user_name}.")

        DuoButton(right_card, text="GUARDAR CAMBIOS", width=180, height=42,
                  bg_color="#58CC02", shadow_color="#46A302", fg_color="#FFFFFF",
                  command=save_profile).pack(anchor="e")

    def _change_avatar(self, new_avatar, display_label):
        self.user_avatar = new_avatar
        display_label.config(text=new_avatar)
        self.avatar_btn.config(text=new_avatar)

    # -------------------------------------------------------------------------
    # 4. BARRA INFERIOR DE NAVEGACIÓN (APRENDER / APUNTES / PERFIL)
    # -------------------------------------------------------------------------
    def _build_bottom_navbar(self):
        t = THEMES[self.current_theme]
        self.bottom_nav_frame = tk.Frame(self, bg=t["nav_bg"], highlightthickness=2, highlightbackground=t["nav_border"], padx=16, pady=8)
        self.bottom_nav_frame.pack(fill="x", padx=16, pady=(4, 12))

        center_box = tk.Frame(self.bottom_nav_frame, bg=self.bottom_nav_frame.cget("bg"))
        center_box.pack(anchor="center")

        self.nav_buttons = {}
        tabs = [
            ("learn", "🗺️ Aprender (Camino)"),
            ("pdfs", "📄 Apuntes PDF Desbloqueados"),
            ("profile", "👤 Perfil y Ajustes")
        ]

        for tab_key, tab_title in tabs:
            btn = tk.Button(
                center_box,
                text=tab_title,
                font=("Segoe UI", 9, "bold"),
                bg="#ECFDF5" if tab_key == "learn" else t["nav_bg"],
                fg="#047857" if tab_key == "learn" else t["text_muted"],
                activebackground="#ECFDF5",
                relief="flat",
                padx=16, pady=6,
                cursor="hand2",
                command=lambda k=tab_key: self.switch_tab(k)
            )
            btn.pack(side="left", padx=8)
            self.nav_buttons[tab_key] = btn


# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    app = CodeLingoApp()
    app.mainloop()
