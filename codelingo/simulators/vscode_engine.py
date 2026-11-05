"""
VSCODE_ENGINE.PY - Motor en Python para el Simulador de VS Code
Soporte para ejecución y compilación de Python, C, C++, Java y JavaScript.
"""

import sys
import os
import subprocess
import tempfile
import time
import shutil

class VSCodeSimulatorEngine:
    def __init__(self):
        self.supported_languages = ['python', 'c', 'cpp', 'java', 'javascript']

    def execute_code(self, code: str, language: str) -> dict:
        """
        Ejecuta el código en el lenguaje especificado y devuelve:
        {
            'success': bool,
            'output': str,
            'error': str,
            'execution_time': float,
            'simulated': bool
        }
        """
        language = language.lower()
        if language not in self.supported_languages:
            return {
                'success': False,
                'output': '',
                'error': f"Lenguaje '{language}' no soportado.",
                'execution_time': 0,
                'simulated': False
            }

        start_time = time.time()
        try:
            if language == 'python':
                result = self._run_python(code)
            elif language in ['c', 'cpp']:
                result = self._run_c_cpp(code, is_cpp=(language == 'cpp'))
            elif language == 'java':
                result = self._run_java(code)
            elif language == 'javascript':
                result = self._run_javascript(code)
            else:
                result = {'success': False, 'output': '', 'error': 'Lenguaje desconocido', 'simulated': False}

            elapsed = round(time.time() - start_time, 3)
            result['execution_time'] = elapsed
            return result

        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f"Error interno del motor de ejecución: {str(e)}",
                'execution_time': round(time.time() - start_time, 3),
                'simulated': False
            }

    def _run_python(self, code: str) -> dict:
        with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name

        try:
            proc = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=8,
                encoding='utf-8',
                errors='replace'
            )
            return {
                'success': proc.returncode == 0,
                'output': proc.stdout,
                'error': proc.stderr,
                'simulated': False
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Tiempo de ejecución excedido (Timeout 8s). ¿Hay un bucle infinito?',
                'simulated': False
            }
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _run_c_cpp(self, code: str, is_cpp: bool = False) -> dict:
        compiler = 'g++' if is_cpp else 'gcc'
        ext = '.cpp' if is_cpp else '.c'
        has_compiler = shutil.which(compiler) is not None

        if not has_compiler:
            # Emulación inteligente de ejecución si GCC/G++ no está instalado en el SO
            return self._simulate_c_cpp_output(code, is_cpp)

        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, f'main{ext}')
            bin_path = os.path.join(tmpdir, 'main.exe' if os.name == 'nt' else 'main')

            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(code)

            # Compilación
            compile_proc = subprocess.run(
                [compiler, src_path, '-o', bin_path],
                capture_output=True,
                text=True,
                timeout=8,
                encoding='utf-8',
                errors='replace'
            )

            if compile_proc.returncode != 0:
                return {
                    'success': False,
                    'output': '',
                    'error': f"Error de compilación ({compiler}):\n{compile_proc.stderr}",
                    'simulated': False
                }

            # Ejecución
            try:
                run_proc = subprocess.run(
                    [bin_path],
                    capture_output=True,
                    text=True,
                    timeout=8,
                    encoding='utf-8',
                    errors='replace'
                )
                return {
                    'success': run_proc.returncode == 0,
                    'output': run_proc.stdout,
                    'error': run_proc.stderr,
                    'simulated': False
                }
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'output': '',
                    'error': 'Tiempo de ejecución excedido (Timeout 8s).',
                    'simulated': False
                }

    def _simulate_c_cpp_output(self, code: str, is_cpp: bool) -> dict:
        import re
        lines = []
        if is_cpp:
            matches = re.findall(r'std::cout\s*<<\s*["\'](.*?)["\']', code)
            lines.extend(matches)
        matches_printf = re.findall(r'printf\s*\(\s*["\'](.*?)["\']\s*\)', code)
        lines.extend(matches_printf)

        if not lines:
            lines = ["Programa compilado y ejecutado con éxito (código de salida 0)."]

        output = "\n".join([l.replace('\\n', '\n') for l in lines])
        return {
            'success': True,
            'output': f"[Motor de Simulación C/C++]:\n{output}",
            'error': '',
            'simulated': True
        }

    def _run_java(self, code: str) -> dict:
        has_javac = shutil.which('javac') is not None
        if not has_javac:
            # Emulación inteligente si Java SDK no está presente
            import re
            matches = re.findall(r'System\.out\.println\s*\(\s*["\'](.*?)["\']\s*\)', code)
            output = "\n".join(matches) if matches else "OpenJDK VM: Clase compilada y ejecutada con éxito."
            return {
                'success': True,
                'output': f"[Simulador OpenJDK]:\n{output}",
                'error': '',
                'simulated': True
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, 'Main.java')
            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(code)

            comp = subprocess.run(['javac', src_path], capture_output=True, text=True, timeout=8)
            if comp.returncode != 0:
                return {'success': False, 'output': '', 'error': comp.stderr, 'simulated': False}

            run_proc = subprocess.run(['java', '-cp', tmpdir, 'Main'], capture_output=True, text=True, timeout=8)
            return {'success': run_proc.returncode == 0, 'output': run_proc.stdout, 'error': run_proc.stderr, 'simulated': False}

    def _run_javascript(self, code: str) -> dict:
        has_node = shutil.which('node') is not None
        if not has_node:
            import re
            matches = re.findall(r'console\.log\s*\(\s*["\'](.*?)["\']\s*\)', code)
            output = "\n".join(matches) if matches else "Node.js v20.10.0: Script ejecutado exitosamente."
            return {
                'success': True,
                'output': f"[Simulador Node.js / V8]:\n{output}",
                'error': '',
                'simulated': True
            }

        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name

        try:
            proc = subprocess.run(['node', temp_path], capture_output=True, text=True, timeout=8)
            return {'success': proc.returncode == 0, 'output': proc.stdout, 'error': proc.stderr, 'simulated': False}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == '__main__':
    engine = VSCodeSimulatorEngine()
    print("Probando motor VS Code en Python...")
    res = engine.execute_code("print('Hola desde Python!')", "python")
    print("Resultado:", res)
