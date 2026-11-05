"""
APP_SERVER.PY - Servidor Web Multihilo y API en Python Puro
Sirve los simuladores y procesa todas las llamadas de hardware y código en Python.
"""

import sys
import os
import json
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
from server.api_handler import SimulatorAPIHandler

class SimulatorHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Base directory de archivos estáticos (raíz del proyecto)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        super().__init__(*args, directory=base_dir, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._handle_api("GET")
        else:
            # Servir archivos estáticos normales (index.html, JS, CSS, Three.js)
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self._handle_api("POST")
        else:
            self.send_error(404, "Endpoint no soportado")

    def _handle_api(self, method: str):
        content_len = int(self.headers.get('Content-Length', 0))
        body = {}
        if content_len > 0:
            raw_body = self.rfile.read(content_len).decode('utf-8', errors='replace')
            try:
                body = json.loads(raw_body)
            except json.JSONDecodeError:
                body = {}

        status_code, response_data = self.server.api_handler.dispatch(self.path, method, body)

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()

        response_bytes = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response_bytes)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        # Log limpio en consola
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()


class ThreadedSimulatorServer(ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, host: str, port: int):
        self.api_handler = SimulatorAPIHandler()
        super().__init__((host, port), SimulatorHTTPHandler)


def get_local_ip() -> str:
    """Detecta la IP de la máquina en la red local (para Android)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def run_server(host: str = "0.0.0.0", port: int = 8080):
    server = ThreadedSimulatorServer(host, port)
    local_ip = get_local_ip()
    print("=" * 70)
    print("  DEV & HARDWARE SIMULATOR SUITE - SERVIDOR EN PYTHON")
    print("  Todos los motores y simuladores ejecutándose en Python 3")
    print("=" * 70)
    print(f"  ➜ En tu PC (Windows / Linux):    http://localhost:{port}")
    print(f"  ➜ En tu celular (Android Wi-Fi): http://{local_ip}:{port}")
    print("=" * 70)
    print("  Presiona Ctrl+C en cualquier momento para detener el servidor.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
        server.server_close()
