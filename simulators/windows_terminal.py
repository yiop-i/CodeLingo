"""
WINDOWS_TERMINAL.PY - Motor en Python para el Simulador de Terminal Windows CMD y PowerShell
Emulador del Símbolo del Sistema de Windows (CMD.EXE) y PowerShell 7 en Python.
"""

import sys
import os
import time

class WindowsTerminalSimulator:
    def __init__(self, mode: str = "powershell"):
        self.mode = mode.lower() # 'cmd' o 'powershell'
        self.cwd = ["C:", "Users", "Administrator"]
        self.history = []
        self.virtual_files = {
            "C:\\Users\\Administrator\\Desktop": {"type": "dir"},
            "C:\\Users\\Administrator\\Documents": {"type": "dir"},
            "C:\\Users\\Administrator\\Downloads": {"type": "dir"},
            "C:\\Users\\Administrator\\notas.txt": {"type": "file", "content": "Bienvenido a Windows PowerShell en Python.\nSimulador listo para comandos de red y procesos."},
            "C:\\Users\\Administrator\\config.json": {"type": "file", "content": "{\n  \"os\": \"Windows 11 Pro\",\n  \"build\": 22631,\n  \"ps_version\": \"7.4.1\"\n}"}
        }

    def get_prompt(self) -> str:
        path_str = "\\".join(self.cwd)
        if self.mode == "powershell":
            return f"PS {path_str}> "
        else:
            return f"{path_str}>"

    def execute_command(self, cmd_line: str) -> dict:
        cmd_line = cmd_line.strip()
        if not cmd_line:
            return {'output': '', 'cwd': "\\".join(self.cwd), 'prompt': self.get_prompt()}

        self.history.append(cmd_line)
        parts = cmd_line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        output = ""

        if cmd in ["cls", "clear", "clear-host"]:
            output = "__CLEAR__"
        elif cmd in ["ver"]:
            output = "\nMicrosoft Windows [Versión 10.0.22631.3296]\n(c) Microsoft Corporation. Todos los derechos reservados."
        elif cmd in ["echo"]:
            output = " ".join(args)
        elif cmd in ["dir", "ls", "get-childitem"]:
            curr_path = "\\".join(self.cwd)
            lines = [
                f"\n El volumen de la unidad C es Windows",
                f" El número de serie del volumen es 4B82-9F1C\n",
                f" Directorio de {curr_path}\n"
            ]
            items = []
            for k, v in self.virtual_files.items():
                if os.path.dirname(k).lower() == curr_path.lower():
                    name = os.path.basename(k)
                    if v["type"] == "dir":
                        items.append(f"01/15/2026  10:30 AM    <DIR>          {name}")
                    else:
                        sz = len(v.get("content", ""))
                        items.append(f"01/15/2026  10:30 AM               {sz:3d} {name}")
            if not items:
                items.append("01/15/2026  10:30 AM    <DIR>          .")
                items.append("01/15/2026  10:30 AM    <DIR>          ..")
            lines.extend(items)
            output = "\n".join(lines)
        elif cmd in ["cd"]:
            if not args:
                output = "\\".join(self.cwd)
            else:
                target = args[0]
                if target == "..":
                    if len(self.cwd) > 1:
                        self.cwd.pop()
                elif target == "\\" or target == "/":
                    self.cwd = [self.cwd[0]]
                else:
                    new_path = "\\".join(self.cwd) + "\\" + target
                    if new_path in self.virtual_files and self.virtual_files[new_path]["type"] == "dir":
                        self.cwd.append(target)
                    else:
                        output = f"El sistema no puede encontrar la ruta especificada: {target}"
        elif cmd in ["type", "cat", "get-content"]:
            if not args:
                output = "La sintaxis del comando no es correcta."
            else:
                path = "\\".join(self.cwd) + "\\" + args[0]
                if path in self.virtual_files and self.virtual_files[path]["type"] == "file":
                    output = self.virtual_files[path]["content"]
                else:
                    output = f"No se encuentra el archivo {args[0]}."
        elif cmd in ["ipconfig"]:
            output = """
Configuración IP de Windows

Adaptador de Ethernet Ethernet 1:
   Sufijo DNS específico para la conexión. . : localdomain
   Vínculo: dirección IPv6 local. . . : fe80::49b2:98fa:312a:9912%12
   Dirección IPv4. . . . . . . . . . . . . . : 192.168.1.105
   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
   Puerta de enlace predeterminada . . . . . : 192.168.1.1

Adaptador de LAN inalámbrica Wi-Fi:
   Estado de los medios. . . . . . . . . . . : Medios desconectados
"""
        elif cmd in ["systeminfo"]:
            output = """
Nombre de host:              ANTIGRAVITY-PC
Nombre del sistema operativo: Microsoft Windows 11 Pro
Versión del SO:              10.0.22631 N/D Compilación 22631
Fabricante del SO:           Microsoft Corporation
Configuración del SO:        Estación de trabajo independiente
Tipo de compilación del SO:  Multiprocessor Free
Fabricante del sistema:      Custom Build Gaming Rig
Modelo del sistema:          Z790 Taichi Razer Edition
Tipo de sistema:             x64-based PC
Procesador(es):              1 procesadores instalados.
                             [01]: Intel64 Family 6 Model 183 Stepping 1 GenuineIntel ~3200 Mhz
Versión del BIOS:            American Megatrends Inc. 3.02, 10/12/2025
Memoria física total:        32,684 MB
Memoria física disponible:   24,192 MB
Tarjeta(s) de red:           1 NIC instaladas.
"""
        elif cmd in ["tasklist", "get-process", "ps"]:
            output = """
Nombre de imagen               PID Nombre de sesión Núm. de ses  Uso de memoria
========================= ======== ================ ============ ===============
System Idle Process              0 Services                    0            8 K
System                           4 Services                    0          128 K
smss.exe                       412 Services                    0        1,024 K
csrss.exe                      580 Services                    0        4,120 K
winlogon.exe                   692 Console                     1        8,450 K
explorer.exe                  2340 Console                     1      145,200 K
Code.exe                      4512 Console                     1      210,400 K
python.exe                    5820 Console                     1       45,600 K
powershell.exe                6190 Console                     1       65,120 K
"""
        elif cmd in ["powershell"]:
            self.mode = "powershell"
            output = "Windows PowerShell\nCopyright (C) Microsoft Corporation. Todos los derechos reservados."
        elif cmd in ["cmd"]:
            self.mode = "cmd"
            output = "Microsoft Windows [Versión 10.0.22631.3296]\n(c) Microsoft Corporation. Todos los derechos reservados."
        elif cmd in ["help"]:
            output = "Comandos Windows implementados en Python:\n  dir, cd, cls, echo, type, ver, ipconfig, systeminfo, tasklist, powershell, cmd, Get-Process, Get-Content, Clear-Host"
        else:
            if self.mode == "powershell":
                output = f"{cmd}: El término '{cmd}' no se reconoce como nombre de un cmdlet, función, archivo de script o programa ejecutable."
            else:
                output = f"'{cmd}' no se reconoce como un comando interno o externo, programa o archivo por lotes ejecutable."

        return {
            'output': output,
            'cwd': "\\".join(self.cwd),
            'prompt': self.get_prompt()
        }


if __name__ == '__main__':
    term = WindowsTerminalSimulator()
    print("Iniciando Windows Terminal Simulator en Python CLI. Escribe 'exit' para salir.\n")
    while True:
        try:
            line = input(term.get_prompt())
            if line.strip().lower() == "exit": break
            res = term.execute_command(line)
            if res['output'] == "__CLEAR__":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif res['output']:
                print(res['output'])
        except (KeyboardInterrupt, EOFError):
            break
