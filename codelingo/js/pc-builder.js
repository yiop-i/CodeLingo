/**
 * PC-BUILDER.JS - TALLER TÉCNICO INTERACTIVO DE HARDWARE (DESKTOP)
 * 1. Diagnóstico y Reconocimiento de Componentes (Ficha y Quiz)
 * 2. Validación de Ubicación (Colocar componentes en su lugar correcto)
 * 3. Cambio de Componentes Viejos por Nuevos (Upgrades de CPU, RAM, GPU, M.2 SSD)
 * 4. Limpieza y Mantenimiento (Destornillador, Aire comprimido, Brocha, Alcohol y Pasta)
 */

class DesktopPCBuilder {
  constructor() {
    this.activeTool = 'inspect'; // inspect, screwdriver, hand, blower, brush, alcohol, paste
    this.currentTab = 'tray'; // 'tray' o 'upgrades'
    
    // Estado de suciedad y mantenimiento de la PC
    this.dustCleaned = false;
    this.fansCleaned = false;
    this.pasteState = 'dry'; // 'dry' (seca), 'clean' (limpia con alcohol), 'fresh' (nueva aplicada)
    this.glassScrews = { s1: true, s2: true, s3: true, s4: true };
    this.glassPanelRemoved = false;
    this.coolerScrews = { cs1: true, cs2: true, cs3: true, cs4: true };
    this.coolerMounted = true;
    this.pcieScrewIn = true;
    this.pcieLatchLocked = true;
    this.gpuCableConnected = true;
    this.sataCableConnected = true;
    this.cleanlinessScore = 15; // 0 a 100%

    // Base de datos de componentes para reconocimiento y quiz
    this.componentsDB = {
      cpu_old: {
        id: 'cpu_old',
        name: 'Intel Core i5-7400 (4 Núcleos @ 3.0 GHz)',
        type: 'cpu',
        slotName: 'Zócalo / Socket LGA',
        slotId: 'slot-cpu',
        category: 'cpu',
        isNew: false,
        installed: true,
        icon: '🔲',
        desc: 'Unidad Central de Procesamiento (CPU). Ejecuta las instrucciones lógicas y de cálculo de los programas.',
        diag: '⚠️ Pasta térmica original cristalizada y seca. Causa sobrecalentamiento severo (92°C) y thermal throttling.',
        quiz: {
          q: '¿Dónde se monta este microprocesador en la placa base?',
          options: ['En el Socket LGA abriendo la palanca de retención', 'En la ranura PCIe x16', 'En las bahías SATA de 3.5 pulgadas'],
          correct: 0
        }
      },
      cpu_new: {
        id: 'cpu_new',
        name: 'Intel Core i9-14900K (24 Núcleos @ 6.0 GHz)',
        type: 'cpu',
        slotName: 'Zócalo / Socket LGA1700',
        slotId: 'slot-cpu',
        category: 'cpu',
        isNew: true,
        installed: false,
        icon: '⚡',
        desc: 'Procesador tope de gama con 8 núcleos de rendimiento y 16 de eficiencia. Ideal para gaming extremo y renderizado.',
        diag: '✅ Componente nuevo sellado de alta gama. Requiere pasta térmica fresca y disipador de alto rendimiento.',
        quiz: {
          q: '¿Qué se debe colocar obligatoriamente sobre el IHS del CPU antes de atornillar el disipador?',
          options: ['Pasta térmica de alta conductividad', 'Alcohol isopropílico', 'Cinta adhesiva común'],
          correct: 0
        }
      },
      cooler_old: {
        id: 'cooler_old',
        name: 'Disipador Stock de Aluminio con Ventilador',
        type: 'cooler',
        slotName: 'Soporte de Disipador de CPU',
        slotId: 'slot-cooler',
        category: 'cooler',
        isNew: false,
        installed: true,
        icon: '🌪️',
        desc: 'Disipador básico por aire con aletas de aluminio y ventilador de 90mm.',
        diag: '⚠️ Aletas de disipación totalmente atascadas de polvo. Ventilador ruidoso e insuficiente para CPUs potentes.',
        quiz: {
          q: '¿Cómo deben desatornillarse y atornillarse los 4 tornillos de un disipador de procesador?',
          options: ['En forma de cruz / diagonal para distribuir la presión uniformemente', 'Apretando uno al máximo antes de tocar los otros', 'En sentido horario únicamente'],
          correct: 0
        }
      },
      cooler_new: {
        id: 'cooler_new',
        name: 'Refrigeración Líquida AIO 360mm ARGB (Radiador Triple)',
        type: 'cooler',
        slotName: 'Soporte de Disipador de CPU',
        slotId: 'slot-cooler',
        category: 'cooler',
        isNew: true,
        installed: false,
        icon: '❄️',
        desc: 'Sistema de refrigeración líquida sellada con bomba de cobre de alta velocidad y 3 ventiladores de 120mm.',
        diag: '✅ Repuesto nuevo. Mantiene el procesador a menos de 60°C bajo máxima carga de trabajo.',
        quiz: {
          q: '¿Cuál es la función del líquido refrigerante dentro del circuito cerrado AIO?',
          options: ['Transportar el calor del bloque de cobre del CPU al radiador para ser enfriado por los ventiladores', 'Dar energía eléctrica al procesador', 'Limpiar el polvo de la placa'],
          correct: 0
        }
      },
      ram_old: {
        id: 'ram_old',
        name: 'Memoria RAM Genérica 8GB DDR4 2133MHz',
        type: 'ram',
        slotName: 'Ranuras DIMM de Memoria RAM',
        slotId: 'slot-ram',
        category: 'ram',
        isNew: false,
        installed: true,
        icon: '💾',
        desc: 'Módulo individual de memoria de acceso aleatorio. Almacena temporalmente los datos de programas en ejecución.',
        diag: '⚠️ Capacidad insuficiente (8GB) y un solo canal (Single Channel), lo que crea un cuello de botella.',
        quiz: {
          q: '¿Qué se debe abrir en la placa madre antes de poder extraer o insertar un módulo de memoria RAM?',
          options: ['Los clips o trabas de retención en los extremos de la ranura DIMM', 'El seguro de la palanca PCIe', 'El tornillo M.2'],
          correct: 0
        }
      },
      ram_new: {
        id: 'ram_new',
        name: 'Kit 32GB (2x16GB) Corsair Dominator DDR5 6000MHz RGB',
        type: 'ram',
        slotName: 'Ranuras DIMM (Canal Dual: Ranuras 2 y 4)',
        slotId: 'slot-ram',
        category: 'ram',
        isNew: true,
        installed: false,
        icon: '🚀',
        desc: 'Kit de alto rendimiento DDR5 con perfil XMP 3.0 activable en BIOS. Duplica el ancho de banda en Dual Channel.',
        diag: '✅ Repuesto nuevo de alto rendimiento. Se debe colocar en las ranuras DIMM 2 y 4 para aprovechar el Canal Dual.',
        quiz: {
          q: 'Para activar la tecnología "Dual Channel" con 2 módulos en una placa de 4 ranuras, ¿en qué ranuras deben colocarse?',
          options: ['En las ranuras 2 y 4 (o 1 y 3 según el fabricante)', 'En las ranuras 1 y 2 juntas', 'En cualquier ranura al azar'],
          correct: 0
        }
      },
      hdd_old: {
        id: 'hdd_old',
        name: 'Disco Rígido Mecánico Seagate 500GB 5400RPM SATA',
        type: 'storage',
        slotName: 'Bahía de Discos 3.5" (Conector SATA)',
        slotId: 'slot-hdd',
        category: 'storage',
        isNew: false,
        installed: true,
        icon: '💿',
        desc: 'Disco duro tradicional con platos magnéticos giratorios y cabezal mecánico.',
        diag: '⚠️ Tecnología mecánica obsoleta. Velocidad de lectura lenta (80 MB/s), sectores defectuosos y arranque de Windows en 3 minutos.',
        quiz: {
          q: '¿Qué cables deben desconectarse para retirar un disco duro SATA de 3.5 pulgadas?',
          options: ['Cable de datos SATA a la placa y cable de alimentación SATA de la fuente', 'Cable HDMI y cable de red', 'Cable de ventilador PWM'],
          correct: 0
        }
      },
      ssd_new: {
        id: 'ssd_new',
        name: 'SSD Samsung 990 PRO 2TB NVMe PCIe 4.0 M.2',
        type: 'storage',
        slotName: 'Ranura M.2 PCIe NVMe',
        slotId: 'slot-storage',
        category: 'storage',
        isNew: true,
        installed: false,
        icon: '⚡',
        desc: 'Unidad de estado sólido ultrarrápida que se conecta directamente al bus PCIe sin cables.',
        diag: '✅ Repuesto nuevo con velocidad de lectura de 7450 MB/s (100 veces más rápido que el HDD mecánico). Windows arrancará en 6 segundos.',
        quiz: {
          q: '¿Cómo se asegura una unidad de estado sólido M.2 en la placa base?',
          options: ['Se inserta en un ángulo de 30° en la ranura M.2, se baja y se asegura con su tornillo pequeño', 'Con cables gruesos de poder', 'Con pegamento térmico'],
          correct: 0
        }
      },
      gpu_old: {
        id: 'gpu_old',
        name: 'Tarjeta Gráfica NVIDIA GeForce GTX 1050 Ti 4GB',
        type: 'gpu',
        slotName: 'Ranura PCIe 5.0 / 4.0 x16',
        slotId: 'slot-gpu',
        category: 'gpu',
        isNew: false,
        installed: true,
        icon: '🎮',
        desc: 'Procesador Gráfico (GPU) dedicado para renderizado 3D y videojuegos.',
        diag: '⚠️ Pasta seca en el chip gráfico, ventilador ruidoso y falta de potencia para juegos modernos.',
        quiz: {
          q: 'Antes de jalar hacia afuera una tarjeta gráfica de la placa madre, ¿qué seguro se debe destrabar?',
          options: ['La pestaña o clip de retención al final de la ranura PCIe x16 y el tornillo del chasis', 'La palanca del CPU', 'El seguro de la fuente'],
          correct: 0
        }
      },
      gpu_new: {
        id: 'gpu_new',
        name: 'NVIDIA GeForce RTX 4080 Super 16GB GDDR6X',
        type: 'gpu',
        slotName: 'Ranura PCIe 5.0 x16',
        slotId: 'slot-gpu',
        category: 'gpu',
        isNew: true,
        installed: false,
        icon: '🔥',
        desc: 'GPU de arquitectura Ada Lovelace con Ray Tracing de 3ra generación y DLSS 3.5.',
        diag: '✅ Repuesto nuevo de ultra alto rendimiento. Requiere conector de alimentación PCIe dedicado.',
        quiz: {
          q: '¿A qué ranura de expansión de la motherboard debe conectarse la tarjeta gráfica para máximo ancho de banda?',
          options: ['A la ranura PCIe x16 principal (la más cercana al CPU)', 'A una ranura PCIe x1 corta', 'A la ranura de memoria RAM'],
          correct: 0
        }
      }
    };

    // Tareas de la orden de trabajo técnico
    this.tasks = [
      { id: 't_glass', text: 'Desatornillar los 4 tornillos y retirar el panel de cristal templado', done: false },
      { id: 't_dust', text: 'Limpiar el polvo de los ventiladores con aire comprimido y placa con brocha', done: false },
      { id: 't_disassemble_old', text: 'Desmontar componentes viejos (Cooler, GPU, HDD y RAM de 8GB)', done: false },
      { id: 't_clean_paste', text: 'Remover la pasta térmica vieja y seca del CPU con alcohol isopropílico', done: false },
      { id: 't_apply_paste', text: 'Aplicar pasta térmica fresca de alta conductividad sobre el CPU', done: false },
      { id: 't_install_upgrades', text: 'Instalar los repuestos nuevos: SSD M.2, 32GB RAM DDR5, Cooler 360mm y GPU RTX', done: false },
      { id: 't_close_test', text: 'Colocar cristal, encender la PC y verificar prueba POST a baja temperatura', done: false }
    ];

    this.initDOM();
    this.bindEvents();
    this.renderCatalog();
    this.renderTasks();
    this.updateStats();
  }

  initDOM() {
    this.catalogList = document.getElementById('pcbItemList');
    this.tasksList = document.getElementById('pcbStepsList');
    this.progressFill = document.getElementById('pcbProgressFill');
    this.cleanlinessStat = document.getElementById('pcbCleanlinessStat');
    this.tempStat = document.getElementById('pcbTempStat');
    this.powerBtn = document.getElementById('pcbPowerBtn');
    this.biosScreen = document.getElementById('biosScreen');
    this.biosContent = document.getElementById('biosContent');
    this.btnExitBios = document.getElementById('btnExitBios');
    this.dustOverlay = document.getElementById('dustOverlay');
    this.glassPanel = document.getElementById('glassSidePanel');
    this.btnGlassToggle = document.getElementById('btnGlassPanel');
    
    // Modal de Inspección
    this.inspectorModal = document.getElementById('componentInspectorModal');
    this.btnCloseInspector = document.getElementById('btnCloseInspector');
  }

  setTool(toolName) {
    this.activeTool = toolName;
    document.querySelectorAll('.pcb-tool').forEach(b => {
      b.classList.toggle('active', b.dataset.tool === toolName);
    });

    const toolNames = {
      inspect: 'Lupa de Inspección y Reconocimiento',
      screwdriver: 'Destornillador Magnético',
      hand: 'Mano (Montar/Desmontar)',
      blower: 'Lata de Aire Comprimido',
      brush: 'Brocha Antiestática',
      alcohol: 'Alcohol Isopropílico y Paño',
      paste: 'Jeringa de Pasta Térmica Nueva'
    };

    if (window.showAppToast) {
      window.showAppToast(`Herramienta activa: ${toolNames[toolName]}`, 'info');
    }
  }

  renderCatalog() {
    this.catalogList.innerHTML = '';
    const items = Object.values(this.componentsDB);
    const filtered = this.currentTab === 'tray'
      ? items.filter(i => !i.installed) // Componentes en la bandeja (desarmados o listos)
      : items.filter(i => i.isNew && !i.installed); // Repuestos nuevos para upgrade

    if (filtered.length === 0) {
      this.catalogList.innerHTML = `<div class="empty-tray-msg">${this.currentTab === 'tray' ? 'Bandeja vacía. Desmonta piezas del gabinete con la Mano.' : 'Todos los repuestos nuevos ya han sido instalados.'}</div>`;
      return;
    }

    filtered.forEach(comp => {
      const card = document.createElement('div');
      card.className = `pcb-item-card ${comp.isNew ? 'is-upgrade' : 'is-old'}`;
      card.innerHTML = `
        <div class="item-badge-row">
          <span class="item-cat-tag">${comp.icon} ${comp.slotName}</span>
          <span class="item-status-tag ${comp.isNew ? 'new-tag' : 'old-tag'}">${comp.isNew ? '★ REPUESTO NUEVO' : 'VIEJO / RETIRADO'}</span>
        </div>
        <div class="item-name">${comp.name}</div>
        <div class="item-actions-row">
          <button class="card-btn inspect-btn" title="Reconocer e Inspeccionar">🔍 Inspeccionar</button>
          <button class="card-btn install-btn" title="Instalar en su lugar correspondiente">＋ Colocar en Chasis</button>
        </div>
      `;

      card.querySelector('.inspect-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        this.openInspector(comp);
      });

      card.querySelector('.install-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        this.tryInstallComponent(comp);
      });

      this.catalogList.appendChild(card);
    });
  }

  renderTasks() {
    this.tasksList.innerHTML = '';
    let doneCount = 0;
    this.tasks.forEach((t, idx) => {
      if (t.done) doneCount++;
      const li = document.createElement('li');
      li.className = `step-item ${t.done ? 'done' : ''} ${!t.done && (idx === 0 || this.tasks[idx - 1].done) ? 'active' : ''}`;
      li.innerHTML = `
        <span class="step-num">${t.done ? '✓' : idx + 1}.</span>
        <span class="step-text">${t.text}</span>
      `;
      this.tasksList.appendChild(li);
    });

    const pct = Math.round((doneCount / this.tasks.length) * 100);
    this.progressFill.style.width = `${pct}%`;
  }

  markTask(taskId) {
    const t = this.tasks.find(x => x.id === taskId);
    if (t && !t.done) {
      t.done = true;
      this.renderTasks();
      if (window.showAppToast) {
        window.showAppToast(`¡Paso completado!: ${t.text}`, 'success');
      }
    }
  }

  updateStats() {
    this.cleanlinessStat.textContent = `${this.cleanlinessScore}% (${this.cleanlinessScore >= 80 ? 'Impecable' : this.cleanlinessScore >= 40 ? 'Regular' : 'Muy Sucio'})`;
    this.cleanlinessStat.className = `stat-val ${this.cleanlinessScore >= 80 ? 'pass' : ''}`;

    if (this.pasteState === 'fresh' && this.componentsDB.cooler_new.installed) {
      this.tempStat.textContent = '31°C (Óptima / Fría)';
      this.tempStat.className = 'stat-val cold';
    } else if (this.pasteState === 'clean' || !this.componentsDB.cooler_old.installed && !this.componentsDB.cooler_new.installed) {
      this.tempStat.textContent = 'Sin disipador (Iniciable)';
      this.tempStat.className = 'stat-val hot';
    } else {
      this.tempStat.textContent = '92°C (Sobrecalentado)';
      this.tempStat.className = 'stat-val hot';
    }
  }

  // 1. RECONOCIMIENTO E INSPECCIÓN DE COMPONENTES
  openInspector(comp) {
    document.getElementById('inspectCompTitle').textContent = `🔍 Ficha de Reconocimiento: ${comp.name}`;
    document.getElementById('inspectCompName').textContent = comp.name;
    document.getElementById('inspectIconBox').textContent = comp.icon;
    document.getElementById('inspectCompSlot').textContent = `Ubicación correcta: ${comp.slotName}`;
    document.getElementById('inspectCompStatus').textContent = comp.isNew ? 'Repuesto Nuevo (100% Salud)' : 'Componente Usado / Desgastado';
    document.getElementById('inspectCompStatus').className = `inspect-tag status ${comp.isNew ? 'new' : ''}`;
    document.getElementById('inspectCompDesc').textContent = comp.desc;
    document.getElementById('inspectCompDiag').textContent = comp.diag;

    // Configurar quiz de reconocimiento
    const qBox = document.getElementById('inspectQuizOptions');
    const qFeedback = document.getElementById('quizFeedback');
    document.getElementById('inspectQuizQuestion').textContent = comp.quiz.q;
    qBox.innerHTML = '';
    qFeedback.textContent = '';

    comp.quiz.options.forEach((optText, optIdx) => {
      const btn = document.createElement('button');
      btn.className = 'quiz-btn';
      btn.textContent = `${['A', 'B', 'C'][optIdx]}) ${optText}`;
      btn.addEventListener('click', () => {
        if (optIdx === comp.quiz.correct) {
          btn.classList.add('correct');
          qFeedback.textContent = '✅ ¡Correcto! Has reconocido la función y ubicación exacta del componente.';
          qFeedback.style.color = '#4ec9b0';
        } else {
          btn.classList.add('wrong');
          qFeedback.textContent = '❌ Incorrecto. Revisa la ubicación técnica indicada arriba.';
          qFeedback.style.color = '#f14c4c';
        }
      });
      qBox.appendChild(btn);
    });

    this.inspectorModal.style.display = 'flex';
  }

  // 2. VALIDACIÓN DE UBICACIÓN (PONER COMPONENTES EN SU LUGAR)
  tryInstallComponent(comp) {
    if (!this.glassPanelRemoved) {
      if (window.showAppToast) window.showAppToast('Debes retirar el panel de cristal templado antes de instalar componentes.', 'warning');
      return;
    }

    if (comp.type === 'storage' && comp.isNew) {
      const m2El = document.getElementById('installedM2');
      m2El.style.display = 'flex';
      comp.installed = true;
      this.markTask('t_install_upgrades');
      if (window.showAppToast) window.showAppToast('SSD Samsung 990 Pro insertado a 30° en la ranura M.2 PCIe y atornillado.', 'success');
    } else if (comp.type === 'ram' && comp.isNew) {
      const s2 = document.getElementById('stick2');
      const s4 = document.getElementById('stick4');
      s2.className = 'ram-stick installed new-ram';
      s4.className = 'ram-stick installed new-ram';
      comp.installed = true;
      this.markTask('t_install_upgrades');
      if (window.showAppToast) window.showAppToast('Kit 32GB DDR5 instalado en ranuras 2 y 4. ¡Canal Dual Activado!', 'success');
    } else if (comp.type === 'cooler' && comp.isNew) {
      if (this.pasteState !== 'fresh') {
        if (window.showAppToast) window.showAppToast('¡Error de ensamblador! Debes aplicar pasta térmica fresca sobre el procesador antes de colocar el disipador.', 'error');
        return;
      }
      const coolerEl = document.getElementById('installedCooler');
      coolerEl.className = 'installed-cooler clean-cooler new-cooler';
      coolerEl.style.display = 'flex';
      document.getElementById('coolerModelLabel').textContent = 'AIO Líquido 360mm ARGB (Limpio)';
      comp.installed = true;
      this.coolerMounted = true;
      this.markTask('t_install_upgrades');
      if (window.showAppToast) window.showAppToast('Refrigeración Líquida 360mm atornillada en cruz sobre el CPU.', 'success');
    } else if (comp.type === 'gpu' && comp.isNew) {
      const gpuEl = document.getElementById('installedGpu');
      gpuEl.className = 'installed-gpu new-gpu';
      gpuEl.style.display = 'flex';
      document.getElementById('gpuLabel').textContent = 'RTX 4080 SUPER 16GB (Nueva)';
      comp.installed = true;
      this.pcieLatchLocked = true;
      this.gpuCableConnected = true;
      document.getElementById('gpuCable').className = 'gpu-power-cable connected';
      document.getElementById('pcieLatch').className = 'pcie-retention-latch';
      this.markTask('t_install_upgrades');
      if (window.showAppToast) window.showAppToast('RTX 4080 Super trabada en ranura PCIe 5.0 x16 y cable de poder conectado.', 'success');
    }

    this.renderCatalog();
    this.updateStats();
  }

  // 3. LIMPIEZA Y MANTENIMIENTO TÉCNICO
  cleanFansWithAir() {
    if (this.activeTool !== 'blower') {
      if (window.showAppToast) window.showAppToast('Selecciona la herramienta "Lata de Aire Comprimido" para soplar los ventiladores.', 'warning');
      return;
    }
    this.fansCleaned = true;
    document.querySelectorAll('.dirty-fan').forEach(f => f.classList.add('cleaned'));
    this.cleanlinessScore += 25;
    this.updateStats();
    if (window.showAppToast) window.showAppToast('💨 ¡Aire a presión aplicado! Aspas girando y polvo expulsado de los ventiladores.', 'success');
    if (this.dustCleaned) this.markTask('t_dust');
  }

  cleanMotherboardBrush() {
    if (this.activeTool !== 'brush') {
      if (window.showAppToast) window.showAppToast('Selecciona la "Brocha Antiestática" para limpiar el polvo de la placa base.', 'warning');
      return;
    }
    this.dustCleaned = true;
    this.dustOverlay.classList.add('cleaned');
    this.cleanlinessScore += 25;
    this.updateStats();
    if (window.showAppToast) window.showAppToast('🖌️ Brocha antiestática pasada por ranuras y circuitos. Polvo despejado.', 'success');
    if (this.fansCleaned) this.markTask('t_dust');
  }

  cleanThermalPasteAlcohol() {
    if (this.activeTool !== 'alcohol') {
      if (window.showAppToast) window.showAppToast('Selecciona "Alcohol Isopropílico y Paño" para remover la pasta vieja.', 'warning');
      return;
    }
    if (this.coolerMounted) {
      if (window.showAppToast) window.showAppToast('Debes desatornillar y retirar el disipador antes de limpiar el procesador.', 'error');
      return;
    }
    const pasteSpot = document.getElementById('thermalPasteSpot');
    pasteSpot.className = 'thermal-paste-spot clean-die';
    this.pasteState = 'clean';
    this.cleanlinessScore += 25;
    this.updateStats();
    this.markTask('t_clean_paste');
    if (window.showAppToast) window.showAppToast('🧽 Pasta térmica seca disuelta con alcohol isopropílico. El IHS del procesador quedó brillante.', 'success');
  }

  applyFreshPaste() {
    if (this.activeTool !== 'paste') {
      if (window.showAppToast) window.showAppToast('Selecciona la "Jeringa de Pasta Térmica Nueva".', 'warning');
      return;
    }
    if (this.pasteState === 'dry') {
      if (window.showAppToast) window.showAppToast('¡No apliques pasta nueva sobre la pasta vieja! Límpiala primero con alcohol isopropílico.', 'error');
      return;
    }
    const pasteSpot = document.getElementById('thermalPasteSpot');
    pasteSpot.className = 'thermal-paste-spot fresh-paste';
    this.pasteState = 'fresh';
    this.cleanlinessScore += 25;
    this.updateStats();
    this.markTask('t_apply_paste');
    if (window.showAppToast) window.showAppToast('🧴 Gota de pasta térmica fresca de alta conductividad aplicada en el centro del procesador.', 'success');
  }

  bindEvents() {
    // Selección de herramientas
    document.querySelectorAll('.pcb-tool').forEach(btn => {
      btn.addEventListener('click', () => this.setTool(btn.dataset.tool));
    });

    // Pestañas del catálogo (Bandeja vs Repuestos Nuevos)
    document.querySelectorAll('.cat-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.cat-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.currentTab = btn.dataset.tab;
        this.renderCatalog();
      });
    });

    // Tornillos del cristal templado
    ['screwGlass1', 'screwGlass2', 'screwGlass3', 'screwGlass4'].forEach((id, idx) => {
      const screw = document.getElementById(id);
      if (screw) {
        screw.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.activeTool !== 'screwdriver') {
            if (window.showAppToast) window.showAppToast('Usa el Destornillador para aflojar los tornillos del panel de cristal.', 'warning');
            return;
          }
          screw.classList.add('unscrewed');
          this.glassScrews[`s${idx + 1}`] = false;
          if (Object.values(this.glassScrews).every(v => !v)) {
            this.glassPanel.classList.add('removed');
            this.glassPanelRemoved = true;
            this.btnGlassToggle.textContent = 'Cristal: Retirado';
            this.markTask('t_glass');
            if (window.showAppToast) window.showAppToast('Panel de cristal templado retirado. Acceso al interior habilitado.', 'success');
          }
        });
      }
    });

    // Botón de cristal
    if (this.btnGlassToggle) {
      this.btnGlassToggle.addEventListener('click', () => {
        if (this.glassPanelRemoved) {
          this.glassPanel.classList.remove('removed');
          this.glassPanelRemoved = false;
          this.btnGlassToggle.textContent = 'Cristal: Puesto';
          if (this.tasks.slice(0, 6).every(t => t.done)) {
            this.markTask('t_close_test');
          }
        } else {
          if (window.showAppToast) window.showAppToast('Usa el destornillador en los 4 tornillos de las esquinas para quitarlo.', 'info');
        }
      });
    }

    // Tornillos del Cooler Stock
    ['coolerScrew1', 'coolerScrew2', 'coolerScrew3', 'coolerScrew4'].forEach((id, idx) => {
      const cs = document.getElementById(id);
      if (cs) {
        cs.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.activeTool !== 'screwdriver') {
            if (window.showAppToast) window.showAppToast('Usa el Destornillador para los tornillos del disipador.', 'warning');
            return;
          }
          cs.classList.add('unscrewed');
          this.coolerScrews[`cs${idx + 1}`] = false;
          if (Object.values(this.coolerScrews).every(v => !v)) {
            if (window.showAppToast) window.showAppToast('Tornillos del disipador aflojados. Ahora puedes retirarlo con la Mano.', 'info');
          }
        });
      }
    });

    // Desmontar Cooler Stock
    const coolerEl = document.getElementById('installedCooler');
    if (coolerEl) {
      coolerEl.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.componentsDB[this.componentsDB.cooler_new.installed ? 'cooler_new' : 'cooler_old']);
          return;
        }
        if (this.activeTool === 'hand') {
          if (Object.values(this.coolerScrews).some(v => v)) {
            if (window.showAppToast) window.showAppToast('Afloja los 4 tornillos con el destornillador antes de levantar el disipador.', 'error');
            return;
          }
          coolerEl.style.display = 'none';
          this.coolerMounted = false;
          this.componentsDB.cooler_old.installed = false;
          this.renderCatalog();
          this.updateStats();
          if (window.showAppToast) window.showAppToast('Disipador retirado a la bandeja. El procesador con pasta seca queda al descubierto.', 'info');
        }
      });
    }

    // Limpieza de Pasta en el CPU / Inspección de CPU
    const cpuEl = document.getElementById('installedCpu');
    if (cpuEl) {
      cpuEl.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.componentsDB[this.componentsDB.cpu_new.installed ? 'cpu_new' : 'cpu_old']);
          return;
        }
        if (this.activeTool === 'alcohol') {
          this.cleanThermalPasteAlcohol();
        } else if (this.activeTool === 'paste') {
          this.applyFreshPaste();
        }
      });
    }

    // Ventiladores del Chasis (Limpieza de polvo con aire comprimido)
    ['fanFront1', 'fanFront2', 'fanRear'].forEach(fid => {
      const fan = document.getElementById(fid);
      if (fan) {
        fan.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.activeTool === 'blower') {
            this.cleanFansWithAir();
          } else if (this.activeTool === 'brush') {
            this.cleanMotherboardBrush();
          } else if (this.activeTool === 'inspect') {
            if (window.showAppToast) window.showAppToast('Ventilador de 120mm con cojinete hidráulico. Acumula pelusa y polvo.', 'info');
          }
        });
      }
    });

    // Desmontar Disco Mecánico HDD viejo
    const hddEl = document.getElementById('installedHdd');
    const sataCable = document.getElementById('sataCable');
    if (sataCable) {
      sataCable.addEventListener('click', (e) => {
        e.stopPropagation();
        this.sataCableConnected = false;
        sataCable.className = 'hdd-sata-cable disconnected';
        if (window.showAppToast) window.showAppToast('Cable de datos SATA desconectado del disco duro.', 'info');
      });
    }
    if (hddEl) {
      hddEl.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.componentsDB.hdd_old);
          return;
        }
        if (this.activeTool === 'hand') {
          if (this.sataCableConnected) {
            if (window.showAppToast) window.showAppToast('Desconecta primero el cable SATA rojo antes de jalar el disco.', 'error');
            return;
          }
          hddEl.style.display = 'none';
          this.componentsDB.hdd_old.installed = false;
          this.renderCatalog();
          this.markTask('t_disassemble_old');
          if (window.showAppToast) window.showAppToast('HDD mecánico viejo retirado a la bandeja de descarte.', 'info');
        }
      });
    }

    // Desmontar RAM Vieja
    const ramStick2 = document.getElementById('stick2');
    if (ramStick2) {
      ramStick2.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.componentsDB[this.componentsDB.ram_new.installed ? 'ram_new' : 'ram_old']);
          return;
        }
        if (this.activeTool === 'hand') {
          ramStick2.className = 'ram-stick';
          this.componentsDB.ram_old.installed = false;
          this.renderCatalog();
          this.markTask('t_disassemble_old');
          if (window.showAppToast) window.showAppToast('Módulo de memoria RAM de 8GB destrabado y retirado.', 'info');
        }
      });
    }

    // Desmontar GPU Vieja (Seguro PCIe y Cable)
    const gpuEl = document.getElementById('installedGpu');
    const pcieLatch = document.getElementById('pcieLatch');
    const pcieScrew = document.getElementById('pcieScrew');
    const gpuCable = document.getElementById('gpuCable');

    if (gpuCable) {
      gpuCable.addEventListener('click', (e) => {
        e.stopPropagation();
        this.gpuCableConnected = false;
        gpuCable.className = 'gpu-power-cable disconnected';
        if (window.showAppToast) window.showAppToast('Cable de alimentación PCIe de la tarjeta gráfica desconectado.', 'info');
      });
    }
    if (pcieScrew) {
      pcieScrew.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool !== 'screwdriver') {
          if (window.showAppToast) window.showAppToast('Usa el destornillador en el tornillo del soporte de la GPU.', 'warning');
          return;
        }
        this.pcieScrewIn = false;
        pcieScrew.style.display = 'none';
        if (window.showAppToast) window.showAppToast('Tornillo de la tarjeta de video desatornillado.', 'info');
      });
    }
    if (pcieLatch) {
      pcieLatch.addEventListener('click', (e) => {
        e.stopPropagation();
        this.pcieLatchLocked = false;
        pcieLatch.classList.add('unlocked');
        if (window.showAppToast) window.showAppToast('Seguro de la ranura PCIe destrabado con éxito.', 'info');
      });
    }
    if (gpuEl) {
      gpuEl.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.componentsDB[this.componentsDB.gpu_new.installed ? 'gpu_new' : 'gpu_old']);
          return;
        }
        if (this.activeTool === 'hand') {
          if (this.gpuCableConnected) {
            if (window.showAppToast) window.showAppToast('Desconecta el cable de poder de la GPU primero.', 'error');
            return;
          }
          if (this.pcieScrewIn) {
            if (window.showAppToast) window.showAppToast('Quita el tornillo del chasis que fija la tarjeta gráfica.', 'error');
            return;
          }
          if (this.pcieLatchLocked) {
            if (window.showAppToast) window.showAppToast('¡Cuidado! Destraba la palanquita del final del slot PCIe para no romper la ranura.', 'error');
            return;
          }
          gpuEl.style.display = 'none';
          this.componentsDB.gpu_old.installed = false;
          this.renderCatalog();
          this.markTask('t_disassemble_old');
          if (window.showAppToast) window.showAppToast('Tarjeta de video retirada a la bandeja.', 'info');
        }
      });
    }

    // Modal de Inspección cerrar
    if (this.btnCloseInspector) {
      this.btnCloseInspector.addEventListener('click', () => {
        this.inspectorModal.style.display = 'none';
      });
    }

    // Power On POST Test
    if (this.powerBtn) {
      this.powerBtn.addEventListener('click', () => {
        if (!this.coolerMounted) {
          alert('¡PELIGRO! No se puede encender la PC sin disipador térmico sobre el procesador.');
          return;
        }
        if (this.pasteState !== 'fresh') {
          alert('¡ALERTA TÉRMICA! La máquina se apagará por protección si la pasta térmica está seca o ausente.');
          return;
        }

        this.biosScreen.style.display = 'flex';
        this.biosContent.innerHTML = `AMERICAN MEGATRENDS BIOS v3.40 (UEFI x64)
Iniciando Power-On Self-Test (POST)...

[OK] CPU: Intel Core i9-14900K @ 6.00 GHz [Temp: 31°C - ÓPTIMA]
[OK] Refrigeración: AIO Líquido 360mm [Bomba: 2600 RPM]
[OK] Memoria RAM: Corsair DDR5 32GB (2x16GB) @ 6000MHz [Canal Dual Activo]
[OK] Almacenamiento Primario: Samsung 990 PRO 2TB NVMe PCIe 4.0 [Salud: 100%]
[OK] Tarjeta Gráfica: NVIDIA GeForce RTX 4080 SUPER 16GB [PCIe 5.0 x16]
[OK] Estado de Limpieza: 100% Despejado de polvo y pelusas.

¡Prueba POST superada sin errores!
Windows 11 arrancando en 6 segundos...`;
        document.getElementById('caseInterior').classList.add('spinning');
        this.markTask('t_close_test');
      });
    }

    if (this.btnExitBios) {
      this.btnExitBios.addEventListener('click', () => {
        this.biosScreen.style.display = 'none';
        document.getElementById('caseInterior').classList.remove('spinning');
      });
    }
  }
}
