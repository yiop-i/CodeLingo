/**
 * LINUX-TERM.JS - SIMULADOR AVANZADO DE TERMINAL LINUX BASH
 * Sistema de archivos virtual jerárquico, comandos estándar, autocompletado y persistencia
 */

class LinuxTerminal {
  constructor() {
    this.history = [];
    this.historyIndex = -1;
    this.currentPath = '/home/user';
    this.currentUser = 'user';
    this.hostname = 'linux-vm';
    
    this.initFileSystem();
    this.initDOM();
    this.bindEvents();
  }

  initFileSystem() {
    const savedFs = localStorage.getItem('linux_vfs');
    if (savedFs) {
      try {
        this.fs = JSON.parse(savedFs);
        return;
      } catch (e) {
        console.error("Error restaurando VFS:", e);
      }
    }

    // Sistema de archivos Linux predeterminado
    this.fs = {
      name: '/',
      type: 'dir',
      children: {
        'bin': {
          type: 'dir',
          children: {
            'bash': { type: 'file', content: 'ELF 64-bit executable' },
            'ls': { type: 'file', content: 'ELF 64-bit executable' },
            'cat': { type: 'file', content: 'ELF 64-bit executable' },
            'python3': { type: 'file', content: 'Python 3.12.3 interpreter' },
            'gcc': { type: 'file', content: 'GCC 13.2.0 compiler' }
          }
        },
        'etc': {
          type: 'dir',
          children: {
            'os-release': {
              type: 'file',
              content: 'NAME="Ubuntu"\nVERSION="24.04 LTS (Noble Numbat)"\nID=ubuntu\nPRETTY_NAME="Ubuntu 24.04 LTS"\nVERSION_CODENAME=noble'
            },
            'hostname': { type: 'file', content: 'linux-vm\n' }
          }
        },
        'home': {
          type: 'dir',
          children: {
            'user': {
              type: 'dir',
              children: {
                'README.txt': {
                  type: 'file',
                  content: '¡Bienvenido al Simulador de Linux!\nPuedes usar comandos como ls, cd, cat, mkdir, touch, rm, echo, python3, gcc, neofetch, clear y help.'
                },
                'hola.py': {
                  type: 'file',
                  content: 'print("¡Hola desde Python 3 en Linux!")\nfor i in range(1, 6):\n    print(f"Paso {i} completado")'
                },
                'programa.c': {
                  type: 'file',
                  content: '#include <stdio.h>\n\nint main() {\n    printf("Compilado exitosamente con GCC en Linux.\\n");\n    return 0;\n}'
                },
                'proyectos': {
                  type: 'dir',
                  children: {
                    'notas.md': { type: 'file', content: '# Mis Proyectos\n- Aprender Linux Shell\n- Montar servidor Docker\n- Programar en C y Python' }
                  }
                }
              }
            }
          }
        },
        'var': { type: 'dir', children: { 'log': { type: 'dir', children: {} } } },
        'tmp': { type: 'dir', children: {} }
      }
    };
    this.saveFS();
  }

  saveFS() {
    try {
      localStorage.setItem('linux_vfs', JSON.stringify(this.fs));
    } catch(e) {}
  }

  initDOM() {
    this.screen = document.getElementById('linuxTermScreen');
    this.historyEl = document.getElementById('linuxTermHistory');
    this.input = document.getElementById('linuxTermInput');
    this.promptEl = document.getElementById('linuxPromptText');
    this.btnClear = document.getElementById('btnLinuxClear');
    this.btnReset = document.getElementById('btnLinuxFsReset');
    this.updatePrompt();
  }

  bindEvents() {
    if (!this.input) return;

    // Al hacer click en la pantalla de terminal, enfocar el input
    this.screen.addEventListener('click', () => this.input.focus());

    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const cmd = this.input.value;
        this.input.value = '';
        this.executeCommand(cmd);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (this.historyIndex > 0) {
          this.historyIndex--;
          this.input.value = this.history[this.historyIndex] || '';
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (this.historyIndex < this.history.length - 1) {
          this.historyIndex++;
          this.input.value = this.history[this.historyIndex] || '';
        } else {
          this.historyIndex = this.history.length;
          this.input.value = '';
        }
      } else if (e.key === 'Tab') {
        e.preventDefault();
        this.autocomplete();
      } else if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        this.clear();
      } else if (e.ctrlKey && e.key === 'c') {
        e.preventDefault();
        this.printPromptEcho(this.input.value + '^C');
        this.input.value = '';
      }
    });

    if (this.btnClear) this.btnClear.addEventListener('click', () => this.clear());
    if (this.btnReset) {
      this.btnReset.addEventListener('click', () => {
        localStorage.removeItem('linux_vfs');
        this.initFileSystem();
        this.currentPath = '/home/user';
        this.updatePrompt();
        this.println('<span class="hl-green">Sistema de archivos restaurado al estado inicial.</span>');
      });
    }

    // Botones móviles de atajos
    document.querySelectorAll('.mobile-term-bar .mob-key').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        const cmd = btn.dataset.cmd;
        if (cmd) {
          this.input.value = cmd;
          this.executeCommand(cmd);
          this.input.focus();
        } else if (key === 'Tab') {
          this.autocomplete();
        } else if (key === 'ArrowUp') {
          if (this.historyIndex > 0) {
            this.historyIndex--;
            this.input.value = this.history[this.historyIndex] || '';
          }
        } else if (key === 'ArrowDown') {
          if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.input.value = this.history[this.historyIndex] || '';
          } else {
            this.historyIndex = this.history.length;
            this.input.value = '';
          }
        } else if (key === 'CtrlC') {
          this.printPromptEcho(this.input.value + '^C');
          this.input.value = '';
        }
      });
    });
  }

  updatePrompt() {
    let displayPath = this.currentPath;
    if (displayPath.startsWith('/home/user')) {
      displayPath = displayPath.replace('/home/user', '~');
    }
    this.promptEl.innerHTML = `<span class="user">${this.currentUser}@${this.hostname}</span>:<span class="path">${displayPath}</span>$ `;
  }

  printPromptEcho(cmd) {
    let displayPath = this.currentPath;
    if (displayPath.startsWith('/home/user')) {
      displayPath = displayPath.replace('/home/user', '~');
    }
    const entry = document.createElement('div');
    entry.className = 'term-cmd-entry';
    entry.innerHTML = `<span class="hl-cyan">${this.currentUser}@${this.hostname}</span>:<span class="hl-green">${displayPath}</span>$ ${this.escapeHtml(cmd)}`;
    this.historyEl.appendChild(entry);
    this.scrollToBottom();
  }

  println(htmlContent) {
    const out = document.createElement('div');
    out.className = 'term-cmd-output';
    out.innerHTML = htmlContent;
    this.historyEl.appendChild(out);
    this.scrollToBottom();
  }

  clear() {
    this.historyEl.innerHTML = '';
  }

  scrollToBottom() {
    this.screen.scrollTop = this.screen.scrollHeight;
  }

  escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Resolución de nodos en el VFS
  resolvePath(pathStr) {
    let target = pathStr.trim();
    if (target.startsWith('~')) {
      target = '/home/user' + target.substring(1);
    }
    let absPath = target.startsWith('/') ? target : (this.currentPath === '/' ? '/' + target : this.currentPath + '/' + target);
    
    // Normalizar . y ..
    const segments = absPath.split('/').filter(Boolean);
    const resolvedSegments = [];
    for (const seg of segments) {
      if (seg === '.') continue;
      if (seg === '..') {
        if (resolvedSegments.length > 0) resolvedSegments.pop();
      } else {
        resolvedSegments.push(seg);
      }
    }

    let current = this.fs;
    for (const seg of resolvedSegments) {
      if (!current.children || !current.children[seg]) {
        return null;
      }
      current = current.children[seg];
    }
    return {
      node: current,
      path: '/' + resolvedSegments.join('/'),
      parentPath: '/' + resolvedSegments.slice(0, -1).join('/'),
      name: resolvedSegments[resolvedSegments.length - 1] || ''
    };
  }

  async executeCommand(rawCmd) {
    const cmdStr = rawCmd.trim();
    if (!cmdStr) {
      this.printPromptEcho('');
      return;
    }

    this.history.push(cmdStr);
    this.historyIndex = this.history.length;
    this.printPromptEcho(cmdStr);

    // Conexión con el motor de terminal Linux en Python
    try {
      const resp = await fetch('/api/linux/exec', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: cmdStr })
      });
      if (resp.ok) {
        const res = await resp.json();
        if (res.output === '__CLEAR__') {
          this.clear();
          return;
        }
        if (res.output) {
          this.println(this.escapeHtml(res.output).replace(/\n/g, '<br>'));
        }
        if (res.cwd) {
          this.currentPath = res.cwd;
          this.updatePrompt();
        }
        return;
      }
    } catch(err) {
      // Fallback a motor local si no hay servidor activo
    }

    const parts = cmdStr.split(/\s+/);
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    switch (cmd) {
      case 'help':
        this.println(`
<span class="hl-cyan">Comandos de Linux Bash soportados:</span>
  <span class="hl-green">ls [-la]</span>         Lista archivos y directorios
  <span class="hl-green">cd [dir]</span>         Cambia de directorio
  <span class="hl-green">pwd</span>              Muestra la ruta actual
  <span class="hl-green">cat [archivo]</span>    Muestra el contenido de un archivo
  <span class="hl-green">mkdir [dir]</span>      Crea un nuevo directorio
  <span class="hl-green">touch [archivo]</span>  Crea un archivo vacío
  <span class="hl-green">rm [-r] [obj]</span>    Elimina un archivo o directorio
  <span class="hl-green">echo [texto]</span>     Imprime texto en pantalla
  <span class="hl-green">grep [patrón] [f]</span>Busca coincidencias en un archivo
  <span class="hl-green">whoami / host</span>    Muestra información de usuario y host
  <span class="hl-green">uname -a</span>         Información del kernel Linux
  <span class="hl-green">date / uptime</span>    Fecha y tiempo de actividad
  <span class="hl-green">python3 [arch.py]</span>Ejecuta scripts de Python
  <span class="hl-green">gcc [prog.c]</span>     Simula la compilación con GCC
  <span class="hl-green">neofetch</span>         Información estilizada del sistema
  <span class="hl-green">clear</span>            Limpia la terminal (Ctrl+L)
        `);
        break;

      case 'clear':
        this.clear();
        break;

      case 'pwd':
        this.println(this.currentPath);
        break;

      case 'whoami':
        this.println(this.currentUser);
        break;

      case 'hostname':
        this.println(this.hostname);
        break;

      case 'uname':
        if (args.includes('-a')) {
          this.println('Linux linux-vm 6.8.0-40-generic #40-Ubuntu SMP PREEMPT_DYNAMIC Sat Jun 1 12:00:00 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux');
        } else {
          this.println('Linux');
        }
        break;

      case 'date':
        this.println(new Date().toString());
        break;

      case 'uptime':
        this.println(' 21:10:00 up 4 days,  2:14,  1 user,  load average: 0.15, 0.08, 0.02');
        break;

      case 'ls': {
        const showAll = args.some(a => a.includes('a'));
        const showLong = args.some(a => a.includes('l'));
        const targetPath = args.find(a => !a.startsWith('-')) || '.';
        
        const resolved = this.resolvePath(targetPath);
        if (!resolved) {
          this.println(`<span class="hl-red">ls: no se puede acceder a '${targetPath}': No existe el archivo o el directorio</span>`);
          return;
        }

        if (resolved.node.type === 'file') {
          this.println(targetPath);
          return;
        }

        const entries = Object.keys(resolved.node.children || {}).sort();
        if (entries.length === 0) return;

        if (showLong) {
          let out = `total ${entries.length * 4}\n`;
          entries.forEach(name => {
            const item = resolved.node.children[name];
            const isDir = item.type === 'dir';
            const perms = isDir ? 'drwxr-xr-x 2' : '-rw-r--r-- 1';
            const size = isDir ? '4096' : (item.content ? item.content.length : 0).toString().padStart(5);
            const coloredName = isDir ? `<span class="hl-cyan">${name}/</span>` : `<span class="hl-green">${name}</span>`;
            out += `${perms} user user ${size} Nov  2 21:00 ${coloredName}\n`;
          });
          this.println(out);
        } else {
          const list = entries.map(name => {
            const isDir = resolved.node.children[name].type === 'dir';
            return isDir ? `<span class="hl-cyan">${name}/</span>` : name;
          }).join('  ');
          this.println(list);
        }
        break;
      }

      case 'cd': {
        const dest = args[0] || '~';
        const resolved = this.resolvePath(dest);
        if (!resolved) {
          this.println(`<span class="hl-red">bash: cd: ${dest}: No existe el archivo o el directorio</span>`);
          return;
        }
        if (resolved.node.type !== 'dir') {
          this.println(`<span class="hl-red">bash: cd: ${dest}: No es un directorio</span>`);
          return;
        }
        this.currentPath = resolved.path;
        this.updatePrompt();
        break;
      }

      case 'cat': {
        if (!args[0]) {
          this.println(`<span class="hl-red">cat: falta un argumento de archivo</span>`);
          return;
        }
        const resolved = this.resolvePath(args[0]);
        if (!resolved) {
          this.println(`<span class="hl-red">cat: ${args[0]}: No existe el archivo</span>`);
          return;
        }
        if (resolved.node.type === 'dir') {
          this.println(`<span class="hl-red">cat: ${args[0]}: Es un directorio</span>`);
          return;
        }
        this.println(this.escapeHtml(resolved.node.content || ''));
        break;
      }

      case 'mkdir': {
        if (!args[0]) {
          this.println(`<span class="hl-red">mkdir: falta un operando</span>`);
          return;
        }
        const dirName = args[0];
        const cur = this.resolvePath('.');
        if (cur.node.children[dirName]) {
          this.println(`<span class="hl-red">mkdir: no se puede crear el directorio '${dirName}': El archivo ya existe</span>`);
          return;
        }
        cur.node.children[dirName] = { type: 'dir', children: {} };
        this.saveFS();
        break;
      }

      case 'touch': {
        if (!args[0]) {
          this.println(`<span class="hl-red">touch: falta un operando</span>`);
          return;
        }
        const fileName = args[0];
        const cur = this.resolvePath('.');
        if (!cur.node.children[fileName]) {
          cur.node.children[fileName] = { type: 'file', content: '' };
          this.saveFS();
        }
        break;
      }

      case 'rm': {
        if (!args[0]) {
          this.println(`<span class="hl-red">rm: falta un operando</span>`);
          return;
        }
        const recursive = args.includes('-r') || args.includes('-rf');
        const target = args.find(a => !a.startsWith('-'));
        const cur = this.resolvePath('.');
        if (!cur.node.children[target]) {
          this.println(`<span class="hl-red">rm: no se puede borrar '${target}': No existe el archivo</span>`);
          return;
        }
        if (cur.node.children[target].type === 'dir' && !recursive) {
          this.println(`<span class="hl-red">rm: no se puede borrar '${target}': Es un directorio (use -r)</span>`);
          return;
        }
        delete cur.node.children[target];
        this.saveFS();
        break;
      }

      case 'echo': {
        const text = args.join(' ');
        this.println(this.escapeHtml(text));
        break;
      }

      case 'grep': {
        if (args.length < 2) {
          this.println(`<span class="hl-red">Uso: grep [patrón] [archivo]</span>`);
          return;
        }
        const pattern = args[0];
        const resolved = this.resolvePath(args[1]);
        if (!resolved || resolved.node.type !== 'file') {
          this.println(`<span class="hl-red">grep: ${args[1]}: No se pudo leer el archivo</span>`);
          return;
        }
        const lines = (resolved.node.content || '').split('\n');
        const matches = lines.filter(l => l.includes(pattern));
        if (matches.length > 0) {
          this.println(matches.map(l => l.replace(new RegExp(pattern, 'g'), `<span class="hl-red"><strong>${pattern}</strong></span>`)).join('\n'));
        }
        break;
      }

      case 'python3':
      case 'python': {
        if (!args[0]) {
          this.println('Python 3.12.3 (main, Apr 10 2026, 05:33:42) [GCC 13.2.0] on linux\nEscriba código desde el simulador de VS Code para una experiencia interactiva completa.');
          return;
        }
        const resolved = this.resolvePath(args[0]);
        if (!resolved) {
          this.println(`<span class="hl-red">python3: can't open file '${args[0]}': [Errno 2] No such file or directory</span>`);
          return;
        }
        // Ejecución simulada de Python
        this.println(`<span class="hl-cyan">[Ejecutando ${args[0]} en Python 3.12]</span>`);
        try {
          // Si tiene print(), evaluar líneas
          const lines = resolved.node.content.split('\n');
          lines.forEach(line => {
            const m = line.match(/print\s*\(\s*["'](.*)["']\s*\)/);
            if (m) this.println(this.escapeHtml(m[1]));
          });
        } catch(e) {
          this.println(this.escapeHtml(resolved.node.content));
        }
        break;
      }

      case 'gcc': {
        if (!args[0]) {
          this.println(`<span class="hl-red">gcc: fatal error: no input files</span>\ncompilation terminated.`);
          return;
        }
        const resolved = this.resolvePath(args[0]);
        if (!resolved) {
          this.println(`<span class="hl-red">gcc: error: ${args[0]}: No such file or directory</span>`);
          return;
        }
        const cur = this.resolvePath('.');
        cur.node.children['a.out'] = { type: 'file', content: 'ELF 64-bit LSB pie executable' };
        this.saveFS();
        this.println(`<span class="hl-green">Compilación exitosa. Generado './a.out'.</span>`);
        break;
      }

      case './a.out': {
        const cur = this.resolvePath('.');
        if (cur.node.children['a.out']) {
          this.println('Compilado exitosamente con GCC en Linux.\nProceso finalizado con código de salida 0.');
        } else {
          this.println('<span class="hl-red">bash: ./a.out: No existe el archivo o el directorio</span>');
        }
        break;
      }

      case 'neofetch':
        this.println(`
<span class="hl-cyan">        -/oyddmdhs+:.</span>                <span class="hl-green">user</span>@<span class="hl-cyan">linux-vm</span>
<span class="hl-cyan">     -odNMMMMMMMMNNmhy+-</span>             -------------------
<span class="hl-cyan">   -yNMMMMMMMMMMMdddddhhy+-</span>          <span class="hl-yellow">OS:</span> Ubuntu 24.04 LTS x86_64
<span class="hl-cyan">  +mMMMMMMMMNNNmdhhhhhhyo+/-</span>         <span class="hl-yellow">Host:</span> Virtual Machine v2.0
<span class="hl-cyan"> +mMMMMMMMMNmhhhhhysoo+/-</span>             <span class="hl-yellow">Kernel:</span> 6.8.0-generic
<span class="hl-cyan">.dMMMMMMMMmhhhhhyso++//-</span>             <span class="hl-yellow">Uptime:</span> 4 days, 2 hours
<span class="hl-cyan">hNMMMMMMMmyyyyso++//-</span>                <span class="hl-yellow">Shell:</span> bash 5.2.21
<span class="hl-cyan">mMMMMMMMNdyyyso++//-</span>                 <span class="hl-yellow">CPU:</span> 13th Gen Intel Core i9-13900K (8) @ 5.4GHz
<span class="hl-cyan">mMMMMMMMNdyyyso++//-</span>                 <span class="hl-yellow">Memory:</span> 3840MiB / 16384MiB
<span class="hl-cyan">hNMMMMMMMmyyyyso++//-</span>
<span class="hl-cyan">.dMMMMMMMMmhhhhhyso++//-</span>
<span class="hl-cyan"> +mMMMMMMMMNmhhhhhysoo+/-</span>
<span class="hl-cyan">  +mMMMMMMMMNNNmdhhhhhhyo+/-</span>
<span class="hl-cyan">   -yNMMMMMMMMMMMdddddhhy+-</span>
<span class="hl-cyan">     -odNMMMMMMMMNNmhy+-</span>
<span class="hl-cyan">        -/oyddmdhs+:.</span>
        `);
        break;

      default:
        this.println(`<span class="hl-red">bash: comando no encontrado: ${this.escapeHtml(cmd)}</span>. Escribe <span class="hl-yellow">'help'</span> para ver los comandos disponibles.`);
    }
  }

  autocomplete() {
    const val = this.input.value;
    const parts = val.split(' ');
    const lastWord = parts[parts.length - 1];
    const cur = this.resolvePath('.');
    if (!cur || !cur.node.children) return;

    const candidates = Object.keys(cur.node.children).filter(k => k.startsWith(lastWord));
    if (candidates.length === 1) {
      parts[parts.length - 1] = candidates[0];
      this.input.value = parts.join(' ');
    } else if (candidates.length > 1) {
      this.printPromptEcho(val);
      this.println(candidates.join('   '));
    }
  }
}
