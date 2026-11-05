# 🦉 Apartado Visual - CodeLingo (Python 2D)

Interfaz gráfica completa en **Python** nativo con `tkinter` inspirada en la metodología y estética 2D de **Duolingo**.

---

## 🚀 Cómo Iniciar la Interfaz Visual

Puedes ejecutar la aplicación directamente con:

```powershell
python "C:\Users\alast\Downloads\app\apartado_visual\main.py"
```

O desde esta misma carpeta:

```powershell
cd "C:\Users\alast\Downloads\app\apartado_visual"
python main.py
```

---

## 📁 Estructura de Archivos en `apartado_visual`

- **`main.py`**: Aplicación gráfica principal que orquesta todas las vistas, ventanas modulares, estados y navegación.
- **`themes.py`**: Sistema de colores y paletas de **Modo Claro (☀️)** y **Modo Oscuro (🌙)**.
- **`widgets.py`**: Componentes 2D personalizados (`DuoButton` con relieve 3D táctil, `DuoNode` para los nodos del camino).
- **`courses_data.py`**: Estructura de los 4 grupos, cursos, plantillas de código y apuntes descargables.
- **`__init__.py`**: Inicializador del paquete para importaciones modulares.

---

## 🎨 Características Implementadas

1. **4 Grupos Principales en la barra superior:**
   - `🐍 Lenguajes` (Python, C++, C, Javascript, Java)
   - `🌐 Desarrollo Web` (HTML, CSS, Javascript Web)
   - `💻 Terminal` (Terminal de Windows, Terminal de Linux)
   - `⚙️ Hardware de Computadora` (Conceptos Generales, PC de Escritorio, Notebook)

2. **Segunda Fila Dinámica:** Las pastillas de cursos cambian automáticamente al seleccionar un grupo.

3. **El Camino de Aprendizaje (Duolingo Path):** Nodos circulares interactivos con coronas, estrellas, cofre de gemas y evaluación de sección (Boss).

4. **Entorno de Lección Integrado:** Se abre al pulsar cualquier lección activa:
   - Editor de código con resaltado y consola de ejecución.
   - Simulador interactivo de Terminal (Windows PowerShell / Linux Ubuntu Bash).
   - Laboratorio visual 2D de Hardware con componentes interactivos.
   - Asistente IA "Byte" con pistas progresivas y evaluador de 1 a 100.

5. **Apartado de Apuntes PDF Desbloqueados:** Biblioteca organizada con resúmenes descargables por curso.

6. **Apartado de Perfil y Ajustes:**
   - Cambio de tema en vivo (**Claro / Oscuro**).
   - Selector de avatar 2D (`🦉`, `🤖`, `🦊`, `🐱`, `👾`).
   - Edición de nombre de usuario, correo y contraseña.
