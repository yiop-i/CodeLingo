"""
LINUX_TERMINAL.PY - Motor en Python para el Simulador de Terminal Linux Bash
Emulador de sistema de archivos virtual jerárquico y comandos bash en Python.
"""

import sys
import os
import time
import re

class VirtualNode:
    def __init__(self, name: str, is_dir: bool = False, content: str = "", owner: str = "root", permissions: str = "rwxr-xr-x"):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.owner = owner
        self.permissions = permissions
        self.children = {} if is_dir else None
        self.mtime = time.time()

class LinuxTerminalSimulator:
    def __init__(self, username: str = "devuser", hostname: str = "antigravity-box"):
        self.username = username
        self.hostname = hostname
        self.history = []
        self._init_vfs()

    def _init_vfs(self):
        self.root = VirtualNode("", is_dir=True)
        # Carpetas base de Linux
        for d in ["bin", "etc", "home", "var", "tmp", "usr", "opt"]:
            self.root.children[d] = VirtualNode(d, is_dir=True)

        user_home = VirtualNode(self.username, is_dir=True, owner=self.username)
        self.root.children["home"].children[self.username] = user_home

        # Archivos de bienvenida en /home/devuser
        user_home.children["bienvenido.txt"] = VirtualNode(
            "bienvenido.txt",
            is_dir=False,
            content="¡Bienvenido al Simulador de Terminal Linux Bash escrito 100% en Python!\nUsa 'help' para ver los comandos disponibles.",
            owner=self.username
        )
        user_home.children["script.py"] = VirtualNode(
            "script.py",
            is_dir=False,
            content="print('Hola desde el VFS de Linux en Python!')\nfor i in range(3):\n    print(f'Paso {i+1}')",
            owner=self.username
        )
        user_home.children["proyectos"] = VirtualNode("proyectos", is_dir=True, owner=self.username)

        self.cwd_path = ["home", self.username]

    def get_prompt(self) -> str:
        tilde_path = self._get_display_path()
        return f"{self.username}@{self.hostname}:{tilde_path}$ "

    def _get_display_path(self) -> str:
        if self.cwd_path == ["home", self.username]:
            return "~"
        elif len(self.cwd_path) > 2 and self.cwd_path[:2] == ["home", self.username]:
            return "~/" + "/".join(self.cwd_path[2:])
        return "/" + "/".join(self.cwd_path)

    def _resolve_node(self, path: str):
        if not path or path == ".":
            curr = self.root
            for seg in self.cwd_path:
                curr = curr.children.get(seg)
                if not curr: return None
            return curr

        parts = [p for p in path.split("/") if p]
        curr = self.root if path.startswith("/") else self._resolve_node(".")
        if not curr: return None

        base_parts = [] if path.startswith("/") else list(self.cwd_path)

        for p in parts:
            if p == ".":
                continue
            elif p == "..":
                if base_parts:
                    base_parts.pop()
                    curr = self.root
                    for b in base_parts:
                        curr = curr.children.get(b)
            else:
                if not curr.is_dir or p not in curr.children:
                    return None
                curr = curr.children[p]
                base_parts.append(p)
        return curr

    def execute_command(self, cmd_line: str) -> dict:
        cmd_line = cmd_line.strip()
        if not cmd_line:
            return {'output': '', 'cwd': self._get_display_path(), 'prompt': self.get_prompt()}

        self.history.append(cmd_line)

        # Manejo de redirección > y >>
        redirect_mode = None
        target_file = None
        if ">>" in cmd_line:
            cmd_line, target_file = cmd_line.split(">>", 1)
            redirect_mode = "append"
            target_file = target_file.strip()
        elif ">" in cmd_line:
            cmd_line, target_file = cmd_line.split(">", 1)
            redirect_mode = "overwrite"
            target_file = target_file.strip()

        parts = cmd_line.strip().split()
        cmd = parts[0]
        args = parts[1:]

        output = ""

        if cmd == "pwd":
            output = "/" + "/".join(self.cwd_path)
        elif cmd == "whoami":
            output = self.username
        elif cmd == "uname":
            output = "Linux antigravity-core 6.8.0-45-generic x86_64 GNU/Linux" if "-a" in args else "Linux"
        elif cmd == "date":
            output = time.strftime("%a %b %d %H:%M:%S %Z %Y")
        elif cmd == "clear":
            output = "__CLEAR__"
        elif cmd == "history":
            output = "\n".join(f"{i+1}  {h}" for i, h in enumerate(self.history))
        elif cmd == "echo":
            output = " ".join(args).replace('"', '').replace("'", "")
        elif cmd == "cd":
            target = args[0] if args else f"/home/{self.username}"
            if target == "~":
                self.cwd_path = ["home", self.username]
            else:
                node = self._resolve_node(target)
                if node and node.is_dir:
                    if target.startswith("/"):
                        self.cwd_path = [p for p in target.split("/") if p]
                    else:
                        for p in [x for x in target.split("/") if x]:
                            if p == "..":
                                if self.cwd_path: self.cwd_path.pop()
                            elif p != ".":
                                self.cwd_path.append(p)
                else:
                    output = f"bash: cd: {target}: No such file or directory"
        elif cmd == "ls":
            curr = self._resolve_node(".")
            if curr and curr.is_dir:
                items = sorted(curr.children.keys())
                if "-l" in args or "-la" in args or "-lh" in args:
                    lines = [f"total {len(items) * 4}"]
                    for it in items:
                        node = curr.children[it]
                        p = ("d" if node.is_dir else "-") + node.permissions
                        sz = len(node.content) if not node.is_dir else 4096
                        lines.append(f"{p} 1 {node.owner} {node.owner} {sz:5d} Jan 01 12:00 {it}")
                    output = "\n".join(lines)
                else:
                    output = "  ".join(items)
            else:
                output = "ls: cannot access directory"
        elif cmd == "mkdir":
            if not args:
                output = "mkdir: missing operand"
            else:
                curr = self._resolve_node(".")
                dir_name = args[0].replace("-p", "").strip()
                if dir_name in curr.children:
                    output = f"mkdir: cannot create directory '{dir_name}': File exists"
                else:
                    curr.children[dir_name] = VirtualNode(dir_name, is_dir=True, owner=self.username)
        elif cmd == "touch":
            if not args:
                output = "touch: missing file operand"
            else:
                curr = self._resolve_node(".")
                fn = args[0]
                if fn not in curr.children:
                    curr.children[fn] = VirtualNode(fn, is_dir=False, content="", owner=self.username)
        elif cmd == "cat":
            if not args:
                output = "cat: missing file operand"
            else:
                node = self._resolve_node(args[0])
                if node and not node.is_dir:
                    output = node.content
                elif node and node.is_dir:
                    output = f"cat: {args[0]}: Is a directory"
                else:
                    output = f"cat: {args[0]}: No such file or directory"
        elif cmd == "rm":
            if not args:
                output = "rm: missing operand"
            else:
                target = args[-1]
                curr = self._resolve_node(".")
                if target in curr.children:
                    del curr.children[target]
                else:
                    output = f"rm: cannot remove '{target}': No such file or directory"
        elif cmd == "grep":
            if len(args) >= 2:
                pattern = args[0]
                node = self._resolve_node(args[1])
                if node and not node.is_dir:
                    matches = [l for l in node.content.splitlines() if pattern in l]
                    output = "\n".join(matches)
                else:
                    output = f"grep: {args[1]}: No such file or directory"
            else:
                output = "Usage: grep <pattern> <file>"
        elif cmd == "neofetch":
            output = f"""
       _,met$$$$$gg.          {self.username}@{self.hostname}
    ,g$$$$$$$$$$$$$$$P.       -------------------
  ,g$$P"     \"\"\"Y$$.".        OS: Debian GNU/Linux 12 (bookworm) x86_64
 ,$$P'              `$$$.     Host: Google Antigravity Virtual Simulator
',$$P       ,ggs.     `$$b:   Kernel: 6.8.0-45-generic
`d$$'     ,$P"'   .    $$$    Uptime: 4 days, 12 hours
 $$P      d$'     ,    $$P    Shell: bash 5.2.15
 $$:      $$.   -    ,d$$'    Terminal: python-virtual-pty
 $$;      Y$b._   _,d$P'      CPU: AMD Ryzen 9 7950X / Intel Core i9
 Y$$.    `.`"Y$$$$P"'         Memory: 2048MiB / 32768MiB
  `$$b      "-.__
   `Y$$
"""
        elif cmd in ["python", "python3"]:
            if args:
                node = self._resolve_node(args[0])
                if node and not node.is_dir:
                    # Ejecutar script con motor Python
                    try:
                        import io
                        import contextlib
                        f_stdout = io.StringIO()
                        with contextlib.redirect_stdout(f_stdout):
                            exec(node.content, {})
                        output = f_stdout.getvalue().strip()
                    except Exception as ex:
                        output = f"Python Traceback (most recent call last):\n{ex}"
                else:
                    output = f"python3: can't open file '{args[0]}': [Errno 2] No such file or directory"
            else:
                output = f"Python {sys.version.split()[0]} (simulated interactive console, write python script.py to execute)"
        elif cmd == "help":
            output = "Comandos implementados en Python:\n  ls, cd, pwd, mkdir, touch, cat, rm, echo, grep, whoami, uname, date, neofetch, python3, history, clear"
        else:
            output = f"bash: {cmd}: command not found"

        # Aplicar redirección si existe
        if redirect_mode and target_file:
            curr = self._resolve_node(".")
            if target_file not in curr.children:
                curr.children[target_file] = VirtualNode(target_file, is_dir=False, content="", owner=self.username)
            if redirect_mode == "overwrite":
                curr.children[target_file].content = output
            elif redirect_mode == "append":
                curr.children[target_file].content += ("\n" + output if curr.children[target_file].content else output)
            output = ""

        return {
            'output': output,
            'cwd': self._get_display_path(),
            'prompt': self.get_prompt()
        }


if __name__ == '__main__':
    term = LinuxTerminalSimulator()
    print("Iniciando Linux Terminal Simulator en Python CLI. Escribe 'exit' para salir.\n")
    while True:
        try:
            line = input(term.get_prompt())
            if line.strip() == "exit": break
            res = term.execute_command(line)
            if res['output'] == "__CLEAR__":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif res['output']:
                print(res['output'])
        except (KeyboardInterrupt, EOFError):
            break
