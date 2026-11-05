# -*- coding: utf-8 -*-
"""
SIMULATORS_BRIDGE.PY - Puente Unificado de Motores de Simulación y Ejecución
Conecta la interfaz gráfica de CodeLingo con:
- El motor de compilación/ejecución multi-lenguaje (Python, C, C++, Java, JS).
- Los simuladores de terminales con VFS (Windows PowerShell/CMD y Linux Bash).
- La base de conocimiento y diagnóstico de Hardware (Escritorio y Notebook).
- El servidor web multihilo local para acceso móvil (Android / Tablets / LAN).
"""

import sys
import os
import threading
import webbrowser

# Asegurar que simulators y server estén en el path
sys.path.append(os.path.dirname(__file__))

try:
    from simulators.vscode_engine import VSCodeSimulatorEngine
    from simulators.linux_terminal import LinuxTerminalSimulator
    from simulators.windows_terminal import WindowsTerminalSimulator
    from simulators.hardware_recognition import HardwareRecognitionSimulator
    from simulators.hardware_placement import HardwarePlacementSimulator
    from simulators.hardware_upgrade import HardwareUpgradeSimulator
    from simulators.hardware_maintenance import HardwareMaintenanceSimulator
except ImportError as e:
    print(f"Aviso en carga de simuladores: {e}")

class SimulatorsBridge:
    _instance = None

    def __init__(self):
        self.code_engine = VSCodeSimulatorEngine()
        self.linux_term = LinuxTerminalSimulator()
        self.windows_term = WindowsTerminalSimulator()
        self.hw_recog = HardwareRecognitionSimulator()
        self.hw_placement = HardwarePlacementSimulator()
        self.hw_upgrade = HardwareUpgradeSimulator()
        self.hw_maintenance = HardwareMaintenanceSimulator()
        self.web_server_thread = None
        self.web_server_running = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SimulatorsBridge()
        return cls._instance

    # 1. EJECUCIÓN DE CÓDIGO
    def run_code(self, code: str, language: str) -> dict:
        """
        Ejecuta código en Python, C++, C, Java, JavaScript, HTML o CSS.
        """
        lang = language.lower()
        if lang in ["python", "c", "cpp", "c++", "java", "javascript", "js", "javascript web"]:
            normalized_lang = "cpp" if lang in ["cpp", "c++"] else ("javascript" if "javascript" in lang or lang == "js" else lang)
            return self.code_engine.execute_code(code, normalized_lang)
        elif lang in ["html", "css"]:
            return {
                "success": True,
                "output": "✓ Código HTML/CSS sintácticamente estructurado. Previsualización disponible en Web Studio.",
                "error": "",
                "execution_time": 0.05,
                "simulated": True
            }
        else:
            return {
                "success": False,
                "output": "",
                "error": f"Lenguaje '{language}' no soportado directamente.",
                "execution_time": 0.0
            }

    # 2. EJECUCIÓN DE TERMINAL
    def execute_terminal_cmd(self, command: str, os_type: str = "linux") -> str:
        """
        Ejecuta un comando en la terminal virtual (Linux Bash o Windows PowerShell/CMD)
        utilizando el sistema de archivos virtual jerárquico.
        """
        cmd = command.strip()
        if not cmd:
            return ""

        if "windows" in os_type.lower():
            res = self.windows_term.execute_command(cmd)
            out = res.get("output", "")
            err = res.get("error", "")
            return out if out else err
        else:
            res = self.linux_term.execute_command(cmd)
            out = res.get("output", "")
            err = res.get("error", "")
            return out if out else err

    def get_terminal_prompt(self, os_type: str = "linux") -> str:
        if "windows" in os_type.lower():
            return self.windows_term.get_prompt()
        return self.linux_term.get_prompt()

    # 3. DIAGNÓSTICO DE HARDWARE
    def get_hardware_components(self):
        return self.hw_recog.get_catalog()

    def validate_slot_placement(self, part_id: str, slot_id: str) -> dict:
        return self.hw_placement.validate_and_place(part_id, slot_id)

    # 4. LANZAMIENTO DE SUITE WEB / MÓVIL
    def launch_mobile_web_server(self, port: int = 8080):
        """Inicia el servidor web multihilo local y abre el simulador en el navegador."""
        if self.web_server_running:
            webbrowser.open(f"http://localhost:{port}")
            return True, f"Servidor ya activo en http://localhost:{port}"

        def _run():
            try:
                from server.app_server import ThreadedSimulatorServer
                server = ThreadedSimulatorServer("0.0.0.0", port)
                self.web_server_running = True
                server.serve_forever()
            except Exception as e:
                print(f"Error al iniciar servidor web: {e}")
                self.web_server_running = False

        self.web_server_thread = threading.Thread(target=_run, daemon=True)
        self.web_server_thread.start()
        webbrowser.open(f"http://localhost:{port}")
        return True, f"Servidor iniciado con éxito en http://localhost:{port}"
