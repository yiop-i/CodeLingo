#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 CODELINGO - PLATAFORMA EDUCATIVA MULTI-DISPOSITIVO EN PYTHON
=============================================================================
Aplicación para aprender lenguajes de programación, terminales de sistemas operativos
y hardware de computadoras (PC y Notebook) inspirada en la metodología y estética 2D de Duolingo.

Características implementadas según especificación:
1. 12 Cursos completos organizados en 4 grupos:
   - Lenguajes: Python, C++, C, Javascript, Java
   - Desarrollo Web: HTML, CSS, Javascript Web
   - Terminal: Terminal de Windows, Terminal de Linux
   - Hardware: PC de Escritorio, Notebook
2. 4 Secciones progresivas por curso con mínimo 25 lecciones pedagógicas por sección
   (1,200+ lecciones en total) siguiendo el flujo didáctico estricto.
3. Entornos de práctica interactivos extraídos de la suite:
   - Editor de código multi-lenguaje con ejecución en vivo y consola.
   - Simuladores de terminal de Windows (PowerShell/CMD) y Linux (Ubuntu Bash) con VFS.
   - Laboratorio de hardware y diagnóstico de ranuras/componentes.
4. Asistente IA unificado ("Byte"):
   - Pistas inteligentes que guían sin revelar la respuesta directa.
   - Evaluador de código y comandos de 1 a 100 con desglose de fortalezas y mejoras.
   - Generación dinámica de niveles de refuerzo adaptativos al reprobar una evaluación.
5. Evaluaciones Boss de Sección:
   - Examen integral que evalúa todo lo visto hasta el momento.
   - Si se aprueba (>= 80%): Desbloquea la siguiente sección y genera el PDF oficial de apuntes.
   - Si no se aprueba: Se desbloquean niveles de refuerzo generados por la IA en dicha sección.
6. Soporte multi-curso simultáneo con persistencia automática en disco.
7. Generador de apuntes y resúmenes oficiales en PDF 1.4 estándar sin dependencias.
8. Servidor web multihilo local integrado para acceso desde celulares y tablets por Wi-Fi.
=============================================================================
"""

import sys
import os

# Asegurar importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def enable_high_dpi():
    """Activa el modo de alta definición (HiDPI) en Windows para evitar que se vea pixelado o borroso."""
    if sys.platform == "win32":
        try:
            import ctypes
            # Per-Monitor V2 DPI awareness context
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

def run_gui():
    enable_high_dpi()
    from gui_main import CodeLingoApp
    app = CodeLingoApp()
    app.mainloop()

def run_web(port=8080):
    from simulators_bridge import SimulatorsBridge
    bridge = SimulatorsBridge.get_instance()
    bridge.launch_mobile_web_server(port=port)
    print("Servidor web en ejecución. Presiona Ctrl+C para detener.")
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor detenido.")

def run_cli(mode="linux"):
    from simulators_bridge import SimulatorsBridge
    bridge = SimulatorsBridge.get_instance()
    os_type = "windows" if mode == "windows" else "linux"
    print("=" * 60)
    print(f"  CODELINGO - TERMINAL VIRTUAL CLI ({os_type.upper()})")
    print("  Escribe 'help' para comandos o 'exit' para salir.")
    print("=" * 60)

    while True:
        try:
            prompt = bridge.get_terminal_prompt(os_type)
            cmd = input(prompt).strip()
            if cmd.lower() in ["exit", "quit"]:
                break
            if cmd:
                out = bridge.execute_terminal_cmd(cmd, os_type)
                if out:
                    print(out)
        except (KeyboardInterrupt, EOFError):
            print("\nSesión terminada.")
            break

def main():
    if "--web" in sys.argv:
        run_web()
    elif "--cli=linux" in sys.argv or "--cli-linux" in sys.argv:
        run_cli("linux")
    elif "--cli=windows" in sys.argv or "--cli-windows" in sys.argv:
        run_cli("windows")
    else:
        run_gui()

if __name__ == "__main__":
    main()
