/**
 * SIM-PLACEMENT.JS - SIMULADOR 2 DEDICADO: MONTAJE EN SU LUGAR CORRESPONDIENTE 3D
 * Ensamble guiado con modelos WebGL 3D, animación de inserción mecánica
 * y validación estricta de ranuras (Estilo pclab.eniun.com)
 */

class HardwarePlacementSim {
  constructor() {
    this.currentMachine = 'desktop'; // 'desktop' o 'notebook'
    this.selectedPart = null;
    this.world3D = null;
    this.installed3DParts = {};

    // Componentes para montar en PC de Escritorio
    this.desktopParts = [
      {
        id: 'part_cpu',
        name: 'Intel Core i9-14900K',
        icon: '🔲',
        validSlot: 'target_cpu',
        desc: 'Socket LGA1700',
        camFocus: [0, 6, 6],
        lookAt: [0, 0, 3],
        target3DPos: new THREE.Vector3(0, 0.35, 3),
        createMesh: () => this.world3D.createCpu3D()
      },
      {
        id: 'part_cooler',
        name: 'Disipador de Torre con Heatpipes',
        icon: '❄️',
        validSlot: 'target_cooler',
        desc: 'Soporte y Backplate del CPU',
        requires: 'part_cpu',
        camFocus: [0, 8, 9],
        lookAt: [0, 3, 3],
        target3DPos: new THREE.Vector3(0, 0.5, 3),
        createMesh: () => this.world3D.createCooler3D()
      },
      {
        id: 'part_ram',
        name: 'Kit 32GB DDR5 RGB (Dual-Channel)',
        icon: '💾',
        validSlot: 'target_ram',
        desc: 'Ranuras DIMM 2 y 4',
        camFocus: [6, 6, 6],
        lookAt: [4.2, 0, 3],
        target3DPos: new THREE.Vector3(4.2, 0.8, 3.0),
        createMesh: () => this.world3D.createRamDDR53D()
      },
      {
        id: 'part_gpu',
        name: 'NVIDIA RTX 4080 Super 16GB',
        icon: '🎮',
        validSlot: 'target_gpu',
        desc: 'Ranura PCIe 5.0 x16 Blindada',
        camFocus: [-1, 7, 5],
        lookAt: [-0.5, 0, -3.2],
        target3DPos: new THREE.Vector3(-0.5, 1.2, -3.2),
        createMesh: () => this.world3D.createGPU3D()
      },
      {
        id: 'part_m2',
        name: 'SSD Samsung 990 Pro 2TB NVMe',
        icon: '⚡',
        validSlot: 'target_m2',
        desc: 'Zócalo M.2 PCIe 4.0',
        camFocus: [0, 5, 2],
        lookAt: [0, 0, -1.2],
        target3DPos: new THREE.Vector3(0, 0.35, -1.2),
        createMesh: () => this.world3D.createM2SSD3D()
      }
    ];

    // Componentes para montar en Notebook CISCO
    this.notebookParts = [
      {
        id: 'lap_battery',
        name: 'Batería Li-Ion 5200mAh',
        icon: '🔋',
        validSlot: 'target_lap_battery',
        desc: 'Bahía de Batería con Pestillos Lock',
        camFocus: [0, 6, 8],
        lookAt: [0, 0, 0],
        target3DPos: new THREE.Vector3(0, 0.6, 5),
        createMesh: () => this.world3D.createLaptopBattery3D()
      },
      {
        id: 'lap_sodimm',
        name: 'Memoria RAM SO-DIMM 16GB (45°)',
        icon: '💻💾',
        validSlot: 'target_lap_sodimm',
        desc: 'Ranura SO-DIMM (Ángulo a 45°)',
        camFocus: [4, 5, 4],
        lookAt: [2, 0, 0],
        target3DPos: new THREE.Vector3(2, 0.3, 0),
        createMesh: () => this.world3D.createRamSODIMM3D()
      },
      {
        id: 'lap_heatpipe',
        name: 'Heatpipe de Cobre & Turbina Blower',
        icon: '🌀',
        validSlot: 'target_lap_cooling',
        desc: 'Circuito Térmico del CPU/GPU',
        camFocus: [0, 6, 6],
        lookAt: [0, 0, 0],
        target3DPos: new THREE.Vector3(-0.5, 0.3, 0),
        createMesh: () => this.world3D.createLaptopHeatpipe3D()
      }
    ];

    this.slotsState = {};
    this.initDOM();
    this.init3DScene();
    this.renderParts();
    this.bindEvents();
  }

  initDOM() {
    this.palette = document.getElementById('placePalette');
    this.machineTitle = document.getElementById('placeMachineTitle');
    this.statusMsg = document.getElementById('placeStatusMsg');
    this.desktopChassis = document.getElementById('placeDesktopChassis');
    this.notebookChassis = document.getElementById('placeNotebookChassis');
    this.btnDesktop = document.getElementById('btnPlaceDesktop');
    this.btnNotebook = document.getElementById('btnPlaceNotebook');
    this.btnReset = document.getElementById('btnPlaceReset');

    // Contenedor principal del escenario
    this.stageContainer = document.querySelector('.place-chassis-stage');
  }

  init3DScene() {
    // Si ya existe el contenedor 3D, evitar duplicarlo
    let container3D = document.getElementById('place3DViewport');
    if (!container3D) {
      container3D = document.createElement('div');
      container3D.id = 'place3DViewport';
      container3D.className = 'place-3d-viewport';
      container3D.style.width = '100%';
      container3D.style.height = '380px';
      container3D.style.position = 'relative';
      container3D.style.borderRadius = '10px';
      container3D.style.overflow = 'hidden';
      container3D.style.background = '#0e1017';
      container3D.style.marginBottom = '14px';

      // Insertar antes del contenedor de slots
      const chassisContainer = document.querySelector('.place-chassis-container');
      if (chassisContainer) {
        chassisContainer.parentNode.insertBefore(container3D, chassisContainer);
      }
    }

    if (!window.Hardware3DWorld) return;

    this.world3D = new Hardware3DWorld('place3DViewport', {
      cameraPos: [0, 16, 20],
      lookAt: [0, 0, 0],
      autoRotate: false,
      enableGrid: true
    });

    // Inyectar HUD de control de cámara 3D
    const hud = document.createElement('div');
    hud.className = 'canvas-3d-hud';
    hud.innerHTML = `
      <button class="hud-3d-btn" id="btnPlaceAutoRotate">🔄 Girar 360°</button>
      <button class="hud-3d-btn" id="btnPlaceResetCam">🎯 Vista General</button>
      <button class="hud-3d-btn" id="btnPlaceTopCam">📐 Vista Superior</button>
    `;
    container3D.appendChild(hud);

    document.getElementById('btnPlaceAutoRotate').addEventListener('click', () => {
      if (this.world3D.controls) {
        this.world3D.controls.autoRotate = !this.world3D.controls.autoRotate;
        document.getElementById('btnPlaceAutoRotate').classList.toggle('active', this.world3D.controls.autoRotate);
      }
    });

    document.getElementById('btnPlaceResetCam').addEventListener('click', () => {
      this.world3D.focusCamera([0, 16, 20], [0, 0, 0]);
    });

    document.getElementById('btnPlaceTopCam').addEventListener('click', () => {
      this.world3D.focusCamera([0, 22, 0.01], [0, 0, 0]);
    });

    // Cargar la placa base base en 3D
    this.loadMachine3D();
  }

  loadMachine3D() {
    if (!this.world3D) return;
    this.world3D.clearScene();
    this.installed3DParts = {};

    if (this.currentMachine === 'desktop') {
      const mobo = this.world3D.createMotherboard3D();
      this.world3D.scene.add(mobo);
      this.world3D.focusCamera([0, 16, 18], [0, 0, 0], 600);
    } else {
      // Placa de notebook compacta
      const mobo = this.world3D.createMotherboard3D();
      mobo.scale.set(0.85, 1, 0.85);
      this.world3D.scene.add(mobo);
      this.world3D.focusCamera([0, 14, 16], [0, 0, 0], 600);
    }
  }

  switchMachine(type) {
    this.currentMachine = type;
    this.btnDesktop.classList.toggle('active', type === 'desktop');
    this.btnNotebook.classList.toggle('active', type === 'notebook');

    if (type === 'desktop') {
      this.machineTitle.textContent = 'Gabinete Gamer ATX (Montaje de Escritorio 3D)';
      this.desktopChassis.style.display = 'grid';
      this.notebookChassis.style.display = 'none';
    } else {
      this.machineTitle.textContent = 'Chasis de Notebook (Cisco Virtual Laptop 3D)';
      this.desktopChassis.style.display = 'none';
      this.notebookChassis.style.display = 'grid';
    }

    this.selectedPart = null;
    this.slotsState = {};
    this.loadMachine3D();
    this.renderParts();
    this.updateStatus('Selecciona una pieza de la paleta izquierda y haz clic en su ranura correspondiente para instalarla en 3D.');
  }

  renderParts() {
    this.palette.innerHTML = '';
    const parts = this.currentMachine === 'desktop' ? this.desktopParts : this.notebookParts;

    parts.forEach(p => {
      const isPlaced = this.slotsState[p.id];
      const card = document.createElement('div');
      card.className = `place-item-card ${isPlaced ? 'placed' : ''} ${this.selectedPart && this.selectedPart.id === p.id ? 'active' : ''}`;
      card.innerHTML = `
        <span class="place-icon">${p.icon}</span>
        <div class="place-info">
          <h4>${p.name}</h4>
          <span>${isPlaced ? '✓ Instalado en su lugar' : 'Destino: ' + p.desc}</span>
        </div>
      `;

      card.addEventListener('click', () => {
        if (isPlaced) return;
        this.selectedPart = p;
        this.renderParts();
        this.highlightValidSlot(p);

        // Enfoque suave de cámara hacia la ranura objetivo en el modelo 3D
        if (this.world3D && p.camFocus) {
          this.world3D.focusCamera(p.camFocus, p.lookAt, 700);
        }

        this.updateStatus(`Has tomado: <strong>${p.name}</strong>. Haz clic en su ranura correspondiente (marcada en verde) para ensamblarla.`);
      });

      this.palette.appendChild(card);
    });
  }

  highlightValidSlot(part) {
    document.querySelectorAll('.slot-target-box').forEach(slot => {
      slot.classList.remove('highlight-valid', 'highlight-invalid');
      if (slot.id === part.validSlot) {
        slot.classList.add('highlight-valid');
      }
    });
  }

  async handleSlotClick(slotEl) {
    if (!this.selectedPart) {
      this.updateStatus('Primero selecciona un componente de la paleta izquierda para colocarlo en 3D.');
      return;
    }

    const part = this.selectedPart;
    const targetId = slotEl.id;

    // Validación de prelación y reglas mediante el motor Python
    try {
      const resp = await fetch('/api/hw/placement/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          machine_type: this.currentMachine,
          part_id: part.id,
          slot_id: targetId
        })
      });
      if (resp.ok) {
        const val = await resp.json();
        if (!val.success) {
          this.showError(slotEl, val.message);
          if (this.world3D) {
            this.world3D.flashSlotBox(part.target3DPos || new THREE.Vector3(0, 1, 0), new THREE.Vector3(4, 1, 4), false);
          }
          return;
        }
      }
    } catch(err) {}

    // Validación de prelación (ej: disipador requiere CPU primero)
    if (part.requires && !this.slotsState[part.requires]) {
      this.showError(slotEl, `¡Error de secuencia técnica! Debes instalar primero el CPU antes de colocar el disipador.`);
      if (this.world3D) {
        this.world3D.flashSlotBox(part.target3DPos, new THREE.Vector3(4, 1, 4), false);
      }
      return;
    }

    // VALIDACIÓN ESTRICTA DE LUGAR
    if (targetId === part.validSlot) {
      // ÉXITO: Ranura correcta
      slotEl.classList.remove('highlight-valid', 'highlight-invalid');
      slotEl.classList.add('occupied');

      const contentEl = slotEl.querySelector('.slot-content');
      if (contentEl) contentEl.style.display = 'flex';
      const phEl = slotEl.querySelector('.slot-ph');
      if (phEl) phEl.style.display = 'none';

      // Animación 3D de inserción de la pieza
      if (this.world3D && part.createMesh) {
        const mesh = part.createMesh();
        this.world3D.animateSlotPlacement(mesh, part.target3DPos, () => {
          this.world3D.flashSlotBox(part.target3DPos, new THREE.Vector3(3.5, 0.8, 3.5), true);
        });
        this.installed3DParts[part.id] = mesh;
      }

      this.slotsState[part.id] = true;
      this.selectedPart = null;
      this.renderParts();

      if (window.showAppToast) {
        window.showAppToast(`¡Excelente! ${part.name} colocado con éxito en su ranura técnica.`, 'success');
      }
      this.updateStatus(`✅ <strong>${part.name}</strong> montado en <em>${part.desc}</em>. Selecciona el siguiente componente.`);
      this.checkCompletion();
    } else {
      // ERROR: Intentó poner la pieza en una ranura incompatible
      this.showError(slotEl, `❌ ¡Incompatibilidad física! No puedes colocar <strong>${part.name}</strong> en esa ranura. Su ubicación técnica correcta es: <strong>${part.desc}</strong>.`);
      if (this.world3D) {
        this.world3D.flashSlotBox(new THREE.Vector3(0, 1, 0), new THREE.Vector3(5, 1, 5), false);
      }
    }
  }

  showError(slotEl, message) {
    slotEl.classList.add('highlight-invalid');
    setTimeout(() => slotEl.classList.remove('highlight-invalid'), 600);
    this.updateStatus(message);
    if (window.showAppToast) {
      window.showAppToast('Ubicación incompatible. Lee la indicación de destino.', 'error');
    }
  }

  checkCompletion() {
    const parts = this.currentMachine === 'desktop' ? this.desktopParts : this.notebookParts;
    const allPlaced = parts.every(p => this.slotsState[p.id]);
    if (allPlaced) {
      this.updateStatus(`🎉 <strong>¡Felicitaciones!</strong> Todos los componentes de la ${this.currentMachine === 'desktop' ? 'PC' : 'Notebook'} han sido colocados en su lugar correspondiente sin ningún error.`);
      if (window.showAppToast) {
        window.showAppToast('¡Ensamble 3D completado al 100%! Máquina armada con éxito.', 'success');
      }
      if (this.world3D && this.world3D.controls) {
        this.world3D.controls.autoRotate = true;
      }
    }
  }

  updateStatus(html) {
    this.statusMsg.innerHTML = html;
  }

  resetAll() {
    this.slotsState = {};
    this.selectedPart = null;
    document.querySelectorAll('.slot-target-box').forEach(slot => {
      slot.classList.remove('occupied', 'highlight-valid', 'highlight-invalid');
      const contentEl = slot.querySelector('.slot-content');
      if (contentEl) contentEl.style.display = 'none';
      const phEl = slotEl => {
        const ph = slotEl.querySelector('.slot-ph');
        if (ph) ph.style.display = 'flex';
      };
      phEl(slot);
    });
    this.loadMachine3D();
    this.renderParts();
    this.updateStatus('Todos los componentes desmontados. Selecciona una pieza para comenzar.');
  }

  bindEvents() {
    this.btnDesktop.addEventListener('click', () => this.switchMachine('desktop'));
    this.btnNotebook.addEventListener('click', () => this.switchMachine('notebook'));
    this.btnReset.addEventListener('click', () => this.resetAll());

    // Clicks en todas las ranuras de montaje
    document.querySelectorAll('.slot-target-box').forEach(slot => {
      slot.addEventListener('click', () => this.handleSlotClick(slot));
    });
  }
}

window.HardwarePlacementSim = HardwarePlacementSim;
