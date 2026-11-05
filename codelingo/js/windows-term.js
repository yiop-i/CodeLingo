/**
 * WINDOWS-TERM.JS - SIMULADOR DE TERMINAL WINDOWS (CMD & POWERSHELL)
 * Simulación de consola de comandos de Windows y PowerShell 7
 */

class WindowsTerminal {
  constructor() {
    this.shellMode = 'ps'; // 'ps' o 'cmd'
    this.history = [];
    this.historyIndex = -1;
    this.currentPath = 'C:\\Users\\User';
    
    this.initFileSystem();
    this.initDOM();
    this.bindEvents();
  }

  initFileSystem() {
    this.fs = {
      'C:': {
        'Users': {
          'User': {
            'Desktop': {},
            'Documents': {
              'reporte.docx': 'Documento de Word - Reporte de Rendimiento',
              'script.ps1': 'Write-Host "¡Ejecutando PowerShell en Windows!"\nGet-Process | Select-Object -First 5'
            },
            'Downloads': {
              'setup_vscode.exe': 'VS Code Installer x64'
            },
            'proyectos': {
              'app.cs': 'using System;\nclass Program {\n  static void Main() {\n    Console.WriteLine("Hola desde C# en Windows");\n  }\n}'
            }
          }
        },
        'Windows': {
          'System32': {
            'cmd.exe': 'Binary',
            'powershell.exe': 'Binary',
            'ipconfig.exe': 'Binary'
          }
        },
        'Program Files': {}
      }
    };
  }

  initDOM() {
    this.screen = document.getElementById('winTermScreen');
    this.historyEl = document.getElementById('winTermHistory');
    this.input = document.getElementById('winTermInput');
    this.promptEl = document.getElementById('winPromptText');
    this.bannerEl = document.getElementById('winBannerText');
    this.tabs = document.querySelectorAll('.win-tab-btn');
    this.updatePrompt();
  }

  setShellMode(mode) {
    this.shellMode = mode;
    this.tabs.forEach(tab => {
      tab.classList.toggle('active', tab.dataset.shell === mode);
    });

    if (mode === 'ps') {
      this.screen.classList.add('powershell-active');
      this.bannerEl.innerHTML = `Windows PowerShell\nCopyright (C) Microsoft Corporation. Todos los derechos reservados.\n\nInstale la versión más reciente de PowerShell para nuevas características y mejoras.\nEscriba <span class="hl-yellow">'help'</span>, <span class="hl-cyan">'Get-Process'</span>, <span class="hl-green">'dir'</span>, <span class="hl-yellow">'systeminfo'</span> o <span class="hl-cyan">'ipconfig'</span>.`;
    } else {
      this.screen.classList.remove('powershell-active');
      this.bannerEl.innerHTML = `Microsoft Windows [Versión 10.0.22631.3880]\n(c) Microsoft Corporation. Todos los derechos reservados.\n\nEscriba <span class="hl-yellow">'help'</span>, <span class="hl-green">'dir'</span>, <span class="hl-yellow">'cls'</span> o <span class="hl-cyan">'ipconfig'</span>.`;
    }
    this.updatePrompt();
  }

  updatePrompt() {
    if (this.shellMode === 'ps') {
      this.promptEl.textContent = `PS ${this.currentPath}> `;
    } else {
      this.promptEl.textContent = `${this.currentPath}> `;
    }
  }

  bindEvents() {
    if (!this.input) return;

    this.screen.addEventListener('click', () => this.input.focus());

    this.tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        this.setShellMode(tab.dataset.shell);
      });
    });

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
      }
    });

    // Botones de atajos móviles de Windows
    document.querySelectorAll('.win-mobile-bar .mob-key').forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.dataset.wincmd;
        const key = btn.dataset.key;
        if (cmd) {
          this.input.value = cmd;
          this.executeCommand(cmd);
          this.input.focus();
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
        }
      });
    });
  }

  printPromptEcho(cmd) {
    const entry = document.createElement('div');
    entry.className = 'term-cmd-entry';
    const promptStr = this.shellMode === 'ps' ? `PS ${this.currentPath}&gt; ` : `${this.currentPath}&gt; `;
    entry.innerHTML = `<span class="win-prompt">${promptStr}</span>${this.escapeHtml(cmd)}`;
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

  getCurrentDirNode() {
    const parts = this.currentPath.split('\\').filter(Boolean);
    let cur = this.fs;
    for (const p of parts) {
      if (cur[p] && typeof cur[p] === 'object') {
        cur = cur[p];
      } else {
        return null;
      }
    }
    return cur;
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

    // Conexión con el motor de terminal Windows en Python
    try {
      const resp = await fetch('/api/windows/exec', {
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
<span class="hl-cyan">Comandos de Windows soportados:</span>
  <span class="hl-green">DIR</span>              Muestra la lista de archivos y subdirectorios
  <span class="hl-green">CD [ruta]</span>        Cambia el directorio actual
  <span class="hl-green">CLS / CLEAR</span>      Limpia la pantalla de comandos
  <span class="hl-green">MD / MKDIR</span>       Crea un nuevo directorio
  <span class="hl-green">DEL</span>              Elimina uno o más archivos
  <span class="hl-green">TYPE</span>             Muestra el contenido de un archivo de texto
  <span class="hl-green">VER</span>              Muestra la versión de Windows
  <span class="hl-green">SYSTEMINFO</span>       Muestra la configuración del sistema operativo
  <span class="hl-green">IPCONFIG</span>         Muestra la configuración de red TCP/IP
  <span class="hl-green">TASKLIST</span>         Lista las aplicaciones y servicios en ejecución
  <span class="hl-green">Get-Process</span>      (PowerShell) Muestra procesos activos
  <span class="hl-green">Write-Host</span>       (PowerShell) Imprime mensajes en la consola
  <span class="hl-green">POWERSHELL / CMD</span> Cambia el modo de emulación
        `);
        break;

      case 'cls':
      case 'clear':
        this.clear();
        break;

      case 'ver':
        this.println('Microsoft Windows [Versión 10.0.22631.3880]');
        break;

      case 'powershell':
        this.setShellMode('ps');
        this.println('Cambiado a Windows PowerShell.');
        break;

      case 'cmd':
        this.setShellMode('cmd');
        this.println('Cambiado a Símbolo del Sistema (CMD).');
        break;

      case 'dir':
      case 'ls':
      case 'get-childitem': {
        const cur = this.getCurrentDirNode();
        if (!cur) return;
        const entries = Object.keys(cur);
        
        let out = ` El volumen de la unidad C no tiene etiqueta.\n El número de serie del volumen es 8E34-B9A1\n\n Directorio de ${this.currentPath}\n\n`;
        let dirCount = 2;
        let fileCount = 0;

        out += `02/11/2026  09:00 PM    &lt;DIR&gt;          .\n`;
        out += `02/11/2026  09:00 PM    &lt;DIR&gt;          ..\n`;

        entries.forEach(name => {
          const isDir = typeof cur[name] === 'object';
          if (isDir) {
            dirCount++;
            out += `02/11/2026  09:10 PM    &lt;DIR&gt;          <span class="hl-cyan">${name}</span>\n`;
          } else {
            fileCount++;
            const size = (cur[name] ? cur[name].length : 512).toString().padStart(14);
            out += `02/11/2026  09:12 PM ${size} <span class="hl-green">${name}</span>\n`;
          }
        });

        out += `              ${fileCount} archivos\n`;
        out += `              ${dirCount} dirs   485.291.827.200 bytes libres\n`;
        this.println(out);
        break;
      }

      case 'cd': {
        if (!args[0]) {
          this.println(this.currentPath);
          return;
        }
        const target = args[0];
        if (target === '..') {
          const parts = this.currentPath.split('\\').filter(Boolean);
          if (parts.length > 1) {
            parts.pop();
            this.currentPath = parts.join('\\');
            if (parts.length === 1) this.currentPath += '\\';
          }
          this.updatePrompt();
          return;
        }

        const cur = this.getCurrentDirNode();
        if (cur && cur[target] && typeof cur[target] === 'object') {
          this.currentPath = this.currentPath.endsWith('\\') ? this.currentPath + target : this.currentPath + '\\' + target;
          this.updatePrompt();
        } else {
          this.println(`El sistema no puede encontrar la ruta especificada: ${target}`);
        }
        break;
      }

      case 'type':
      case 'cat': {
        if (!args[0]) {
          this.println('La sintaxis del comando no es correcta.');
          return;
        }
        const cur = this.getCurrentDirNode();
        if (cur && cur[args[0]] && typeof cur[args[0]] === 'string') {
          this.println(this.escapeHtml(cur[args[0]]));
        } else {
          this.println(`El sistema no puede encontrar el archivo especificado: ${args[0]}`);
        }
        break;
      }

      case 'md':
      case 'mkdir': {
        if (!args[0]) {
          this.println('La sintaxis del comando no es correcta.');
          return;
        }
        const cur = this.getCurrentDirNode();
        if (cur) {
          cur[args[0]] = {};
          this.println(`Directorio '${args[0]}' creado.`);
        }
        break;
      }

      case 'del': {
        if (!args[0]) {
          this.println('La sintaxis del comando no es correcta.');
          return;
        }
        const cur = this.getCurrentDirNode();
        if (cur && cur[args[0]] !== undefined) {
          delete cur[args[0]];
          this.println(`Archivo '${args[0]}' eliminado.`);
        } else {
          this.println(`No se pudo encontrar ${args[0]}`);
        }
        break;
      }

      case 'echo':
      case 'write-host': {
        this.println(this.escapeHtml(args.join(' ')));
        break;
      }

      case 'systeminfo':
        this.println(`
Nombre de host:              DESKTOP-WIN11PRO
Nombre del sistema operativo:Microsoft Windows 11 Pro
Versión del sistema operativo:10.0.22631 N/D Compilación 22631
Fabricante del sistema:      ASUS ROG STRIX
Modelo del sistema:          Custom Gaming PC
Tipo de sistema:             x64-based PC
Procesador(es):              1 Procesadores instalados.
                             [01]: Intel64 Family 6 Model 183 ~3000 Mhz
Versión de BIOS:             American Megatrends Inc. 3.40, 15/01/2026
Memoria física total:        32.684 MB
Memoria física disponible:   24.120 MB
Tarjeta(s) de red:           1 NIC instaladas.
                             [01]: Intel(R) Wi-Fi 6E AX211 160MHz
        `);
        break;

      case 'ipconfig':
        this.println(`
Configuración IP de Windows

Adaptador de Ethernet Ethernet 2:
   Estado de los medios. . . . . . . . . . . : Medios desconectados

Adaptador de LAN inalámbrica Wi-Fi:
   Sufijo DNS específico para la conexión. . : localdomain
   Vínculo: dirección IPv6 local. . . : fe80::9a41:45cf:82b1:10d%14
   Dirección IPv4. . . . . . . . . . . . . . : <span class="hl-cyan">192.168.1.145</span>
   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
   Puerta de enlace predeterminada . . . . . : <span class="hl-yellow">192.168.1.1</span>
        `);
        break;

      case 'tasklist':
      case 'get-process':
        this.println(`
Nombre de imagen               PID Nombre de sesión Núm. de ses  Uso de mem
========================= ======== ================ ============ ============
System Idle Process              0 Services                    0          8 K
System                           4 Services                    0      3.820 K
Registry                       144 Services                    0     94.120 K
smss.exe                       480 Services                    0      1.140 K
csrss.exe                      688 Services                    0      5.230 K
explorer.exe                  3140 Console                     1    142.900 K
Code.exe                      7820 Console                     1    285.400 K
powershell.exe                9240 Console                     1     68.100 K
chrome.exe                   12410 Console                     1    310.200 K
        `);
        break;

      default:
        if (this.shellMode === 'ps') {
          this.println(`<span class="hl-red">${this.escapeHtml(cmd)} : El término '${this.escapeHtml(cmd)}' no se reconoce como nombre de un cmdlet, función, archivo de script o programa ejecutable.</span>`);
        } else {
          this.println(`'${this.escapeHtml(cmd)}' no se reconoce como un comando interno o externo,\nprograma o archivo por lotes ejecutable.`);
        }
    }
  }

  autocomplete() {
    const val = this.input.value;
    const parts = val.split(' ');
    const lastWord = parts[parts.length - 1];
    const cur = this.getCurrentDirNode();
    if (!cur) return;

    const candidates = Object.keys(cur).filter(k => k.toLowerCase().startsWith(lastWord.toLowerCase()));
    if (candidates.length === 1) {
      parts[parts.length - 1] = candidates[0];
      this.input.value = parts.join(' ');
    }
  }
}
