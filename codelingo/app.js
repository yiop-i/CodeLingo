/**
 * ============================================================
 * CODELINGO - LÓGICA DE LA APLICACIÓN JAVASCRIPT
 * ============================================================
 */

// Estado global de la aplicación
let currentGroup = 'languages'; // 'languages', 'web', 'terminals', 'hardware'
let currentCourse = 'Python';
let currentAppTheme = 'light';
let activeNavTab = 'learn';
let termFiles = ['notas.txt', 'script.py', 'proyecto/'];

// Catálogo de los 4 Grupos Principales y sus Cursos Específicos
const catalog = {
  languages: [
    { id: 'Python', name: 'Python', icon: '🐍' },
    { id: 'C++', name: 'C++', icon: '⚡' },
    { id: 'C', name: 'C', icon: '⚙️' },
    { id: 'Javascript', name: 'Javascript', icon: '🟨' },
    { id: 'Java', name: 'Java', icon: '☕' }
  ],
  web: [
    { id: 'HTML', name: 'HTML', icon: '📄' },
    { id: 'CSS', name: 'CSS', icon: '🎨' },
    { id: 'Javascript Web', name: 'Javascript Web', icon: '🌐' }
  ],
  terminals: [
    { id: 'Terminal de Windows', name: 'Terminal de Windows', icon: '🪟' },
    { id: 'Terminal de Linux', name: 'Terminal de Linux', icon: '🐧' }
  ],
  hardware: [
    { id: 'Conceptos Generales', name: 'Conceptos Generales', icon: '💡' },
    { id: 'PC de Escritorio', name: 'PC de Escritorio', icon: '🖥️' },
    { id: 'Notebook', name: 'Notebook', icon: '💻' }
  ]
};

// Plantillas de código para el editor
const templates = {
  'Python': `# Python 3.12 - Ejercicio guiado\nradio = 5\nPI = 3.1416\narea = PI * (radio ** 2)\nprint("Radio:", radio)\nprint("Área calculada:", area)\n`,
  'C++': `// C++ 14\n#include <iostream>\nusing namespace std;\n\nint main() {\n    double radio = 5.0;\n    cout << "Área: " << (3.1416 * radio * radio) << endl;\n    return 0;\n}\n`,
  'C': `/* C Clang */\n#include <stdio.h>\n\nint main() {\n    printf("Área calculada: %.2f\\n", 3.1416f * 5.0f * 5.0f);\n    return 0;\n}\n`,
  'Javascript': `// JavaScript ES6\nconst radio = 5;\nconst area = Math.PI * Math.pow(radio, 2);\nconsole.log("Área del círculo:", area.toFixed(2));\n`,
  'Java': `// Java 21\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Área: " + (3.1416 * 5.0 * 5.0));\n    }\n}\n`,
  'HTML': `<!DOCTYPE html>\n<html>\n<head><title>Mi Web</title></head>\n<body>\n  <h1>¡Hola desde HTML5! 🚀</h1>\n  <p>Párrafo semántico de prueba en CodeLingo.</p>\n  <button onclick="alert('¡Funciona!')">Haz clic aquí</button>\n</body>\n</html>`,
  'CSS': `<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    body { font-family: sans-serif; text-align: center; padding: 20px; background: #e0f2fe; }\n    .caja { background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }\n  </style>\n</head>\n<body>\n  <div class="caja"><h2>Estilos con CSS3 🎨</h2><p>Diseño responsivo y sombras.</p></div>\n</body>\n</html>`,
  'Javascript Web': `<!DOCTYPE html>\n<html>\n<body>\n  <h2 id="txt">Texto original</h2>\n  <button onclick="document.getElementById('txt').innerText = '¡DOM Modificado con JS!'">Cambiar Contenido</button>\n</body>\n</html>`
};

// Biblioteca de apuntes PDF desbloqueados
const notesLibrary = [
  { course: 'Python', group: 'Lenguajes', title: 'Fundamentos de Python 3.12 y Tipos', icon: '🐍', status: 'Desbloqueado ✅', pages: '4 Páginas' },
  { course: 'C++', group: 'Lenguajes', title: 'Sintaxis de C++ y Streams de Salida', icon: '⚡', status: 'Desbloqueado ✅', pages: '5 Páginas' },
  { course: 'C', group: 'Lenguajes', title: 'Manejo de Memoria y Tipos Primitivos en C', icon: '⚙️', status: 'Desbloqueado ✅', pages: '3 Páginas' },
  { course: 'Javascript', group: 'Lenguajes', title: 'Variables, Funciones Flecha y ES6', icon: '🟨', status: 'Desbloqueado ✅', pages: '6 Páginas' },
  { course: 'Java', group: 'Lenguajes', title: 'Programación Orientada a Objetos en Java 21', icon: '☕', status: 'Desbloqueado ✅', pages: '5 Páginas' },
  { course: 'HTML', group: 'Desarrollo Web', title: 'Estructura Semántica y Etiquetas HTML5', icon: '📄', status: 'Desbloqueado ✅', pages: '4 Páginas' },
  { course: 'CSS', group: 'Desarrollo Web', title: 'Box Model, Flexbox y Sombras en CSS3', icon: '🎨', status: 'Desbloqueado ✅', pages: '5 Páginas' },
  { course: 'Javascript Web', group: 'Desarrollo Web', title: 'Manipulación del DOM y Eventos Web', icon: '🌐', status: 'Desbloqueado ✅', pages: '4 Páginas' },
  { course: 'Terminal de Windows', group: 'Terminal', title: 'Comandos PowerShell y Consola Windows', icon: '🪟', status: 'Desbloqueado ✅', pages: '3 Páginas' },
  { course: 'Terminal de Linux', group: 'Terminal', title: 'Comandos Bash, Permisos y Rutas Ubuntu', icon: '🐧', status: 'Desbloqueado ✅', pages: '4 Páginas' },
  { course: 'Hardware de Computadora', group: 'Hardware', title: 'Arquitectura: CPU, RAM, GPU y Comparativa PC vs Notebook', icon: '⚙️', status: 'Desbloqueado ✅', pages: '6 Páginas' }
];

// 1. SELECCIÓN DE UNO DE LOS 4 GRUPOS SUPERIORES
function selectGroup(groupId) {
  currentGroup = groupId;

  ['grpBtnLanguages', 'grpBtnWeb', 'grpBtnTerminals', 'grpBtnHardware'].forEach(id => {
    document.getElementById(id).className = "duo-btn btn-duo-white px-3 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 transition whitespace-nowrap";
  });
  const activeMap = {
    languages: 'grpBtnLanguages',
    web: 'grpBtnWeb',
    terminals: 'grpBtnTerminals',
    hardware: 'grpBtnHardware'
  };
  document.getElementById(activeMap[groupId]).className = "duo-btn btn-duo-green px-3 py-1.5 rounded-xl text-xs font-black flex items-center gap-1.5 transition whitespace-nowrap";

  // Re-renderizar las opciones de cursos
  renderCoursePills();
  selectCourse(catalog[groupId][0].id);
}

// 2. RENDERIZADO DINÁMICO DE CURSOS (FILA 2)
function renderCoursePills() {
  const container = document.getElementById('coursesPillsContainer');
  container.innerHTML = `
    <span class="text-xs font-black uppercase text-slate-400 dark:text-slate-500 mr-1 flex items-center gap-1">
      <span>📚</span> Cursos:
    </span>
  `;
  const courses = catalog[currentGroup];
  courses.forEach(c => {
    const btn = document.createElement('button');
    btn.id = 'pill_' + c.id.replace(/\s+/g, '_');
    btn.className = `course-pill ${c.id === currentCourse ? 'active' : ''}`;
    btn.innerHTML = `<span>${c.icon}</span> <span>${c.name}</span>`;
    btn.onclick = () => selectCourse(c.id);
    container.appendChild(btn);
  });
}

// 3. SELECCIÓN DE CURSO ESPECÍFICO
function selectCourse(courseId) {
  currentCourse = courseId;
  document.querySelectorAll('.course-pill').forEach(el => el.classList.remove('active'));
  const activePill = document.getElementById('pill_' + courseId.replace(/\s+/g, '_'));
  if (activePill) activePill.classList.add('active');

  document.getElementById('activeCourseLabel').innerText = courseId;
  document.getElementById('bannerBreadcrumb').innerText = `CURSO: ${courseId.toUpperCase()} • SECCIÓN 1`;
  document.getElementById('bannerCourseTitle').innerText = `${courseId}: Fundamentos y Práctica`;
  
  const node2Icon = document.getElementById('node2Icon');
  if (currentGroup === 'terminals') node2Icon.innerText = '📟';
  else if (currentGroup === 'hardware') node2Icon.innerText = '⚙️';
  else node2Icon.innerText = '💻';
}

// 4. CAMBIO DE SECCIÓN EN LA BARRA INFERIOR
function switchNavTab(tab) {
  activeNavTab = tab;
  ['screenLearn', 'screenPdfs', 'screenProfile'].forEach(id => document.getElementById(id).classList.add('hidden'));
  
  ['navBtnLearn', 'navBtnPdfs', 'navBtnProfile'].forEach(id => {
    document.getElementById(id).className = "flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-xs text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 border-2 border-transparent transition";
  });

  if (tab === 'learn') {
    document.getElementById('screenLearn').classList.remove('hidden');
    document.getElementById('courseSelectionBar').classList.remove('hidden');
    document.getElementById('navBtnLearn').className = "flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-xs text-[#58cc02] bg-emerald-50 dark:bg-emerald-950/40 border-2 border-[#58cc02]/30 transition";
  } else if (tab === 'pdfs') {
    document.getElementById('screenPdfs').classList.remove('hidden');
    document.getElementById('courseSelectionBar').classList.add('hidden');
    document.getElementById('navBtnPdfs').className = "flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-xs text-amber-500 bg-amber-50 dark:bg-amber-950/40 border-2 border-amber-500/30 transition";
    renderPdfsGrid();
  } else if (tab === 'profile') {
    document.getElementById('screenProfile').classList.remove('hidden');
    document.getElementById('courseSelectionBar').classList.add('hidden');
    document.getElementById('navBtnProfile').className = "flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-xs text-blue-500 bg-blue-50 dark:bg-blue-950/40 border-2 border-blue-500/30 transition";
  }
}

// 5. BIBLIOTECA DE APUNTES PDF
function renderPdfsGrid() {
  const grid = document.getElementById('pdfLibraryGrid');
  grid.innerHTML = '';
  notesLibrary.forEach(item => {
    const card = document.createElement('div');
    card.className = "bg-white dark:bg-slate-900 rounded-3xl p-5 border-2 border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between";
    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-2xl">${item.icon}</span>
          <span class="text-[10px] font-black uppercase bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded-full">${item.status}</span>
        </div>
        <span class="text-[10px] font-black uppercase text-slate-400 dark:text-slate-500 tracking-wider">${item.group} • ${item.pages}</span>
        <h4 class="font-black text-slate-800 dark:text-slate-100 text-sm mt-0.5">${item.title}</h4>
      </div>
      <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <span class="text-[11px] font-bold text-slate-400">PDF Oficial</span>
        <button onclick="downloadPdfDoc('${item.course}')" class="duo-btn btn-duo-green text-xs px-3 py-1.5 rounded-xl">
          📥 Descargar
        </button>
      </div>
    `;
    grid.appendChild(card);
  });
}

function downloadPdfDoc(courseName) {
  alert(`📥 Descargando Apuntes Oficiales de ${courseName} (Documento PDF desbloqueado).`);
}

// 6. CAMBIO DE TEMA CLARO / OSCURO
function setAppTheme(theme) {
  currentAppTheme = theme;
  const root = document.getElementById('htmlRoot');
  const btnL = document.getElementById('themeLightBtn');
  const btnD = document.getElementById('themeDarkBtn');

  if (theme === 'dark') {
    root.classList.add('dark');
    btnD.className = "flex-1 py-1.5 rounded-xl font-black text-xs bg-slate-700 text-white shadow-sm transition";
    btnL.className = "flex-1 py-1.5 rounded-xl font-black text-xs text-slate-400 hover:text-white transition";
  } else {
    root.classList.remove('dark');
    btnL.className = "flex-1 py-1.5 rounded-xl font-black text-xs bg-white text-slate-800 shadow-sm transition";
    btnD.className = "flex-1 py-1.5 rounded-xl font-black text-xs text-slate-500 hover:text-slate-800 transition";
  }
}

// 7. PERFIL DE USUARIO Y AVATARES
function setAvatar(emoji) {
  document.getElementById('profileAvatarDisplay').innerText = emoji;
  document.getElementById('headerAvatarIcon').innerText = emoji;
}

function saveProfileChanges() {
  const name = document.getElementById('inputUsername').value.trim() || 'Estudiante';
  document.getElementById('profileDisplayName').innerText = name;
  alert(`✅ Cambios guardados con éxito para ${name}.`);
}

// 8. APERTURA DE LECCIÓN AL HACER CLIC EN UN NODO DEL CAMINO
function openLessonModal(nodeId, title, desc) {
  const modal = document.getElementById('lessonModal');
  document.getElementById('lessonModalTitle').innerText = `${title} • ${currentCourse}`;
  document.getElementById('lessonModalTag').innerText = `SECCIÓN 1 • NIVEL ${nodeId}`;

  const codeEnv = document.getElementById('lessonCodeEnvironment');
  const termEnv = document.getElementById('lessonTerminalEnvironment');
  const hwEnv = document.getElementById('lessonHardwareEnvironment');
  const execBtn = document.getElementById('lessonExecuteBtn');

  codeEnv.classList.add('hidden');
  termEnv.classList.add('hidden');
  hwEnv.classList.add('hidden');

  if (currentGroup === 'terminals') {
    termEnv.classList.remove('hidden');
    execBtn.innerText = "▶ ENVIAR COMANDO";
    const isWin = currentCourse === 'Terminal de Windows';
    document.getElementById('lessonTermHeader').innerText = isWin ? "Windows PowerShell 7.4" : "student@antigravity: ~ (bash 5.2)";
    document.getElementById('lessonTermPrompt').innerText = isWin ? "PS C:\\Users\\Student>" : "student@antigravity:~$";
  } else if (currentGroup === 'hardware') {
    hwEnv.classList.remove('hidden');
    execBtn.innerText = "✓ COMPLETAR RETO";
  } else {
    codeEnv.classList.remove('hidden');
    execBtn.innerText = "▶ EJECUTAR CÓDIGO";
    document.getElementById('lessonCodeInput').value = templates[currentCourse] || `# Código para ${currentCourse}\nprint("Hola Mundo")`;
    document.getElementById('lessonCodeFilename').innerText = `● main_${currentCourse.toLowerCase().replace(/\s+/g,'_')}`;
    
    const isWeb = currentGroup === 'web';
    document.getElementById('lessonWebPreviewBox').classList.toggle('hidden', !isWeb);
    if (isWeb) updateLessonWebPreview();
  }

  modal.classList.remove('hidden');
}

function closeLessonModal() {
  document.getElementById('lessonModal').classList.add('hidden');
}

function executeLessonSolution() {
  if (currentGroup === 'terminals') {
    alert("🎯 ¡Comando ejecutado con éxito! Tarea de consola completada.");
  } else if (currentGroup === 'hardware') {
    alert("🎯 ¡Has identificado correctamente la función del componente!");
  } else {
    const consoleEl = document.getElementById('lessonConsoleOut');
    consoleEl.innerText = `> Compilando y ejecutando [${currentCourse}]...\nRadio: 5\nÁrea calculada: 78.54\n[Proceso terminado exitosamente con código 0]`;
    if (currentGroup === 'web') updateLessonWebPreview();
  }
  setTimeout(() => {
    closeLessonModal();
    alert("🎉 ¡Lección completada! Has ganado +20 XP ⚡.");
  }, 700);
}

function updateLessonWebPreview() {
  const code = document.getElementById('lessonCodeInput').value;
  document.getElementById('lessonWebIframe').srcdoc = code;
}

function resetLessonTemplate() {
  document.getElementById('lessonCodeInput').value = templates[currentCourse] || '';
}

function insertCodeChar(ch) {
  const txt = document.getElementById('lessonCodeInput');
  const start = txt.selectionStart;
  const end = txt.selectionEnd;
  txt.value = txt.value.substring(0, start) + ch + txt.value.substring(end);
  txt.selectionStart = txt.selectionEnd = start + ch.length;
  txt.focus();
}

function requestLessonHint() {
  const card = document.getElementById('lessonHintCard');
  card.classList.remove('hidden');
  document.getElementById('lessonHintContent').innerText = `Pista para ${currentCourse}: Verifica la sintaxis de variables y recuerda no dejar llaves o paréntesis sin cerrar.`;
}

function evaluateLessonScore() {
  alert(`🤖 Evaluación de Byte (IA):\n\nPuntaje: 96/100 ⭐\n\n✓ Excelente estructuración de variables y nombres descriptivos.\n⚠ Recuerda agregar comentarios explicativos para documentar tu solución.`);
}

function handleLessonTermKey(e) {
  if (e.key === 'Enter') {
    const val = e.target.value.trim();
    if (val) {
      const log = document.getElementById('lessonTermLog');
      const prompt = document.getElementById('lessonTermPrompt').innerText;
      const line = document.createElement('div');
      line.className = "text-white font-bold";
      line.innerText = `${prompt} ${val}`;
      log.appendChild(line);

      const res = document.createElement('div');
      res.className = "text-slate-300";
      if (val === 'ls' || val === 'dir') res.innerText = termFiles.join('   ');
      else if (val.startsWith('mkdir')) res.innerText = `Directorio creado.`;
      else res.innerText = `Comando ejecutado.`;
      log.appendChild(res);

      e.target.value = '';
      log.scrollTop = log.scrollHeight;
    }
  }
}

function openBossEvaluation() {
  alert(`🏆 Evaluación de Sección: ${currentCourse}\n\nExamen obligatorio para desbloquear la siguiente sección. Necesitas un puntaje de al menos 80/100.`);
}

function claimRewardChest() {
  alert("🎁 ¡Abriste el cofre! Ganaste +15 Gemas 💎 y +20 Puntos XP ⚡.");
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
  selectGroup('languages');
  renderPdfsGrid();
});
