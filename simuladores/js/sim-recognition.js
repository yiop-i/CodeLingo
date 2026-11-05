/**
 * SIM-RECOGNITION.JS - SIMULADOR 1 DEDICADO: RECONOCIMIENTO DE COMPONENTES 3D
 * Inspección 3D orbital en 360°, hotspots interactivos con zoom cinemático
 * y examen interactivo con modelos WebGL (Estilo pclab.eniun.com)
 */

class HardwareRecognitionSim {
  constructor() {
    this.currentMode = 'explore'; // 'explore' o 'quiz'
    this.activeCategory = 'all';
    this.quizScore = 0;
    this.quizTotal = 0;
    this.world3D = null;
    this.activeMesh = null;

    this.database = [
      {
        id: 'comp_mobo',
        name: 'Placa Base / Tarjeta Madre (Motherboard ATX)',
        category: 'pc',
        icon: '🖲️',
        desc: 'Circuito impreso principal (PCB multicapa) que interconecta todos los buses y componentes del sistema (CPU, RAM, GPU, Almacenamiento y periféricos).',
        slot: 'Se atornilla sobre los 9 separadores metálicos del chasis (Gabinete ATX/Micro-ATX/ITX).',
        voltage: 'Alimentada por el conector principal ATX de 24 pines y conectores EPS de 8 pines.',
        cameraPos: [0, 14, 18],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Socket del Procesador (LGA1700)', cam: [0, 6, 6], look: [0, 0, 3], tip: 'Zócalo donde se inserta el CPU. Cuenta con 1700 contactos dorados y palanca de acero.' },
          { name: 'Ranuras DIMM DDR5 (Dual-Channel)', cam: [6, 6, 6], look: [4.2, 0, 3], tip: 'Ranuras para memorias DDR5 de alta frecuencia con pestillos de retención en extremos.' },
          { name: 'Ranura Blindada PCIe 5.0 x16 (GPU)', cam: [-1, 5, -2], look: [-0.5, 0, -3.2], tip: 'Slot reforzado con armadura de acero para tarjetas gráficas pesadas de alto ancho de banda.' },
          { name: 'Ranura M.2 NVMe PCIe 4.0', cam: [0, 4, 1], look: [0, 0, -1.2], tip: 'Zócalo compacto para almacenamiento SSD ultrarrápido conectado directo a líneas PCIe.' },
          { name: 'Disipadores de Aluminio VRM', cam: [-4, 5, 6], look: [-3.2, 0, 3.2], tip: 'Módulos reguladores de voltaje masivos que estabilizan la corriente hacia el microprocesador.' }
        ],
        quizQ: '¿Cuál es el conector principal que alimenta de energía eléctrica a toda la placa madre?',
        quizOpts: ['Conector ATX principal de 24 pines', 'Cable HDMI de alta velocidad', 'Conector SATA de datos'],
        quizAns: 0
      },
      {
        id: 'comp_cpu',
        name: 'Unidad Central de Procesamiento (CPU Intel Core i9-14900K)',
        category: 'pc',
        icon: '🔲',
        desc: 'El "cerebro" del ordenador. Ejecuta cálculos lógicos, aritméticos y coordina todas las instrucciones del sistema operativo.',
        slot: 'Se coloca en el Socket de la placa madre respetando el triángulo dorado de alineación.',
        voltage: 'Voltaje de núcleo entre 0.8V y 1.45V con un consumo pico de hasta 253W en carga máxima.',
        cameraPos: [0, 5, 6],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'IHS (Integrated Heat Spreader)', cam: [0, 4, 3], look: [0, 0, 0], tip: 'Difusor térmico de níquel pulido con grabado láser que transfiere el calor al disipador.' },
          { name: 'Pads de Contacto LGA (Parte inferior)', cam: [0, -4, 3], look: [0, 0, 0], tip: 'Contactos dorados que apoyan sobre los pines elásticos del zócalo sin doblarlos.' },
          { name: 'Triángulo Dorado de Alineación', cam: [-1.5, 2, 2], look: [-1.5, 0, 1.5], tip: 'Guía visual indispensable: debe coincidir exactamente con la flecha del socket de la placa.' }
        ],
        quizQ: '¿Qué componente se debe aplicar siempre entre el IHS del CPU y la base del disipador?',
        quizOpts: ['Pasta térmica de alta conductividad', 'Alcohol en gel', 'Aceite mineral'],
        quizAns: 0
      },
      {
        id: 'comp_ram',
        name: 'Memoria RAM DDR5 Gamer (32GB 6000MHz Dual Channel)',
        category: 'pc',
        icon: '💾',
        desc: 'Memoria volátil ultrarrápida. Almacena en tiempo real los datos que el procesador necesita inmediatamente para evitar cuellos de botella.',
        slot: 'Se instala en las ranuras DIMM abriendo los pestillos y ejerciendo presión uniforme hasta escuchar el "clic".',
        voltage: 'DDR5 estándar a 1.1V (hasta 1.35V con perfiles XMP 3.0 / EXPO overclocking).',
        cameraPos: [0, 4, 7],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Muesca Central de Seguridad (Key Notch)', cam: [0, 1, 3], look: [0, -0.9, 0], tip: 'Ranura física descentrada que impide instalar el módulo al revés o forzar DDR4 en DDR5.' },
          { name: 'Disipador Térmico de Aluminio', cam: [0, 2, 4], look: [0, 0, 0], tip: 'Cuerpo de aleación de aluminio que absorbe el calor de los chips de memoria a 6000+ MHz.' },
          { name: 'Barra Difusora Superior RGB', cam: [0, 3, 2], look: [0, 0.95, 0], tip: 'Polímero acrílico translúcido con diodos LED direccionables sincronizados por software.' }
        ],
        quizQ: '¿Qué ocurre con la información en la memoria RAM al apagar por completo la computadora?',
        quizOpts: ['Se borra completamente por ser memoria volátil', 'Se guarda para siempre como en un disco rígido', 'Se envía a la nube automáticamente'],
        quizAns: 0
      },
      {
        id: 'comp_gpu',
        name: 'Tarjeta Gráfica Dedicada (NVIDIA GeForce RTX 4080 Super)',
        category: 'pc',
        icon: '🎮',
        desc: 'Aceleradora gráfica masiva con miles de núcleos CUDA / RT Cores dedicada al renderizado 3D en tiempo real, trazado de rayos (Ray Tracing) e Inteligencia Artificial.',
        slot: 'Se conecta en la ranura PCIe 5.0 x16 y se atornilla al chasis con dos tornillos metálicos.',
        voltage: 'Requiere alimentación suplementaria mediante conector 12VHPWR (hasta 450W).',
        cameraPos: [0, 7, 13],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Conector Dorado PCIe x16', cam: [-1, 2, 4], look: [-1, 0.4, 2.3], tip: 'Peine de 164 contactos dorados que se inserta firmemente en la ranura PCIe blindada.' },
          { name: 'Sistema de Refrigeración Triple Fan', cam: [0, 2, 6], look: [0, -1.8, 0], tip: 'Tres ventiladores axiales con aspas invertidas y disipador atravesado por tubos de cobre.' },
          { name: 'Soporte Metálico Posterior (I/O Bracket)', cam: [-5, 2, 3], look: [-5.8, -0.6, 0], tip: 'Sujeta la tarjeta al gabinete y aloja los puertos DisplayPort 1.4a y HDMI 2.1.' }
        ],
        quizQ: '¿En qué ranura específica de la placa madre se instala la tarjeta gráfica principal?',
        quizOpts: ['Ranura PCIe x16 (blindada)', 'Ranura DIMM de memoria RAM', 'Puerto SATA'],
        quizAns: 0
      },
      {
        id: 'comp_m2',
        name: 'Unidad de Estado Sólido SSD M.2 NVMe (Samsung 990 Pro 2TB)',
        category: 'pc',
        icon: '⚡',
        desc: 'Almacenamiento flash de estado sólido de ultra alta velocidad. Ofrece velocidades de lectura y escritura superiores a 7000 MB/s gracias al protocolo NVMe.',
        slot: 'Se inserta a 30° en la ranura M.2 de la placa base y se asegura con el tornillo o pestillo giratorio.',
        voltage: '3.3V suministrado directamente por el zócalo M.2.',
        cameraPos: [0, 4, 6],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Conector M-Key Dorado', cam: [-2, 2, 2], look: [-2, 0, 0], tip: 'Pines con muesca tipo M que conectan 4 líneas PCIe 4.0 directamente al microprocesador.' },
          { name: 'Chips de Memoria V-NAND Flash', cam: [1, 2, 2], look: [1, 0, 0], tip: 'Pastillas de silicio donde se almacenan los archivos de forma permanente sin partes mecánicas.' }
        ],
        quizQ: '¿Cuál es la principal ventaja de un SSD M.2 NVMe frente a un disco duro tradicional HDD?',
        quizOpts: ['Velocidad hasta 50 veces superior, sin ruidos mecánicos ni piezas móviles', 'Es más grande y pesado', 'Tiene partes mecánicas giratorias'],
        quizAns: 0
      },
      {
        id: 'comp_cooler',
        name: 'Disipador Térmico de Torre con Heatpipes y Ventilador PWM',
        category: 'pc',
        icon: '❄️',
        desc: 'Sistema de enfriamiento por aire para CPU compuesto por base de contacto de cobre, tubos de transferencia de calor sellados y aletas de aluminio.',
        slot: 'Se atornilla sobre el backplate posterior de la placa madre presionando contra el procesador.',
        voltage: 'Ventilador alimentado por conector PWM de 4 pines (12V DC).',
        cameraPos: [0, 6, 10],
        lookAt: [0, 3, 0],
        hotspots: [
          { name: 'Base de Contacto de Cobre Pulido', cam: [0, 1, 4], look: [0, 0.2, 0], tip: 'Superficie plana que hace contacto térmico directo con el procesador mediante pasta térmica.' },
          { name: 'Tubos de Cobre (Heatpipes)', cam: [1, 4, 3], look: [0, 3.4, 0], tip: 'Tubos sellados al vacío con líquido en cambio de fase que conducen el calor velozmente.' },
          { name: 'Ventilador de 120mm PWM Silencioso', cam: [0, 4, 4], look: [0, 3.8, 1.7], tip: 'Genera flujo de aire constante a través de las aletas para expulsar el calor al exterior.' }
        ],
        quizQ: '¿Qué componente conduce el calor desde la base de cobre hacia las aletas del disipador?',
        quizOpts: ['Los tubos de cobre sellados (Heatpipes)', 'El cable SATA', 'El conector RGB'],
        quizAns: 0
      },
      {
        id: 'comp_laptop_battery',
        name: 'Batería de Notebook Li-Ion (4 Celdas 5200mAh)',
        category: 'laptop',
        icon: '🔋',
        desc: 'Módulo de energía autónomo para portátiles con celdas de iones de litio y circuito BMS de protección contra sobrecargas.',
        slot: 'Bahía inferior asegurada con pestillos mecánicos Lock (bloqueo) y Release (expulsión).',
        voltage: 'Voltaje nominal de 11.1V a 14.8V.',
        cameraPos: [0, 5, 8],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Terminal de Conexión Multipin', cam: [3, 2, 3], look: [2.8, 0, 1.15], tip: 'Conecta el bus de energía y comunicación SMBus con la placa madre de la notebook.' },
          { name: 'Pestillos de Seguridad (Lock & Release)', cam: [-3, 2, -2], look: [-3.2, 0, -1.15], tip: 'Traban mecánicamente el pack al chasis para evitar desconexiones accidentales.' }
        ],
        quizQ: '¿Cuál es la primera regla de seguridad técnica antes de abrir una notebook para mantenimiento?',
        quizOpts: ['Desconectar el cargador de pared y retirar la batería', 'Poner la notebook sobre una toalla mojada', 'Acelerar los ventiladores'],
        quizAns: 0
      },
      {
        id: 'comp_laptop_sodimm',
        name: 'Memoria RAM SO-DIMM (Laptop Form Factor 16GB)',
        category: 'laptop',
        icon: '💻💾',
        desc: 'Módulo de memoria RAM compacto diseñado específicamente para ordenadores portátiles, mini PCs y consolas.',
        slot: 'Se inserta obligatoriamente en un ángulo inclinado de 30° a 45° antes de presionar hacia abajo hasta el bloqueo.',
        voltage: '1.2V (DDR4) o 1.1V (DDR5).',
        cameraPos: [0, 3, 5],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Borde de Contactos a 45°', cam: [0, 1, 3], look: [0, -0.7, 0], tip: 'Debe ingresar completamente en la ranura con inclinación antes de presionar hacia abajo.' },
          { name: 'Muescas Laterales de Sujeción', cam: [0, 1, 2], look: [0, 0, 0], tip: 'Donde traban los dos resortes metálicos laterales de la bahía SO-DIMM.' }
        ],
        quizQ: '¿A qué ángulo se introduce un módulo de memoria RAM SO-DIMM en su ranura en una notebook?',
        quizOpts: ['A un ángulo inclinado de 30° a 45°', 'Totalmente vertical a 90°', 'Completamente plana a 0°'],
        quizAns: 0
      },
      {
        id: 'comp_laptop_heatpipe',
        name: 'Sistema Térmico de Laptop (Heatpipe Plano y Turbina Blower)',
        category: 'laptop',
        icon: '🌀🔥',
        desc: 'Circuito de refrigeración ultradelgado para portátiles con conductos planos de cobre al vacío y ventilador radial tipo turbina.',
        slot: 'Se atornilla en orden numerado cruzado (1, 2, 3, 4) sobre los núcleos del CPU y GPU.',
        voltage: 'Ventilador turbina alimentado por conector PWM de 5V DC.',
        cameraPos: [0, 6, 8],
        lookAt: [0, 0, 0],
        hotspots: [
          { name: 'Placa Térmica del CPU con Tornillos', cam: [-2, 2, 2], look: [-2, 0, 0], tip: 'Superficie de cobre que aprieta contra el silicio con resortes calibrados en cruz.' },
          { name: 'Conducto Plano de Cobre (Heatpipe)', cam: [0, 2, 2], look: [0.5, 0, 0.5], tip: 'Transporta el calor hacia las aletas del radiador sin aumentar el grosor de la laptop.' },
          { name: 'Turbina Blower de Expulsión', cam: [3, 2, 3], look: [3.2, 0, 0.8], tip: 'Aspira aire frío por debajo del chasis y lo expulsa lateralmente a través del radiador.' }
        ],
        quizQ: 'Si la rejilla del heatpipe se tapa de pelusa, ¿qué síntoma experimentará la laptop?',
        quizOpts: ['Sobrecalentamiento excesivo, ventilador al 100% ruidoso y apagones repentinos', 'El teclado dejará de responder', 'Aumentará la duración de la batería'],
        quizAns: 0
      }
    ];

    this.selectedComp = this.database[0];
    this.initDOM();
    this.init3DScene();
    this.renderList();
    this.renderComponent();
    this.bindEvents();
  }

  initDOM() {
    this.listEl = document.getElementById('recogCatalogList');
    this.cardTitle = document.getElementById('recogTitle');
    this.cardDesc = document.getElementById('recogDesc');
    this.cardSlot = document.getElementById('recogSlot');
    this.cardVoltage = document.getElementById('recogVoltage');
    this.visualBox = document.getElementById('recogVisualBox');
    this.tipBox = document.getElementById('recogTipBox');
    this.btnExplore = document.getElementById('btnModeExplore');
    this.btnQuiz = document.getElementById('btnModeQuiz');
    this.quizArea = document.getElementById('recogQuizArea');
    this.quizQuestion = document.getElementById('recogQuizQ');
    this.quizOptions = document.getElementById('recogQuizOpts');
    this.quizResult = document.getElementById('recogQuizResult');

    // Preparar contenedor visual para el Canvas 3D
    if (this.visualBox) {
      this.visualBox.style.position = 'relative';
      this.visualBox.style.padding = '0';
      this.visualBox.style.overflow = 'hidden';
      this.visualBox.style.background = '#0d0f17';
      this.visualBox.style.height = '360px';
    }
  }

  init3DScene() {
    if (!window.Hardware3DWorld) {
      console.warn('Hardware3DWorld aún no cargado');
      return;
    }

    // Instanciar el mundo 3D en el viewport
    this.world3D = new Hardware3DWorld('recogVisualBox', {
      cameraPos: [0, 8, 14],
      lookAt: [0, 0, 0],
      autoRotate: false,
      enableGrid: true
    });

    // Inyectar barra flotante de control de cámara 3D (Estilo pclab.eniun.com)
    const hudControls = document.createElement('div');
    hudControls.className = 'canvas-3d-hud';
    hudControls.innerHTML = `
      <button class="hud-3d-btn" id="btnRecogAutoRotate" title="Rotación Automática 360°">🔄 Girar</button>
      <button class="hud-3d-btn" id="btnRecogResetCam" title="Centrar Cámara">🎯 Centrar</button>
      <button class="hud-3d-btn" id="btnRecogTopView" title="Vista Superior">📐 Superior</button>
    `;
    this.visualBox.appendChild(hudControls);

    document.getElementById('btnRecogAutoRotate').addEventListener('click', () => {
      if (this.world3D.controls) {
        this.world3D.controls.autoRotate = !this.world3D.controls.autoRotate;
        document.getElementById('btnRecogAutoRotate').classList.toggle('active', this.world3D.controls.autoRotate);
      }
    });

    document.getElementById('btnRecogResetCam').addEventListener('click', () => {
      const c = this.selectedComp;
      this.world3D.focusCamera(c.cameraPos, c.lookAt);
    });

    document.getElementById('btnRecogTopView').addEventListener('click', () => {
      this.world3D.focusCamera([0, 16, 0.01], [0, 0, 0]);
    });
  }

  renderList() {
    this.listEl.innerHTML = '';
    const filtered = this.activeCategory === 'all'
      ? this.database
      : this.database.filter(c => c.category === this.activeCategory);

    filtered.forEach(c => {
      const card = document.createElement('div');
      card.className = `recog-item-card ${c.id === this.selectedComp.id ? 'active' : ''}`;
      card.innerHTML = `
        <div class="recog-icon">${c.icon}</div>
        <div class="recog-info">
          <h4>${c.name.split('(')[0].trim()}</h4>
          <span>${c.category === 'pc' ? 'PC de Escritorio 3D' : 'Notebook / Laptop 3D'}</span>
        </div>
      `;
      card.addEventListener('click', () => {
        this.selectedComp = c;
        this.renderList();
        this.renderComponent();
      });
      this.listEl.appendChild(card);
    });
  }

  renderComponent() {
    const c = this.selectedComp;
    this.cardTitle.textContent = c.name;
    this.cardDesc.textContent = c.desc;
    this.cardSlot.textContent = c.slot;
    this.cardVoltage.textContent = c.voltage;
    this.tipBox.innerHTML = '💡 <strong>Navegación 3D:</strong> Arrastra con el ratón o con el dedo en pantallas táctiles para rotar en 360°. Usa la rueda o pellizca para hacer zoom. Haz clic en los botones de inspección para enfocar cada parte.';

    // Actualizar Modelo 3D en el escenario
    this.update3DModel(c);

    // Renderizar botones de inspección de Hotspots
    this.renderHotspotsList(c);

    // Renderizar Quiz si está activo
    if (this.currentMode === 'quiz') {
      this.renderQuiz();
    }
  }

  update3DModel(comp) {
    if (!this.world3D) return;

    this.world3D.clearScene();

    let mesh = null;
    switch (comp.id) {
      case 'comp_mobo':
        mesh = this.world3D.createMotherboard3D();
        break;
      case 'comp_cpu':
        mesh = this.world3D.createCpu3D();
        break;
      case 'comp_ram':
        mesh = this.world3D.createRamDDR53D();
        break;
      case 'comp_gpu':
        mesh = this.world3D.createGPU3D();
        break;
      case 'comp_m2':
        mesh = this.world3D.createM2SSD3D();
        break;
      case 'comp_cooler':
        mesh = this.world3D.createCooler3D();
        break;
      case 'comp_laptop_battery':
        mesh = this.world3D.createLaptopBattery3D();
        break;
      case 'comp_laptop_sodimm':
        mesh = this.world3D.createRamSODIMM3D();
        break;
      case 'comp_laptop_heatpipe':
        mesh = this.world3D.createLaptopHeatpipe3D();
        break;
      default:
        mesh = this.world3D.createMotherboard3D();
    }

    if (mesh) {
      this.activeMesh = mesh;
      this.world3D.scene.add(mesh);
      this.world3D.focusCamera(comp.cameraPos, comp.lookAt, 700);
    }
  }

  renderHotspotsList(comp) {
    // Si existe contenedor previo de hotspots, remover
    let hostpotBar = document.getElementById('recogHotspotsBar');
    if (!hostpotBar) {
      hostpotBar = document.createElement('div');
      hostpotBar.id = 'recogHotspotsBar';
      hostpotBar.className = 'recog-hotspots-bar';
      this.tipBox.parentNode.insertBefore(hostpotBar, this.tipBox);
    }

    hostpotBar.innerHTML = '<span class="hotspot-bar-title">🔍 Puntos Clave de Inspección 3D:</span>';
    const btnGroup = document.createElement('div');
    btnGroup.className = 'hotspot-btn-group';

    comp.hotspots.forEach((h, idx) => {
      const btn = document.createElement('button');
      btn.className = 'hotspot-btn';
      btn.innerHTML = `<span class="h-num">${idx + 1}</span> <span>${h.name}</span>`;
      btn.addEventListener('click', () => {
        // Enfoque cinemático de cámara hacia el punto exacto
        this.world3D.focusCamera(h.cam, h.look, 700);
        this.tipBox.innerHTML = `<strong>🔍 ${h.name}:</strong> ${h.tip}`;
        document.querySelectorAll('.hotspot-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
      btnGroup.appendChild(btn);
    });

    hostpotBar.appendChild(btnGroup);
  }

  renderQuiz() {
    const c = this.selectedComp;
    this.quizArea.style.display = 'flex';
    this.quizQuestion.textContent = c.quizQ;
    this.quizOptions.innerHTML = '';
    this.quizResult.textContent = '';

    c.quizOpts.forEach((optText, idx) => {
      const btn = document.createElement('button');
      btn.className = 'quiz-btn';
      btn.textContent = `${['A', 'B', 'C'][idx]}) ${optText}`;
      btn.addEventListener('click', async () => {
        this.quizTotal++;

        // Validación de evaluación mediante el backend Python
        let isCorrect = (idx === c.quizAns);
        try {
          const resp = await fetch('/api/hw/recog/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ component_id: c.id, option_index: idx })
          });
          if (resp.ok) {
            const data = await resp.json();
            isCorrect = data.correct;
          }
        } catch(err) {}

        if (isCorrect) {
          btn.classList.add('correct');
          this.quizScore++;
          this.quizResult.textContent = `✅ ¡Correcto! Respuestas acertadas: ${this.quizScore} de ${this.quizTotal}`;
          this.quizResult.style.color = '#4ec9b0';
        } else {
          btn.classList.add('wrong');
          this.quizResult.textContent = `❌ Incorrecto. La respuesta técnica correcta era: ${c.quizOpts[c.quizAns]}`;
          this.quizResult.style.color = '#f14c4c';
        }
      });
      this.quizOptions.appendChild(btn);
    });
  }

  bindEvents() {
    this.btnExplore.addEventListener('click', () => {
      this.currentMode = 'explore';
      this.btnExplore.classList.add('active');
      this.btnQuiz.classList.remove('active');
      this.quizArea.style.display = 'none';
    });

    this.btnQuiz.addEventListener('click', () => {
      this.currentMode = 'quiz';
      this.btnQuiz.classList.add('active');
      this.btnExplore.classList.remove('active');
      this.renderQuiz();
    });

    // Filtros de categoría PC vs Laptop
    document.querySelectorAll('.recog-cat-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.recog-cat-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.activeCategory = btn.dataset.cat;
        this.renderList();
      });
    });
  }
}

window.HardwareRecognitionSim = HardwareRecognitionSim;
