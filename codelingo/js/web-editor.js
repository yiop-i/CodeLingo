/**
 * WEB-EDITOR.JS - SIMULADOR DE DESARROLLO WEB (HTML, CSS & JS LIVE PREVIEW)
 * Renderizado en tiempo real en iframe, cambio de dispositivos y consola integrada
 */

class WebStudio {
  constructor() {
    this.templates = {
      portfolio: {
        html: `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Portafolio Desarrollador</title>
</head>
<body>
  <div class="card">
    <div class="avatar-glow">
      <div class="avatar">🚀</div>
    </div>
    <h1>Alex Rivera</h1>
    <p class="role">Full Stack & Systems Engineer</p>
    <div class="tags">
      <span class="tag">Python</span>
      <span class="tag">C++</span>
      <span class="tag">Linux</span>
      <span class="tag">Hardware</span>
    </div>
    <div class="metrics">
      <div class="metric"><span class="val" id="counter1">0</span><span class="lbl">Proyectos</span></div>
      <div class="metric"><span class="val" id="counter2">0</span><span class="lbl">Commits</span></div>
      <div class="metric"><span class="val">100%</span><span class="lbl">Uptime</span></div>
    </div>
    <button class="btn" id="btnInteract">¡Saludar en Consola!</button>
  </div>
</body>
</html>`,
        css: `* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: radial-gradient(circle at top, #1e2638, #0f111a);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}
.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  padding: 32px 24px;
  max-width: 380px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  animation: float 4s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.avatar-glow {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #007acc, #4ec9b0);
  border-radius: 50%;
  padding: 3px;
  box-shadow: 0 0 20px rgba(0, 122, 204, 0.5);
}
.avatar {
  width: 100%;
  height: 100%;
  background: #181920;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
}
h1 { font-size: 24px; margin-bottom: 4px; font-weight: 700; }
.role { color: #4ec9b0; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-bottom: 20px; }
.tag {
  background: rgba(0, 122, 204, 0.18);
  border: 1px solid rgba(0, 122, 204, 0.4);
  color: #58a6ff;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 20px;
}
.metrics { display: flex; justify-content: space-around; margin-bottom: 24px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px; }
.metric { display: flex; flex-direction: column; }
.metric .val { font-size: 20px; font-weight: 800; color: #ffb703; }
.metric .lbl { font-size: 11px; color: #8c93a0; }
.btn {
  background: linear-gradient(135deg, #007acc, #005a9e);
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 100%;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 122, 204, 0.4);
}`,
        js: `console.log("Portafolio cargado en tiempo real.");

// Animación de contadores
let pCount = 0;
let cCount = 0;
const targetP = 42;
const targetC = 850;

const timer = setInterval(() => {
  if (pCount < targetP) pCount += 2;
  if (cCount < targetC) cCount += 35;
  
  const elP = document.getElementById("counter1");
  const elC = document.getElementById("counter2");
  if (elP) elP.innerText = pCount;
  if (elC) elC.innerText = cCount;

  if (pCount >= targetP && cCount >= targetC) {
    clearInterval(timer);
    console.log("Métricas calculadas con éxito.");
  }
}, 50);

document.getElementById("btnInteract").addEventListener("click", () => {
  console.log("¡Hola desde el botón interactivo de Web Studio!");
  alert("¡Interacción exitosa! Tu diseño web responde en tiempo real.");
});`
      },
      calculator: {
        html: `<div class="calc-box">
  <div class="display" id="calcDisplay">0</div>
  <div class="grid">
    <button class="c-btn op" onclick="clearCalc()">AC</button>
    <button class="c-btn op" onclick="pressKey('+/-')">±</button>
    <button class="c-btn op" onclick="pressKey('%')">%</button>
    <button class="c-btn act" onclick="pressKey('/')">÷</button>
    <button class="c-btn" onclick="pressKey('7')">7</button>
    <button class="c-btn" onclick="pressKey('8')">8</button>
    <button class="c-btn" onclick="pressKey('9')">9</button>
    <button class="c-btn act" onclick="pressKey('*')">×</button>
    <button class="c-btn" onclick="pressKey('4')">4</button>
    <button class="c-btn" onclick="pressKey('5')">5</button>
    <button class="c-btn" onclick="pressKey('6')">6</button>
    <button class="c-btn act" onclick="pressKey('-')">−</button>
    <button class="c-btn" onclick="pressKey('1')">1</button>
    <button class="c-btn" onclick="pressKey('2')">2</button>
    <button class="c-btn" onclick="pressKey('3')">3</button>
    <button class="c-btn act" onclick="pressKey('+')">+</button>
    <button class="c-btn zero" onclick="pressKey('0')">0</button>
    <button class="c-btn" onclick="pressKey('.')">.</button>
    <button class="c-btn equal" onclick="calcResult()">=</button>
  </div>
</div>`,
        css: `body {
  background: #111;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  margin: 0;
  font-family: sans-serif;
}
.calc-box {
  width: 300px;
  background: #222;
  padding: 20px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.8);
}
.display {
  background: #000;
  color: #0f0;
  font-family: monospace;
  font-size: 36px;
  text-align: right;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
}
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.c-btn {
  background: #333;
  color: #fff;
  border: none;
  font-size: 20px;
  height: 55px;
  border-radius: 50%;
  cursor: pointer;
  transition: 0.1s;
}
.c-btn:active { transform: scale(0.92); }
.c-btn.op { background: #555; }
.c-btn.act { background: #ff9500; }
.c-btn.equal { background: #27c93f; }
.c-btn.zero { grid-column: span 2; border-radius: 28px; }`,
        js: `let expr = "0";
function updateDisplay() {
  document.getElementById("calcDisplay").innerText = expr;
}
function pressKey(k) {
  if (expr === "0" && !isNaN(k)) expr = k;
  else expr += k;
  updateDisplay();
}
function clearCalc() {
  expr = "0";
  updateDisplay();
}
function calcResult() {
  try {
    expr = String(eval(expr));
    console.log("Resultado calculado:", expr);
  } catch(e) {
    expr = "Error";
    console.error("Error matemático:", e.message);
  }
  updateDisplay();
}`
      },
      blank: {
        html: `<!DOCTYPE html>
<html>
<head>
  <title>Mi Nueva Web</title>
</head>
<body>
  <h1>Hola Mundo</h1>
  <p>Diseña tu página aquí.</p>
</body>
</html>`,
        css: `body {
  font-family: sans-serif;
  padding: 20px;
}`,
        js: `console.log("Página inicializada.");`
      }
    };

    this.debounceTimer = null;
    this.initDOM();
    this.bindEvents();
    this.loadTemplate('portfolio');
  }

  initDOM() {
    this.htmlEditor = document.getElementById('htmlEditor');
    this.cssEditor = document.getElementById('cssEditor');
    this.jsEditor = document.getElementById('jsEditor');
    this.previewFrame = document.getElementById('webPreviewFrame');
    this.deviceFrame = document.getElementById('previewDeviceFrame');
    this.dimensionBadge = document.getElementById('previewDimensionBadge');
    this.templateSelect = document.getElementById('webTemplateSelect');
    this.consoleLogs = document.getElementById('webConsoleLogs');
    this.btnConsoleClear = document.getElementById('webConsoleClear');
    this.resizer = document.getElementById('webResizer');
    this.editorsPane = document.getElementById('webEditorsPane');
    this.previewPane = document.getElementById('webPreviewPane');
    this.workspace = document.getElementById('webWorkspace');
  }

  loadTemplate(tplName) {
    const tpl = this.templates[tplName] || this.templates.portfolio;
    this.htmlEditor.value = tpl.html;
    this.cssEditor.value = tpl.css;
    this.jsEditor.value = tpl.js;
    this.triggerUpdate();
  }

  bindEvents() {
    // Escucha en los textareas
    [this.htmlEditor, this.cssEditor, this.jsEditor].forEach(area => {
      area.addEventListener('input', () => this.triggerUpdate());
      area.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          e.preventDefault();
          const start = area.selectionStart;
          const end = area.selectionEnd;
          area.value = area.value.substring(0, start) + "  " + area.value.substring(end);
          area.selectionStart = area.selectionEnd = start + 2;
          this.triggerUpdate();
        }
      });
    });

    // Pestañas HTML / CSS / JS / Split
    const tabBtns = document.querySelectorAll('.web-toolbar .web-btn[data-tab]');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tab = btn.dataset.tab;

        if (tab === 'split') {
          this.editorsPane.classList.add('split-mode');
        } else {
          this.editorsPane.classList.remove('split-mode');
          document.querySelectorAll('.code-box').forEach(box => box.classList.remove('active'));
          const targetBox = document.getElementById(`box-${tab}`);
          if (targetBox) targetBox.classList.add('active');
        }
      });
    });

    // Selector de dispositivos
    const deviceBtns = document.querySelectorAll('.device-btn[data-device]');
    deviceBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        deviceBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const dev = btn.dataset.device;

        this.deviceFrame.className = 'preview-browser-frame';
        if (dev === 'mobile') {
          this.deviceFrame.classList.add('device-mobile');
          this.dimensionBadge.textContent = '375 x 667 (Móvil)';
        } else if (dev === 'tablet') {
          this.deviceFrame.classList.add('device-tablet');
          this.dimensionBadge.textContent = '768 x 1024 (Tablet)';
        } else {
          this.dimensionBadge.textContent = '100% (Flexible)';
        }
      });
    });

    // Selector de plantillas
    if (this.templateSelect) {
      this.templateSelect.addEventListener('change', (e) => {
        this.loadTemplate(e.target.value);
      });
    }

    // Botón refrescar
    const btnRefresh = document.getElementById('btnRefreshPreview');
    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => this.renderPreview());
    }

    // Botón limpiar consola
    if (this.btnConsoleClear) {
      this.btnConsoleClear.addEventListener('click', () => {
        this.consoleLogs.innerHTML = '';
      });
    }

    // Redimensionador arrastrable (Touch & Mouse)
    let isDragging = false;
    const startDrag = (e) => {
      isDragging = true;
      this.resizer.classList.add('dragging');
    };
    const stopDrag = () => {
      isDragging = false;
      this.resizer.classList.remove('dragging');
    };
    const onDrag = (e) => {
      if (!isDragging) return;
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const rect = this.workspace.getBoundingClientRect();

      if (window.innerWidth > 850) {
        const offset = clientX - rect.left;
        const total = rect.width;
        const pct = Math.max(15, Math.min(85, (offset / total) * 100));
        this.editorsPane.style.flex = `0 0 ${pct}%`;
        this.previewPane.style.flex = `0 0 ${100 - pct}%`;
      } else {
        const offset = clientY - rect.top;
        const total = rect.height;
        const pct = Math.max(15, Math.min(85, (offset / total) * 100));
        this.editorsPane.style.height = `${pct}%`;
        this.previewPane.style.height = `${100 - pct}%`;
      }
    };

    this.resizer.addEventListener('mousedown', startDrag);
    this.resizer.addEventListener('touchstart', startDrag, { passive: true });
    window.addEventListener('mouseup', stopDrag);
    window.addEventListener('touchend', stopDrag);
    window.addEventListener('mousemove', onDrag);
    window.addEventListener('touchmove', onDrag, { passive: true });

    // Escuchar mensajes de console enviados desde el iframe
    window.addEventListener('message', (e) => {
      if (e.data && e.data.source === 'web-preview-console') {
        this.addConsoleLog(e.data.type, e.data.message);
      }
    });
  }

  triggerUpdate() {
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => this.renderPreview(), 300);
  }

  addConsoleLog(type, msg) {
    const logItem = document.createElement('div');
    logItem.className = `c-log ${type}`;
    logItem.textContent = `[${type.toUpperCase()}] ${msg}`;
    this.consoleLogs.appendChild(logItem);
    this.consoleLogs.scrollTop = this.consoleLogs.scrollHeight;
  }

  renderPreview() {
    const html = this.htmlEditor.value;
    const css = this.cssEditor.value;
    const js = this.jsEditor.value;

    // Script inyectado para capturar console.log / error dentro del iframe
    const interceptScript = `
      <script>
        (function() {
          const sendLog = (type, args) => {
            try {
              const msg = Array.from(args).map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
              window.parent.postMessage({ source: 'web-preview-console', type: type, message: msg }, '*');
            } catch(e) {}
          };
          const origLog = console.log;
          const origWarn = console.warn;
          const origErr = console.error;
          console.log = function() { origLog.apply(console, arguments); sendLog('log', arguments); };
          console.warn = function() { origWarn.apply(console, arguments); sendLog('warn', arguments); };
          console.error = function() { origErr.apply(console, arguments); sendLog('error', arguments); };
          window.onerror = function(msg, url, line) {
            sendLog('error', [msg + ' (línea ' + line + ')']);
          };
        })();
      <\/script>
    `;

    const fullDocument = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>${css}</style>
        ${interceptScript}
      </head>
      <body>
        ${html}
        <script>
          try {
            ${js}
          } catch(err) {
            console.error(err.message);
          }
        <\/script>
      </body>
      </html>
    `;

    this.previewFrame.srcdoc = fullDocument;
  }
}
