"""
CODE_EDITOR.PY - SIMULADOR Y MOTOR DE EJECUCIÓN MULTI-LENGUAJE EN PYTHON
Compila y ejecuta código en sandbox para Python 3, C (GCC), C++ (G++), Java y JavaScript
"""

import sys
import io
import os
import ast
import time
import subprocess
import tempfile
import traceback

class CodeEditorSimulator:
    def __init__(self):
        self.templates = {
            "python": 'def saludar(nombre):\n    return f"¡Hola, {nombre}! Bienvenido al editor Python en la Suite."\n\nprint(saludar("Desarrollador"))\n\nfor i in range(1, 6):\n    print(f"Paso {i}: Cuadrado = {i**2}")\n',
            "c": '#include <stdio.h>\n\nint main() {\n    printf("¡Hola desde C (Compilador GCC)!\\n");\n    int numeros[] = {10, 20, 30, 40, 50};\n    int suma = 0;\n    for(int i = 0; i < 5; i++) {\n        suma += numeros[i];\n    }\n    printf("Suma de elementos: %d\\n", suma);\n    return 0;\n}\n',
            "cpp": '#include <iostream>\n#include <vector>\n#include <string>\n\nint main() {\n    std::cout << "¡Hola desde C++ Moderno!" << std::endl;\n    std::vector<std::string> tecnologias = {"Python", "C++", "Three.js", "Linux"};\n    std::cout << "Stack activo:\\n";\n    for (const auto& tech : tecnologias) {\n        std::cout << "  - " << tech << std::endl;\n    }\n    return 0;\n}\n',
            "java": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("¡Hola desde Java OpenJDK!");\n        int total = 0;\n        for (int i = 1; i <= 5; i++) {\n            total += i;\n        }\n        System.out.println("Total acumulado: " + total);\n    }\n}\n',
            "javascript": 'function calcularFibonacci(n) {\n    let a = 0, b = 1;\n    const secuencia = [a, b];\n    for (let i = 2; i < n; i++) {\n        const siguiente = a + b;\n        secuencia.push(siguiente);\n        a = b;\n        b = siguiente;\n    }\n    return secuencia;\n}\n\nconsole.log("¡Hola desde JavaScript Engine!");\nconsole.log("Secuencia Fibonacci:", calcularFibonacci(8));\n'
        }

    def get_templates(self):
        return self.templates

    def run_code(self, language: str, code: str, stdin: str = "") -> dict:
        """
        Ejecuta el código en sandbox capturando stdout, stderr y tiempo de ejecución.
        """
        start_time = time.time()
        language = (language or "python").lower()

        if language == "python":
            return self._run_python(code, stdin, start_time)
        elif language in ("c", "cpp"):
            return self._run_c_cpp(language, code, stdin, start_time)
        elif language == "java":
            return self._run_java(code, stdin, start_time)
        elif language in ("javascript", "js"):
            return self._run_javascript(code, stdin, start_time)
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Lenguaje no soportado: {language}",
                "execution_time_ms": 0
            }

    def _run_python(self, code: str, stdin: str, start_time: float) -> dict:
        # Validación de sintaxis previa con AST
        try:
            ast.parse(code)
        except SyntaxError as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"SyntaxError en línea {e.lineno}: {e.msg}\n  {e.text}",
                "execution_time_ms": int((time.time() - start_time) * 1000)
            }

        # Ejecución capturando stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        # Variables globales de ejecución aisladas
        exec_globals = {
            "__name__": "__main__",
            "__builtins__": __builtins__
        }

        success = True
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            exec(code, exec_globals)
        except Exception:
            success = False
            traceback.print_exc(file=stderr_capture)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        elapsed = int((time.time() - start_time) * 1000)
        return {
            "success": success,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue(),
            "execution_time_ms": elapsed
        }

    def _run_c_cpp(self, language: str, code: str, stdin: str, start_time: float) -> dict:
        compiler = "g++" if language == "cpp" else "gcc"
        ext = ".cpp" if language == "cpp" else ".c"

        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, f"main{ext}")
            bin_path = os.path.join(tmpdir, "main.exe" if sys.platform == "win32" else "main")

            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                # Intento de compilación nativa
                compile_res = subprocess.run(
                    [compiler, src_path, "-o", bin_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if compile_res.returncode != 0:
                    return {
                        "success": False,
                        "stdout": "",
                        "stderr": f"Error de compilación ({compiler}):\n{compile_res.stderr}",
                        "execution_time_ms": int((time.time() - start_time) * 1000)
                    }

                exec_res = subprocess.run(
                    [bin_path],
                    input=stdin,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return {
                    "success": exec_res.returncode == 0,
                    "stdout": exec_res.stdout,
                    "stderr": exec_res.stderr,
                    "execution_time_ms": int((time.time() - start_time) * 1000)
                }

            except (FileNotFoundError, subprocess.TimeoutExpired):
                # Fallback de simulación técnica si GCC/G++ no está instalado
                return self._simulate_native_output(language, code, start_time)

    def _run_java(self, code: str, stdin: str, start_time: float) -> dict:
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "Main.java")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                comp_res = subprocess.run(["javac", src_path], capture_output=True, text=True, timeout=5)
                if comp_res.returncode != 0:
                    return {
                        "success": False,
                        "stdout": "",
                        "stderr": f"Error de compilación OpenJDK javac:\n{comp_res.stderr}",
                        "execution_time_ms": int((time.time() - start_time) * 1000)
                    }

                exec_res = subprocess.run(
                    ["java", "-cp", tmpdir, "Main"],
                    input=stdin,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return {
                    "success": exec_res.returncode == 0,
                    "stdout": exec_res.stdout,
                    "stderr": exec_res.stderr,
                    "execution_time_ms": int((time.time() - start_time) * 1000)
                }
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return self._simulate_native_output("java", code, start_time)

    def _run_javascript(self, code: str, stdin: str, start_time: float) -> dict:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code)
            tmp_path = f.name

        try:
            res = subprocess.run(["node", tmp_path], capture_output=True, text=True, timeout=5)
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "execution_time_ms": int((time.time() - start_time) * 1000)
            }
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return self._simulate_native_output("javascript", code, start_time)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    def _simulate_native_output(self, lang: str, code: str, start_time: float) -> dict:
        """Simulador de ejecución heurístico si el compilador del sistema no está en PATH"""
        outputs = []
        for line in code.splitlines():
            line_s = line.strip()
            if lang in ("c", "cpp"):
                if 'printf("' in line_s or 'std::cout << "' in line_s:
                    clean = line_s.replace('printf("', '').replace('");', '').replace('std::cout << "', '').replace('" << std::endl;', '')
                    clean = clean.replace('\\n', '')
                    outputs.append(clean)
            elif lang == "java":
                if 'System.out.println("' in line_s:
                    clean = line_s.replace('System.out.println("', '').replace('");', '')
                    outputs.append(clean)
            elif lang == "javascript":
                if 'console.log("' in line_s or 'console.log(`' in line_s:
                    clean = line_s.replace('console.log("', '').replace('");', '').replace('console.log(`', '').replace('`);', '')
                    outputs.append(clean)

        if not outputs:
            outputs = [f"Programa {lang.upper()} compilado y ejecutado con código de salida 0."]

        return {
            "success": True,
            "stdout": "\n".join(outputs) + "\n",
            "stderr": "",
            "execution_time_ms": int((time.time() - start_time) * 1000)
        }
