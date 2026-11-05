/**
 * NOTEBOOK-BUILDER.JS - SIMULADOR VIRTUAL DE LAPTOP (CISCO IT ESSENTIALS)
 * Taller Técnico Completo de Laptop:
 * 1. Reconocimiento de Componentes Móviles (Batería, Turbina, Heatpipe, SO-DIMM, Caddy, ZIF)
 * 2. Desensamble y Montaje en el lugar correcto (Clips a 45°, tornillos en cruz, seguros Lock/Release)
 * 3. Cambio de Componentes Viejos por Nuevos (Batería nueva, SSD 1TB, 16GB RAM)
 * 4. Limpieza y Mantenimiento (Extracción de pelusa en turbina, alcohol isopropílico en die, pasta fresca)
 */

class NotebookBuilder {
  constructor() {
    this.currentStage = 'battery'; // battery, optical, cover, cooling, ram, storage, keyboard
    this.currentMode = 'learn'; // learn, test
    this.activeTool = 'inspect'; // inspect, screwdriver, hand, blower, brush, alcohol, paste

    // Estados de hardware de la laptop
    this.batteryInstalled = 'old'; // 'old', 'none', 'new'
    this.batteryLockUnlocked = false;
    this.batteryReleasePulled = false;
    this.opticalScrewOut = false;
    this.opticalDriveRemoved = false;
    this.coverScrews = { cs1: true, cs2: true, cs3: true, cs4: true };
    this.coverRemoved = false;
    this.fanClogCleaned = false;
    this.heatpipeScrews = { hs1: true, hs2: true };
    this.heatpipeRemoved = false;
    this.diePasteState = 'dry'; // 'dry', 'clean', 'fresh'
    this.ramInstalled = 'old'; // 'old' (4GB), 'none', 'new' (16GB)
    this.ramEjected45 = false;
    this.hddInstalled = 'old'; // 'old' (500GB HDD), 'none', 'new' (1TB SSD)
    this.caddyScrewsOut = false;
    this.caddyDisconnected = false;
    this.keyboardLifted = false;
    this.zifFlapOpen = false;
    this.keyboardRemoved = false;

    // Base de datos de componentes de laptop para reconocimiento
    this.laptopDB = {
      battery_old: {
        id: 'battery_old',
        name: 'Batería Li-Ion 6 Celdas 11.1V 4400mAh (Degradada / Hinchada)',
        slotName: 'Bahía Externa de Batería (Pestillos Lock y Release)',
        icon: '🔋',
        isNew: false,
        desc: 'Batería recargable de iones de litio. Proporciona alimentación autónoma a la placa y circuitos.',
        diag: '⚠️ Celdas químicas degradadas con hinchamiento físico. Retención de carga al 15% (dura menos de 10 minutos). Riesgo de sobrepresión.',
        quiz: {
          q: '¿Por qué se debe retirar la batería antes de manipular cualquier componente interno de una laptop?',
          options: ['Para evitar cortocircuitos accidentales en la placa base', 'Para que la laptop pese menos', 'Para calibrar el teclado'],
          correct: 0
        }
      },
      battery_new: {
        id: 'battery_new',
        name: 'Batería Original Nueva 6 Celdas 5200mAh Li-Ion',
        slotName: 'Bahía Externa de Batería',
        icon: '⚡🔋',
        isNew: true,
        desc: 'Batería de reemplazo grado A con microcontrolador de carga inteligente y protección térmica.',
        diag: '✅ Repuesto nuevo al 100% de salud. Proporcionará entre 5 y 7 horas continuas de autonomía.',
        quiz: {
          q: 'Una vez insertada la batería nueva en la bahía, ¿qué se debe hacer para fijarla firmemente?',
          options: ['Deslizar el Seguro 1 (Lock) hacia la posición de bloqueo', 'Dejarla suelta', 'Pegarla con cinta'],
          correct: 0
        }
      },
      cooling_fan: {
        id: 'cooling_fan',
        name: 'Ventilador Centrífugo Tipo Turbina 5V DC',
        slotName: 'Bahía de Disipación Lateral / Rejilla de Escape',
        icon: '🌀',
        isNew: false,
        desc: 'Ventilador con aspas curvadas que toma aire del chasis y lo expulsa lateralmente a través de las aletas del radiador de cobre.',
        diag: '⚠️ Atasco severo por "colchón de pelusa" y polvo acumulado en la rejilla. El aire caliente no puede salir, causando recalentamiento a 89°C.',
        quiz: {
          q: '¿Qué herramienta es ideal para limpiar el colchón de pelusa y polvo en las aletas de la turbina?',
          options: ['Brocha antiestática y lata de aire comprimido a presión', 'Agua corriente de la canilla', 'Aceite de cocina'],
          correct: 0
        }
      },
      heatpipe: {
        id: 'heatpipe',
        name: 'Conducto Térmico de Cobre Sellado (Heatpipe) con Placa Base',
        slotName: 'Socket Térmico de CPU / GPU Móvil',
        icon: '🔥➡️❄️',
        isNew: false,
        desc: 'Tubo de cobre sellado al vacío con fluido térmico en fase vapor que transfiere el calor del procesador hacia el radiador exterior.',
        diag: '⚠️ Pasta térmica seca y quebradiza en la zona de contacto. Requiere limpieza con alcohol isopropílico y reaplicación de compuesto térmico.',
        quiz: {
          q: '¿Cómo funciona un Heatpipe de cobre en una notebook?',
          options: ['El calor evapora el líquido interno, el vapor viaja al extremo frío, se condensa y retorna por capilaridad', 'Con cables eléctricos que congelan el procesador', 'Es simplemente una barra sólida de hierro'],
          correct: 0
        }
      },
      sodimm_old: {
        id: 'sodimm_old',
        name: 'Memoria RAM SO-DIMM 4GB DDR4 2133MHz',
        slotName: 'Ranuras SO-DIMM (Inserción en ángulo de 45°)',
        icon: '💾',
        isNew: false,
        desc: 'Módulo de memoria de factor de forma pequeño (Small Outline DIMM) diseñado específicamente para portátiles.',
        diag: '⚠️ Capacidad insuficiente para multitarea (4GB causa paginación constante en el disco y lentitud extrema).',
        quiz: {
          q: '¿A qué ángulo se debe insertar o extraer un módulo de memoria RAM SO-DIMM en su ranura?',
          options: ['A un ángulo aproximado de 30° a 45° antes de presionar hacia abajo', 'Totalmente perpendicular a 90°', 'Plano a 0° forzándolo horizontalmente'],
          correct: 0
        }
      },
      sodimm_new: {
        id: 'sodimm_new',
        name: 'Memoria RAM SO-DIMM 16GB DDR4 3200MHz Kingston Fury Impact',
        slotName: 'Ranuras SO-DIMM',
        icon: '🚀',
        isNew: true,
        desc: 'Módulo de alta velocidad y 16GB de capacidad con latencia reducida CL16.',
        diag: '✅ Repuesto nuevo de alta velocidad. Cuadruplica la memoria de la laptop y elimina todo retardo en Windows.',
        quiz: {
          q: '¿Cómo se confirma que un módulo SO-DIMM quedó correctamente bloqueado en la ranura?',
          options: ['Los dos clips metálicos laterales hacen un sonido de "clic" y encajan en las muescas del módulo', 'Se le pone un tornillo encima', 'Se presiona hasta que se doble'],
          correct: 0
        }
      },
      hdd_old: {
        id: 'hdd_old',
        name: 'Disco Rígido Mecánico 2.5" SATA III 500GB 5400 RPM',
        slotName: 'Bahía de Almacenamiento 2.5" con Caddy Protector',
        icon: '💿',
        isNew: false,
        desc: 'Disco magnético giratorio de 2.5 pulgadas montado dentro de una canasta o caddy metálico con tirador.',
        diag: '⚠️ Muy lento (lectura 60 MB/s), sonido metálico de cabezal y arranque de Windows que demora 4 minutos.',
        quiz: {
          q: '¿Para qué sirve el Caddy metálico o plástico que envuelve al disco en una laptop?',
          options: ['Para absorber vibraciones, aislar eléctricamente y asegurar la conexión al puerto SATA', 'Para decorar el interior', 'Para enfriar con agua'],
          correct: 0
        }
      },
      ssd_new: {
        id: 'ssd_new',
        name: 'SSD 2.5" SATA III Crucial MX500 1TB (560 MB/s)',
        slotName: 'Bahía de Almacenamiento 2.5" con Caddy',
        icon: '⚡',
        isNew: true,
        desc: 'Unidad de estado sólido con memoria NAND 3D, sin partes mecánicas móviles y resistente a golpes.',
        diag: '✅ Repuesto nuevo de 1TB. Velocidad de lectura 10 veces mayor, consumo mínimo de batería y arranque en 8 segundos.',
        quiz: {
          q: 'Al reemplazar un disco en su caddy, ¿qué paso es fundamental antes de deslizarlo al conector SATA?',
          options: ['Atornillar los tornillos laterales que fijan el SSD dentro del caddy metálico', 'Formatear la pantalla', 'Quitar la tarjeta madre'],
          correct: 0
        }
      }
    };

    // Checklist de Cisco por etapa
    this.stagesData = {
      battery: {
        title: 'Etapa 1: Batería Externa',
        instruction: 'Paso 1: Destraba el Seguro 1 (Lock) y desliza el Seguro 2 (Release) para expulsar la batería vieja degradada.',
        tasks: [
          { id: 'bat_latch1', text: 'Desbloquear Seguro 1 de la batería (Lock)', done: false },
          { id: 'bat_latch2', text: 'Deslizar Seguro 2 de expulsión (Release)', done: false },
          { id: 'bat_remove', text: 'Extraer batería vieja hinchada a la bandeja', done: false },
          { id: 'bat_new', text: 'Instalar batería nueva original y asegurar Lock', done: false }
        ]
      },
      optical: {
        title: 'Etapa 2: Unidad Óptica / DVD',
        instruction: 'Usa el destornillador para aflojar el tornillo retenedor y tira de la pestaña para retirar la unidad óptica.',
        tasks: [
          { id: 'opt_screw', text: 'Aflojar tornillo de seguridad de la bahía óptica', done: false },
          { id: 'opt_remove', text: 'Extraer unidad DVD-RW UltraSlim', done: false }
        ]
      },
      cover: {
        title: 'Etapa 3: Tapa Inferior Principal',
        instruction: 'Usa el destornillador magnético para retirar los 4 tornillos de la cubierta y levántala con la mano.',
        tasks: [
          { id: 'cover_screws', text: 'Desatornillar los 4 tornillos de la tapa inferior', done: false },
          { id: 'cover_remove', text: 'Retirar la tapa plástica inferior de acceso', done: false }
        ]
      },
      cooling: {
        title: 'Etapa 4: Refrigeración (Turbina & Heatpipe)',
        instruction: 'Limpia el colchón de pelusa de la turbina con aire y brocha. Luego quita la pasta seca del chip con alcohol isopropílico.',
        tasks: [
          { id: 'cl_fan', text: 'Expulsar el colchón de pelusa de la turbina con aire comprimido', done: false },
          { id: 'cl_pipe_screw', text: 'Desatornillar los tornillos del disipador de cobre (Heatpipe)', done: false },
          { id: 'cl_paste_clean', text: 'Remover la pasta seca del procesador con alcohol isopropílico', done: false },
          { id: 'cl_paste_fresh', text: 'Aplicar gota de pasta térmica fresca de alta conductividad', done: false }
        ]
      },
      ram: {
        title: 'Etapa 5: Memoria RAM SO-DIMM (Ángulo 45°)',
        instruction: 'Abre los clips de resorte: el módulo viejo de 4GB saltará a 45°. Luego inserta el nuevo de 16GB a 45° hasta trabar.',
        tasks: [
          { id: 'ram_clips', text: 'Abrir clips de resorte (el módulo viejo salta a 45°)', done: false },
          { id: 'ram_remove_old', text: 'Retirar módulo de memoria de 4GB obsoleto', done: false },
          { id: 'ram_install_new', text: 'Insertar nuevo módulo de 16GB a 45° y presionar hasta escuchar el clic', done: false }
        ]
      },
      storage: {
        title: 'Etapa 6: Disco & Caddy (Upgrade a SSD)',
        instruction: 'Tira de la lengüeta SATA, retira el caddy, desatornilla el HDD viejo de 500GB y monta el nuevo SSD SATA de 1TB.',
        tasks: [
          { id: 'hdd_pull', text: 'Tirar de la lengüeta plástica para desacoplar el puerto SATA', done: false },
          { id: 'hdd_caddy_screws', text: 'Desatornillar tornillos laterales del caddy metálico', done: false },
          { id: 'hdd_upgrade', text: 'Montar el nuevo SSD de 1TB en el caddy y acoplar al conector SATA', done: false }
        ]
      },
      keyboard: {
        title: 'Etapa 7: Teclado & Flex ZIF',
        instruction: 'Levanta el borde del teclado y destraba la pestaña del conector ZIF antes de desconectar el cable flex.',
        tasks: [
          { id: 'kb_lift', text: 'Levantar el marco superior del teclado', done: false },
          { id: 'zif_unlock', text: 'Levantar la pestaña de bloqueo del conector ZIF', done: false },
          { id: 'kb_cable', text: 'Desconectar cable plano de datos Ribbon Flex sin dañarlo', done: false }
        ]
      }
    };

    this.initDOM();
    this.bindEvents();
    this.setStage('battery');
    this.renderTray();
  }

  initDOM() {
    this.instructionEl = document.getElementById('ciscoInstructionText');
    this.checklistEl = document.getElementById('ciscoChecklist');
    this.partsTray = document.getElementById('ciscoTraySlots');
    this.btnNext = document.getElementById('ciscoNextStep');
    this.btnReset = document.getElementById('ciscoResetStep');
  }

  setTool(tool) {
    this.activeTool = tool;
    document.querySelectorAll('.cisco-tool-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tool === tool);
    });

    const names = {
      inspect: 'Lupa de Reconocimiento y Diagnóstico',
      screwdriver: 'Destornillador Phillips',
      hand: 'Mano (Manipular / Montar)',
      blower: 'Lata de Aire Comprimido',
      brush: 'Brocha Antiestática',
      alcohol: 'Alcohol Isopropílico y Paño',
      paste: 'Jeringa de Pasta Térmica Nueva'
    };

    if (window.showAppToast) {
      window.showAppToast(`Herramienta de Laptop: ${names[tool]}`, 'info');
    }
  }

  setStage(stageKey) {
    this.currentStage = stageKey;
    const stage = this.stagesData[stageKey];

    document.querySelectorAll('.stage-step-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.stage === stageKey);
    });

    document.querySelectorAll('.cisco-layer').forEach(l => l.style.display = 'none');
    const layer = document.getElementById(`layer-${stageKey}`);
    if (layer) layer.style.display = 'flex';

    if (this.currentMode === 'learn') {
      this.instructionEl.textContent = stage.instruction;
    } else {
      this.instructionEl.textContent = `[Modo Examen Técnico]: Ejecuta el procedimiento correcto para ${stage.title} sin ayudas.`;
    }

    this.renderChecklist();
  }

  renderChecklist() {
    const stage = this.stagesData[this.currentStage];
    this.checklistEl.innerHTML = '';
    stage.tasks.forEach(t => {
      const li = document.createElement('li');
      li.className = `cisco-check-item ${t.done ? 'done' : ''}`;
      li.innerHTML = `<span class="chk-box">${t.done ? '☑' : '☐'}</span> <span>${t.text}</span>`;
      this.checklistEl.appendChild(li);
    });

    const navBtn = document.querySelector(`.stage-step-btn[data-stage="${this.currentStage}"]`);
    if (navBtn) {
      navBtn.classList.toggle('completed', stage.tasks.every(t => t.done));
    }
  }

  markTask(taskId) {
    const stage = this.stagesData[this.currentStage];
    const task = stage.tasks.find(t => t.id === taskId);
    if (task && !task.done) {
      task.done = true;
      this.renderChecklist();
      if (window.showAppToast) {
        window.showAppToast(`Paso de laptop completado: ${task.text}`, 'success');
      }
    }
  }

  renderTray() {
    this.partsTray.innerHTML = '';
    const parts = [
      { id: 'p_bat_new', name: 'Batería Original Nueva 5200mAh', icon: '🔋', type: 'battery', compId: 'battery_new' },
      { id: 'p_sodimm_new', name: 'SO-DIMM 16GB DDR4 3200MHz', icon: '💾', type: 'ram', compId: 'sodimm_new' },
      { id: 'p_ssd_new', name: 'SSD 2.5" Crucial 1TB SATA', icon: '⚡', type: 'storage', compId: 'ssd_new' }
    ];

    parts.forEach(p => {
      const el = document.createElement('div');
      el.className = 'tray-item new-part';
      el.innerHTML = `${p.icon} <span>${p.name}</span>`;
      el.title = 'Click para inspeccionar o instalar este repuesto nuevo';
      
      el.addEventListener('click', () => {
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB[p.compId]);
        } else {
          this.installUpgradePart(p);
        }
      });
      this.partsTray.appendChild(el);
    });
  }

  openInspector(comp) {
    const modal = document.getElementById('componentInspectorModal');
    if (!modal) return;

    document.getElementById('inspectCompTitle').textContent = `🔍 Ficha Laptop: ${comp.name}`;
    document.getElementById('inspectCompName').textContent = comp.name;
    document.getElementById('inspectIconBox').textContent = comp.icon;
    document.getElementById('inspectCompSlot').textContent = `Conexión: ${comp.slotName}`;
    document.getElementById('inspectCompStatus').textContent = comp.isNew ? 'Repuesto Nuevo Certificado' : 'Componente con Desgaste / Suciedad';
    document.getElementById('inspectCompDesc').textContent = comp.desc;
    document.getElementById('inspectCompDiag').textContent = comp.diag;

    const qBox = document.getElementById('inspectQuizOptions');
    const qFeed = document.getElementById('quizFeedback');
    document.getElementById('inspectQuizQuestion').textContent = comp.quiz.q;
    qBox.innerHTML = '';
    qFeed.textContent = '';

    comp.quiz.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.className = 'quiz-btn';
      btn.textContent = `${['A', 'B', 'C'][idx]}) ${opt}`;
      btn.addEventListener('click', () => {
        if (idx === comp.quiz.correct) {
          btn.classList.add('correct');
          qFeed.textContent = '✅ ¡Correcto! Procedimiento técnico validado.';
          qFeed.style.color = '#4ec9b0';
        } else {
          btn.classList.add('wrong');
          qFeed.textContent = '❌ Incorrecto. Revisa el protocolo de servicio de laptop.';
          qFeed.style.color = '#f14c4c';
        }
      });
      qBox.appendChild(btn);
    });

    modal.style.display = 'flex';
  }

  installUpgradePart(part) {
    if (part.type === 'battery' && this.currentStage === 'battery') {
      if (this.batteryInstalled !== 'none') {
        if (window.showAppToast) window.showAppToast('Debes extraer primero la batería vieja antes de colocar la nueva.', 'error');
        return;
      }
      const batEl = document.getElementById('ciscoBattery');
      batEl.classList.remove('removed', 'old-battery');
      batEl.classList.add('new-battery');
      document.getElementById('ciscoBatteryLabel').textContent = 'BATERÍA LI-ION NUEVA (100% SALUD - 5200mAh)';
      this.batteryInstalled = 'new';
      this.markTask('bat_new');
      if (window.showAppToast) window.showAppToast('Batería nueva original instalada. Recuerda trabar el Seguro 1 (Lock).', 'success');
    } else if (part.type === 'ram' && this.currentStage === 'ram') {
      if (this.ramInstalled !== 'none') {
        if (window.showAppToast) window.showAppToast('Retira primero el módulo de 4GB antes de insertar el de 16GB.', 'error');
        return;
      }
      const so1 = document.getElementById('soDimm1');
      so1.style.display = 'flex';
      so1.className = 'cisco-component so-dimm-module new-sodimm'; // bloqueado horizontal
      document.getElementById('soDimmLabel1').textContent = '16GB DDR4 3200MHz Kingston Fury (Nuevo)';
      this.ramInstalled = 'new';
      this.markTask('ram_install_new');
      if (window.showAppToast) window.showAppToast('Módulo de 16GB insertado a 45° y presionado hacia abajo. ¡Clips trabados!', 'success');
    } else if (part.type === 'storage' && this.currentStage === 'storage') {
      if (this.hddInstalled !== 'none') {
        if (window.showAppToast) window.showAppToast('Retira primero el disco viejo del caddy.', 'error');
        return;
      }
      const hddEl = document.getElementById('ciscoHdd');
      hddEl.style.display = 'flex';
      hddEl.className = 'cisco-component hdd-caddy new-ssd';
      document.getElementById('ciscoHddLabel').textContent = 'SSD 2.5" CRUCIAL 1TB SATA III (NUEVO - 560 MB/s)';
      this.hddInstalled = 'new';
      this.markTask('hdd_upgrade');
      if (window.showAppToast) window.showAppToast('SSD nuevo de 1TB atornillado en el caddy y acoplado firmemente al puerto SATA.', 'success');
    } else {
      if (window.showAppToast) window.showAppToast(`Debes estar en la etapa correspondiente (${part.type}) para montar esta pieza.`, 'warning');
    }
  }

  bindEvents() {
    // Cambio de etapas
    document.querySelectorAll('.stage-step-btn').forEach(b => {
      b.addEventListener('click', () => this.setStage(b.dataset.stage));
    });

    // Herramientas
    document.querySelectorAll('.cisco-tool-btn').forEach(btn => {
      btn.addEventListener('click', () => this.setTool(btn.dataset.tool));
    });

    // ETAPA 1: BATERÍA
    const latch1 = document.getElementById('latch1');
    const latch2 = document.getElementById('latch2');
    const battery = document.getElementById('ciscoBattery');

    if (latch1) {
      latch1.addEventListener('click', () => {
        this.batteryLockUnlocked = !this.batteryLockUnlocked;
        latch1.classList.toggle('unlocked', this.batteryLockUnlocked);
        latch1.querySelector('.latch-indicator').textContent = this.batteryLockUnlocked ? '🔓' : '🔒';
        if (this.batteryLockUnlocked) this.markTask('bat_latch1');
      });
    }

    if (latch2) {
      latch2.addEventListener('click', () => {
        if (!this.batteryLockUnlocked) {
          if (window.showAppToast) window.showAppToast('Debes desbloquear el Seguro 1 antes de deslizar el expulsor 2.', 'warning');
          return;
        }
        this.batteryReleasePulled = true;
        latch2.classList.add('unlocked');
        this.markTask('bat_latch2');
      });
    }

    if (battery) {
      battery.addEventListener('click', () => {
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB[this.batteryInstalled === 'new' ? 'battery_new' : 'battery_old']);
          return;
        }
        if (!this.batteryLockUnlocked || !this.batteryReleasePulled) {
          if (window.showAppToast) window.showAppToast('¡Atención! La batería sigue retenida mecánicamente por los pestillos.', 'error');
          return;
        }
        battery.classList.add('removed');
        this.batteryInstalled = 'none';
        this.markTask('bat_remove');
        if (window.showAppToast) window.showAppToast('Batería vieja hinchada retirada a la bandeja. Selecciona la batería nueva de la bandeja para colocarla.', 'info');
      });
    }

    // ETAPA 2: UNIDAD ÓPTICA
    const optScrew = document.getElementById('opticalScrew');
    const optDrive = document.getElementById('ciscoOptical');

    if (optScrew) {
      optScrew.addEventListener('click', () => {
        if (this.activeTool !== 'screwdriver') {
          if (window.showAppToast) window.showAppToast('Selecciona el Destornillador Phillips.', 'warning');
          return;
        }
        optScrew.style.display = 'none';
        this.opticalScrewOut = true;
        this.markTask('opt_screw');
        if (window.showAppToast) window.showAppToast('Tornillo de fijación de la unidad óptica desatornillado.', 'info');
      });
    }

    if (optDrive) {
      optDrive.addEventListener('click', () => {
        if (!this.opticalScrewOut) {
          if (window.showAppToast) window.showAppToast('La unidad óptica está atornillada al chasis.', 'error');
          return;
        }
        optDrive.style.transform = 'translateX(-120px)';
        optDrive.style.opacity = '0.2';
        this.opticalDriveRemoved = true;
        this.markTask('opt_remove');
        if (window.showAppToast) window.showAppToast('Unidad DVD-RW extraída de la bahía lateral.', 'info');
      });
    }

    // ETAPA 3: TAPA INFERIOR PRINCIPAL
    ['cs1', 'cs2', 'cs3', 'cs4'].forEach((cid, idx) => {
      const screw = document.getElementById(cid);
      if (screw) {
        screw.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.activeTool !== 'screwdriver') {
            if (window.showAppToast) window.showAppToast('Usa el Destornillador Phillips para los tornillos de la carcasa.', 'warning');
            return;
          }
          screw.classList.add('unscrewed');
          this.coverScrews[`cs${idx + 1}`] = false;
          if (Object.values(this.coverScrews).every(v => !v)) {
            this.markTask('cover_screws');
            if (window.showAppToast) window.showAppToast('Los 4 tornillos fueron retirados. Haz clic en la tapa con la Mano para abrirla.', 'info');
          }
        });
      }
    });

    const coverEl = document.getElementById('laptopFullCover');
    if (coverEl) {
      coverEl.addEventListener('click', () => {
        if (Object.values(this.coverScrews).some(v => v)) {
          if (window.showAppToast) window.showAppToast('Debes desatornillar los 4 tornillos de las esquinas antes de levantar la tapa.', 'error');
          return;
        }
        coverEl.classList.add('opened');
        this.coverRemoved = true;
        this.markTask('cover_remove');
        if (window.showAppToast) window.showAppToast('Tapa inferior retirada. Placa base y circuito de refrigeración al descubierto.', 'success');
      });
    }

    // ETAPA 4: REFRIGERACIÓN (TURBINA & HEATPIPE)
    const blowerFan = document.getElementById('laptopBlower');
    if (blowerFan) {
      blowerFan.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB.cooling_fan);
          return;
        }
        if (this.activeTool === 'blower' || this.activeTool === 'brush') {
          blowerFan.classList.add('cleaned');
          this.fanClogCleaned = true;
          this.markTask('cl_fan');
          if (window.showAppToast) window.showAppToast('💨 ¡Colchón de pelusa y polvo removido! Las aletas de la turbina giran libremente.', 'success');
        } else {
          if (window.showAppToast) window.showAppToast('Usa el Aire Comprimido o la Brocha para limpiar la pelusa atascada en la turbina.', 'warning');
        }
      });
    }

    ['hs1', 'hs2'].forEach((hid, idx) => {
      const hs = document.getElementById(hid);
      if (hs) {
        hs.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.activeTool !== 'screwdriver') {
            if (window.showAppToast) window.showAppToast('Usa el destornillador en los tornillos numerados del heatpipe.', 'warning');
            return;
          }
          hs.style.opacity = '0.2';
          this.heatpipeScrews[`hs${idx + 1}`] = false;
          if (Object.values(this.heatpipeScrews).every(v => !v)) {
            this.heatpipeRemoved = true;
            this.markTask('cl_pipe_screw');
            if (window.showAppToast) window.showAppToast('Tubo de cobre (Heatpipe) desatornillado. El chip del CPU con pasta seca queda visible.', 'info');
          }
        });
      }
    });

    const dieChip = document.getElementById('laptopDieChip');
    if (dieChip) {
      dieChip.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB.heatpipe);
          return;
        }
        if (this.activeTool === 'alcohol') {
          document.getElementById('laptopPasteSpot').className = 'thermal-paste-spot clean-die';
          this.diePasteState = 'clean';
          this.markTask('cl_paste_clean');
          if (window.showAppToast) window.showAppToast('🧽 Pasta térmica vieja disuelta con alcohol isopropílico. Núcleo de silicio limpio.', 'success');
        } else if (this.activeTool === 'paste') {
          if (this.diePasteState === 'dry') {
            if (window.showAppToast) window.showAppToast('¡Limpia la pasta vieja con alcohol primero!', 'error');
            return;
          }
          document.getElementById('laptopPasteSpot').className = 'thermal-paste-spot fresh-paste';
          this.diePasteState = 'fresh';
          this.markTask('cl_paste_fresh');
          if (window.showAppToast) window.showAppToast('🧴 Gota térmica fresca aplicada en el chip del CPU móvil.', 'success');
        }
      });
    }

    // ETAPA 5: RAM SO-DIMM (45 GRADOS)
    const clipL = document.getElementById('clipL1');
    const clipR = document.getElementById('clipR1');
    const soModule1 = document.getElementById('soDimm1');

    const trigger45Degrees = () => {
      this.ramEjected45 = true;
      soModule1.classList.add('ejected');
      this.markTask('ram_clips');
      if (window.showAppToast) window.showAppToast('¡Clips liberados! El módulo SO-DIMM de 4GB saltó a un ángulo de 45° listo para retirarse.', 'success');
    };

    if (clipL) clipL.addEventListener('click', trigger45Degrees);
    if (clipR) clipR.addEventListener('click', trigger45Degrees);

    if (soModule1) {
      soModule1.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB[this.ramInstalled === 'new' ? 'sodimm_new' : 'sodimm_old']);
          return;
        }
        if (!this.ramEjected45) {
          if (window.showAppToast) window.showAppToast('Abre los dos clips laterales para que el módulo se incline a 45° antes de retirarlo.', 'error');
          return;
        }
        soModule1.style.display = 'none';
        this.ramInstalled = 'none';
        this.markTask('ram_remove_old');
        if (window.showAppToast) window.showAppToast('RAM vieja de 4GB retirada. Selecciona el módulo Kingston de 16GB de la bandeja para instalarlo a 45°.', 'info');
      });
    }

    // ETAPA 6: DISCO DURO & CADDY (UPGRADE A SSD)
    const caddyPull = document.getElementById('caddyPullTab');
    const hddCaddy = document.getElementById('ciscoHdd');
    const cscrew1 = document.getElementById('caddyScrew1');
    const cscrew2 = document.getElementById('caddyScrew2');

    if (caddyPull) {
      caddyPull.addEventListener('click', (e) => {
        e.stopPropagation();
        this.caddyDisconnected = true;
        hddCaddy.style.transform = 'translateX(-30px)';
        this.markTask('hdd_pull');
        if (window.showAppToast) window.showAppToast('Caddy desacoplado del conector SATA interno.', 'info');
      });
    }

    const unscrewCaddy = (el) => {
      if (this.activeTool !== 'screwdriver') {
        if (window.showAppToast) window.showAppToast('Usa el destornillador en los tornillos del caddy.', 'warning');
        return;
      }
      el.style.opacity = '0.2';
      this.caddyScrewsOut = true;
      this.markTask('hdd_caddy_screws');
      if (window.showAppToast) window.showAppToast('Tornillos laterales del caddy desatornillados.', 'info');
    };

    if (cscrew1) cscrew1.addEventListener('click', (e) => { e.stopPropagation(); unscrewCaddy(cscrew1); });
    if (cscrew2) cscrew2.addEventListener('click', (e) => { e.stopPropagation(); unscrewCaddy(cscrew2); });

    if (hddCaddy) {
      hddCaddy.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.activeTool === 'inspect') {
          this.openInspector(this.laptopDB[this.hddInstalled === 'new' ? 'ssd_new' : 'hdd_old']);
          return;
        }
        if (!this.caddyDisconnected) {
          if (window.showAppToast) window.showAppToast('Tira de la lengüeta plástica para desconectar el disco del puerto SATA.', 'error');
          return;
        }
        if (!this.caddyScrewsOut) {
          if (window.showAppToast) window.showAppToast('Desatornilla los tornillos del caddy con el destornillador antes de retirar el disco.', 'error');
          return;
        }
        hddCaddy.style.display = 'none';
        this.hddInstalled = 'none';
        if (window.showAppToast) window.showAppToast('Disco mecánico viejo extraído del caddy. Selecciona el nuevo SSD de 1TB de la bandeja.', 'info');
      });
    }

    // ETAPA 7: TECLADO & CABLE FLEX ZIF
    const kb = document.getElementById('ciscoKeyboard');
    const zifFlap = document.getElementById('zifFlap');

    if (kb) {
      kb.addEventListener('click', () => {
        if (!this.keyboardLifted) {
          this.keyboardLifted = true;
          kb.style.transform = 'translateY(-25px) rotate(-4deg)';
          this.markTask('kb_lift');
          if (window.showAppToast) window.showAppToast('Teclado levantado. ¡Cuidado con el cable plano ZIF!', 'warning');
        } else if (this.zifFlapOpen) {
          kb.style.display = 'none';
          this.keyboardRemoved = true;
          this.markTask('kb_cable');
          if (window.showAppToast) window.showAppToast('Cable plano liberado y ensamble de teclado retirado con seguridad.', 'success');
        } else {
          if (window.showAppToast) window.showAppToast('¡Alto! Destraba la solapa del conector ZIF antes de jalar el teclado o romperás las pistas.', 'error');
        }
      });
    }

    if (zifFlap) {
      zifFlap.addEventListener('click', () => {
        this.zifFlapOpen = true;
        zifFlap.style.backgroundColor = '#27c93f';
        this.markTask('zif_unlock');
        if (window.showAppToast) window.showAppToast('Solapa ZIF levantada. El cable flex está libre para desconectarse.', 'success');
      });
    }

    // Navegación entre etapas
    if (this.btnNext) {
      this.btnNext.addEventListener('click', () => {
        const order = ['battery', 'optical', 'cover', 'cooling', 'ram', 'storage', 'keyboard'];
        const idx = order.indexOf(this.currentStage);
        if (idx < order.length - 1) {
          this.setStage(order[idx + 1]);
        } else {
          this.setStage(order[0]);
        }
      });
    }

    if (this.btnReset) {
      this.btnReset.addEventListener('click', () => {
        const s = this.stagesData[this.currentStage];
        s.tasks.forEach(t => t.done = false);
        this.setStage(this.currentStage);
        if (window.showAppToast) window.showAppToast(`Etapa ${s.title} reiniciada.`, 'info');
      });
    }
  }
}
