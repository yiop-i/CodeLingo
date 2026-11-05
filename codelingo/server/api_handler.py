"""
API_HANDLER.PY - Enrutador de API REST en Python para todos los Simuladores
Procesa peticiones JSON y conecta la interfaz con los motores de Python.
"""

import json
from simulators import (
    VSCodeSimulatorEngine,
    LinuxTerminalSimulator,
    WindowsTerminalSimulator,
    WebStudioSimulator,
    HardwareRecognitionSimulator,
    HardwarePlacementSimulator,
    HardwareUpgradeSimulator,
    HardwareMaintenanceSimulator
)

class SimulatorAPIHandler:
    def __init__(self):
        self.vscode = VSCodeSimulatorEngine()
        self.linux_term = LinuxTerminalSimulator()
        self.win_term = WindowsTerminalSimulator()
        self.web_studio = WebStudioSimulator()
        self.hw_recog = HardwareRecognitionSimulator()
        self.hw_place = HardwarePlacementSimulator()
        self.hw_upgrade = HardwareUpgradeSimulator()
        self.hw_maint = HardwareMaintenanceSimulator()

    def dispatch(self, path: str, method: str, body: dict = None) -> tuple[int, dict]:
        body = body or {}

        # 1. VS Code Multi-lenguaje (Python, C, C++, Java, JS)
        if path in ["/api/vscode/execute", "/api/code/run"] and method == "POST":
            code = body.get("code", "")
            lang = body.get("language") or body.get("lang", "python")
            res = self.vscode.execute_code(code, lang)
            # Compatibilidad dual de nombres de campos
            res['stdout'] = res.get('output', '')
            res['stderr'] = res.get('error', '')
            res['execution_time_ms'] = int(res.get('execution_time', 0) * 1000)
            return 200, res

        # 2. Terminal Linux Bash
        elif path in ["/api/terminal/linux", "/api/linux/exec"] and method == "POST":
            cmd = body.get("command") or body.get("cmd", "")
            res = self.linux_term.execute_command(cmd)
            return 200, res

        # 3. Terminal Windows CMD / PS
        elif path in ["/api/terminal/windows", "/api/windows/exec"] and method == "POST":
            cmd = body.get("command") or body.get("cmd", "")
            res = self.win_term.execute_command(cmd)
            return 200, res

        # 4. Web Studio (HTML/CSS/JS)
        elif path == "/api/web/preview" and method == "POST":
            h = body.get("html", "")
            c = body.get("css", "")
            j = body.get("js", "")
            res = self.web_studio.build_preview_document(h, c, j)
            return 200, res

        # 5. Simulador 1: Reconocimiento de Componentes 3D
        elif path == "/api/hardware/recognition" and method == "GET":
            catalog = self.hw_recog.get_catalog()
            return 200, {'catalog': catalog}

        elif path == "/api/hardware/recognition/quiz" and method == "POST":
            comp_id = body.get("comp_id", "")
            ans_idx = int(body.get("answer_index", 0))
            res = self.hw_recog.validate_quiz_answer(comp_id, ans_idx)
            return 200, res

        # 6. Simulador 2: Montaje y Validación Estricta de Ranuras
        elif path == "/api/hardware/placement/set_machine" and method == "POST":
            m_type = body.get("machine", "desktop")
            self.hw_place.set_active_machine(m_type)
            return 200, {'success': True, 'machine': m_type}

        elif path == "/api/hardware/placement/validate" and method == "POST":
            part_id = body.get("part_id", "")
            slot_id = body.get("slot_id", "")
            res = self.hw_place.validate_and_place(part_id, slot_id)
            return 200, res

        elif path == "/api/hardware/placement/reset" and method == "POST":
            self.hw_place.reset_machine()
            return 200, {'success': True}

        # 7. Simulador 3: Upgrades y Benchmarks en Vivo
        elif path == "/api/hardware/upgrade/set_case" and method == "POST":
            case_id = body.get("case_id", "desktop")
            self.hw_upgrade.set_case(case_id)
            return 200, {'success': True, 'case_id': case_id, 'benchmarks': self.hw_upgrade.calculate_benchmarks()}

        elif path == "/api/hardware/upgrade/unmount" and method == "POST":
            slot_key = body.get("slot_key", "")
            res = self.hw_upgrade.unmount_component(slot_key)
            return 200, res

        elif path == "/api/hardware/upgrade/install" and method == "POST":
            slot_key = body.get("slot_key", "")
            res = self.hw_upgrade.install_upgrade(slot_key)
            return 200, res

        # 8. Simulador 4: Limpieza, Térmica y Mantenimiento Técnico
        elif path == "/api/hardware/maintenance/tool" and method == "POST":
            tool = body.get("tool", "blower")
            res = self.hw_maint.apply_tool(tool)
            return 200, res

        elif path == "/api/hardware/maintenance/reset" and method == "POST":
            res = self.hw_maint.reset()
            return 200, {'success': True, 'telemetry': res}

        # Ruta no encontrada
        return 404, {'error': f"Endpoint no encontrado: {path}"}
