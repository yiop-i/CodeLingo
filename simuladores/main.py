#!/usr/bin/env python3
"""
MAIN.PY - PUNTO DE ENTRADA PRINCIPAL EN PYTHON
Suite completa de Simuladores de Software y Hardware en 3D
Ejecución:
    python main.py               (Inicia el servidor y abre la aplicación universal)
    python main.py --port=8080   (Especifica puerto personalizado)
    python main.py --cli=linux   (Abre directamente la terminal Linux interactiva en Python)
    python main.py --cli=windows (Abre directamente la terminal Windows interactiva en Python)
"""

import sys
import os
import argparse
import webbrowser
import threading
import time

# Asegurar que el directorio raíz esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from server.app_server import run_server, get_local_ip

def start_gui_browser(url: str):
    time.sleep(1.0)
    print(f"Abriendo aplicación en el navegador: {url} ...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"No se pudo abrir el navegador automáticamente: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Suite de Simuladores de Software y Montaje de Hardware 3D programada en Python"
    )
    parser.add_argument("--port", type=int, default=8080, help="Puerto del servidor (por defecto: 8080)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host de enlace (por defecto: 0.0.0.0 para acceso en red local)")
    parser.add_argument("--no-browser", action="store_true", help="No abrir automáticamente el navegador")
    parser.add_argument("--cli", type=str, choices=["linux", "windows", "placement", "maint"], help="Ejecutar simulador específico en modo terminal CLI")

    args = parser.parse_args()

    # Modo Terminal CLI directo en Python si el usuario lo solicita
    if args.cli == "linux":
        from simulators.linux_terminal import LinuxTerminalSimulator
        term = LinuxTerminalSimulator()
        print("=== TERMINAL LINUX BASH EN PYTHON CLI ===")
        print("Escribe 'exit' para salir.\n")
        while True:
            try:
                cmd = input(term.get_prompt())
                if cmd.strip().lower() == "exit": break
                res = term.execute_command(cmd)
                if res['output'] == "__CLEAR__":
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif res['output']:
                    print(res['output'])
            except (KeyboardInterrupt, EOFError):
                break
        return

    elif args.cli == "windows":
        from simulators.windows_terminal import WindowsTerminalSimulator
        term = WindowsTerminalSimulator()
        print("=== TERMINAL WINDOWS POWERSHELL / CMD EN PYTHON CLI ===")
        print("Escribe 'exit' para salir.\n")
        while True:
            try:
                cmd = input(term.get_prompt())
                if cmd.strip().lower() == "exit": break
                res = term.execute_command(cmd)
                if res['output'] == "__CLEAR__":
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif res['output']:
                    print(res['output'])
            except (KeyboardInterrupt, EOFError):
                break
        return

    # Modo Aplicación Gráfica Completa Multi-OS (Windows, Linux, Android)
    url = f"http://localhost:{args.port}"

    if not args.no_browser:
        t = threading.Thread(target=start_gui_browser, args=(url,), daemon=True)
        t.start()

    run_server(host=args.host, port=args.port)

if __name__ == '__main__':
    main()
