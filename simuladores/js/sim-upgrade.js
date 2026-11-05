/**
 * SIM-UPGRADE.JS - SIMULADOR 3 DEDICADO: CAMBIO DE COMPONENTES VIEJOS POR NUEVOS 3D
 * Diagnóstico de cuellos de botella, desmontaje 3D de piezas obsoletas
 * e instalación de repuestos modernos con benchmarks en tiempo real
 */

class HardwareUpgradeSim {
  constructor() {
    this.currentCase = 'desktop'; // 'desktop' o 'laptop'
    this.world3D = null;
    this.installed3DMeshes = {};

    this.orders = {
      desktop: {
        client: 'Marcos R. (Gamer & Creador de Contenido)',
        problem: 'Mi PC tarda 3 minutos en prender, los juegos van a tirones (22 FPS) y el disco duro hace un ruido mecánico insoportable. Necesito un upgrade urgente.',
        tasks: [
          { id: 'u_hdd', text: 'Reemplazar disco mecánico HDD 500GB por SSD M.2 NVMe 2TB', done: false },
          { id: 'u_ram', text: 'Reemplazar 8GB RAM DDR4 genérica por Kit 32GB DDR5 6000MHz Dual Channel', done: false },
          { id: 'u_gpu', text: 'Reemplazar tarjeta gráfica GTX 1050 Ti por NVIDIA RTX 4080 Super 16GB', done: false }
        ]
      },
      laptop: {
        client: 'Elena G. (Diseñadora & Trabajo Remoto)',
        problem: 'Mi notebook hierve en las piernas, la batería solo dura 10 minutos y se congela al abrir Photoshop. Necesito batería nueva, más RAM y un disco rápido.',
        tasks: [
          { id: 'u_bat', text: 'Reemplazar batería degradada (15% salud) por batería nueva 5200mAh', done: false },
          { id: 'u_lap_ram', text: 'Reemplazar módulo SO-DIMM de 4GB por módulo de 16GB a 45°', done: false },
          { id: 'u_lap_cooling', text: 'Limpiar y reinstalar el sistema térmico con pasta térmica nueva', done: false }
        ]
      }
    };

    // Componentes del caso activo (viejos instalados vs repuestos nuevos)
    this.components = {
      desktop: {
        storage: {
          slotKey: 'storage',
          oldName: 'HDD Seagate 500GB 5400RPM Lento',
          newName: 'SSD Samsung 990 Pro 2TB NVMe 7450MB/s',
          state: 'old',
          target3DPos: new THREE.Vector3(0, 0.35, -1.2),
          createOldMesh: () => {
            const hdd = new THREE.Mesh(
              new THREE.BoxGeometry(4.5, 0.8, 6.0),
              new THREE.MeshStandardMaterial({ color: 0x333845, roughness: 0.6, metalness: 0.5 })
            );
            return hdd;
          },
          createNewMesh: () => this.world3D.createM2SSD3D()
        },
        ram: {
          slotKey: 'ram',
          oldName: '1x 8GB DDR4 2133MHz Verde Genérica',
          newName: '32GB (2x16GB) Corsair DDR5 6000MHz RGB',
          state: 'old',
          target3DPos: new THREE.Vector3(4.2, 0.8, 3.0),
          createOldMesh: () => {
            const ram = new THREE.Mesh(
              new THREE.BoxGeometry(0.12, 1.3, 5.0),
              new THREE.MeshStandardMaterial({ color: 0x1f5c35, roughness: 0.6 })
            );
            return ram;
          },
          createNewMesh: () => this.world3D.createRamDDR53D()
        },
        gpu: {
          slotKey: 'gpu',
          oldName: 'NVIDIA GeForce GTX 1050 Ti 4GB (Monoventilador)',
          newName: 'NVIDIA GeForce RTX 4080 Super 16GB Triple Fan',
          state: 'old',
          target3DPos: new THREE.Vector3(-0.5, 1.2, -3.2),
          createOldMesh: () => {
            const gpu = new THREE.Mesh(
              new THREE.BoxGeometry(6.5, 1.4, 3.5),
              new THREE.MeshStandardMaterial({ color: 0x22242b, roughness: 0.7 })
            );
            return gpu;
          },
          createNewMesh: () => this.world3D.createGPU3D()
        }
      },
      laptop: {
        battery: {
          slotKey: 'battery',
          oldName: 'Batería Li-Ion Degradada (Hinchada 15% vida útil)',
          newName: 'Batería Original 5200mAh 4 Celdas Nueva',
          state: 'old',
          target3DPos: new THREE.Vector3(0, 0.6, 5),
          createOldMesh: () => this.world3D.createLaptopBattery3D(),
          createNewMesh: () => this.world3D.createLaptopBattery3D()
        },
        ram: {
          slotKey: 'ram',
          oldName: 'SO-DIMM 4GB DDR4 2133MHz Lenta',
          newName: 'SO-DIMM 16GB DDR4 3200MHz Kingston',
          state: 'old',
          target3DPos: new THREE.Vector3(2, 0.3, 0),
          createOldMesh: () => this.world3D.createRamSODIMM3D(),
          createNewMesh: () => this.world3D.createRamSODIMM3D()
        },
        cooling: {
          slotKey: 'cooling',
          oldName: 'Disipador Térmico con pasta seca petrificada',
          newName: 'Sistema Térmico Limpio con Pasta Fresca',
          state: 'old',
          target3DPos: new THREE.Vector3(-0.5, 0.3, 0),
          createOldMesh: () => this.world3D.createLaptopHeatpipe3D(),
          createNewMesh: () => this.world3D.createLaptopHeatpipe3D()
        }
      }
    };

    this.initDOM();
    this.init3DScene();
    this.renderCase();
    this.bindEvents();
  }

  initDOM() {
    this.clientName = document.getElementById('upClientName');
    this.clientMsg = document.getElementById('upClientMsg');
    this.tasksList = document.getElementById('upTasksList');
    this.machineSlotArea = document.getElementById('upMachineSlotArea');
    this.storeList = document.getElementById('upStoreList');
    this.benchFps = document.getElementById('benchFpsVal');
    this.benchFpsBar = document.getElementById('benchFpsBar');
    this.benchBoot = document.getElementById('benchBootVal');
    this.benchBootBar = document.getElementById('benchBootBar');
    this.benchRam = document.getElementById('benchRamVal');
    this.benchRamBar = document.getElementById('benchRamBar');
    this.btnCaseDesktop = document.getElementById('btnUpCaseDesktop');
    this.btnCaseLaptop = document.getElementById('btnUpCaseLaptop');
  }

  init3DScene() {
    let container3D = document.getElementById('upgrade3DViewport');
    if (!container3D) {
      container3D = document.createElement('div');
      container3D.id = 'upgrade3DViewport';
      container3D.className = 'upgrade-3d-viewport';
      container3D.style.width = '100%';
      container3D.style.height = '340px';
      container3D.style.position = 'relative';
      container3D.style.borderRadius = '10px';
      container3D.style.overflow = 'hidden';
      container3D.style.background = '#0e1017';
      container3D.style.marginBottom = '14px';

      const benchArea = document.querySelector('.upgrade-bench-area');
      if (benchArea) {
        benchArea.parentNode.insertBefore(container3D, benchArea);
      }
    }

    if (!window.Hardware3DWorld) return;

    this.world3D = new Hardware3DWorld('upgrade3DViewport', {
      cameraPos: [0, 16, 20],
      lookAt: [0, 0, 0],
      autoRotate: false,
      enableGrid: true
    });

    const hud = document.createElement('div');
    hud.className = 'canvas-3d-hud';
    hud.innerHTML = `
      <button class="hud-3d-btn" id="btnUpAutoRotate">🔄 Girar 360°</button>
      <button class="hud-3d-btn" id="btnUpResetCam">🎯 Vista General</button>
    `;
    container3D.appendChild(hud);

    document.getElementById('btnUpAutoRotate').addEventListener('click', () => {
      if (this.world3D.controls) {
        this.world3D.controls.autoRotate = !this.world3D.controls.autoRotate;
        document.getElementById('btnUpAutoRotate').classList.toggle('active', this.world3D.controls.autoRotate);
      }
    });

    document.getElementById('btnUpResetCam').addEventListener('click', () => {
      this.world3D.focusCamera([0, 16, 20], [0, 0, 0]);
    });
  }

  load3DState() {
    if (!this.world3D) return;
    this.world3D.clearScene();
    this.installed3DMeshes = {};

    // Placa base
    const mobo = this.world3D.createMotherboard3D();
    this.world3D.scene.add(mobo);

    // Cargar componentes según su estado actual (old o new)
    const comps = this.components[this.currentCase];
    Object.keys(comps).forEach(slotKey => {
      const item = comps[slotKey];
      if (item.state === 'old' && item.createOldMesh) {
        const mesh = item.createOldMesh();
        mesh.position.copy(item.target3DPos);
        this.world3D.scene.add(mesh);
        this.installed3DMeshes[slotKey] = mesh;
      } else if (item.state === 'new' && item.createNewMesh) {
        const mesh = item.createNewMesh();
        mesh.position.copy(item.target3DPos);
        this.world3D.scene.add(mesh);
        this.installed3DMeshes[slotKey] = mesh;
      }
    });

    this.world3D.focusCamera([0, 16, 18], [0, 0, 0], 600);
  }

  setCase(caseKey) {
    this.currentCase = caseKey;
    this.btnCaseDesktop.classList.toggle('active', caseKey === 'desktop');
    this.btnCaseLaptop.classList.toggle('active', caseKey === 'laptop');
    this.renderCase();
  }

  renderCase() {
    const o = this.orders[this.currentCase];
    this.clientName.textContent = o.client;
    this.clientMsg.textContent = o.problem;

    this.load3DState();
    this.renderTasks();
    this.renderMachineSlots();
    this.renderStore();
    this.updateBenchmarks();
  }

  renderTasks() {
    const o = this.orders[this.currentCase];
    this.tasksList.innerHTML = '';
    o.tasks.forEach(t => {
      const li = document.createElement('li');
      li.className = `step-item ${t.done ? 'done' : ''}`;
      li.innerHTML = `<span>${t.done ? '✓' : '○'}</span> <span>${t.text}</span>`;
      this.tasksList.appendChild(li);
    });
  }

  renderMachineSlots() {
    this.machineSlotArea.innerHTML = '';
    const comps = this.components[this.currentCase];

    Object.keys(comps).forEach(slotKey => {
      const item = comps[slotKey];
      const slotBox = document.createElement('div');
      slotBox.className = `up-slot-card ${item.state}`;

      let badge = item.state === 'old' ? '⚠️ COMPONENTE VIEJO' : (item.state === 'empty' ? '⚪ RANURA VACÍA' : '✅ REPUESTO NUEVO INSTALADO');
      let name = item.state === 'old' ? item.oldName : (item.state === 'empty' ? 'Desmontado (Listo para instalar nuevo repuesto 3D)' : item.newName);

      slotBox.innerHTML = `
        <div class="slot-header">
          <span class="slot-type">${slotKey.toUpperCase()}</span>
          <span class="slot-badge ${item.state}">${badge}</span>
        </div>
        <div class="slot-name">${name}</div>
        <div class="slot-action-row">
          ${item.state === 'old' ? `<button class="up-btn unmount-btn">⬇ Desmontar Pieza Vieja</button>` : ''}
          ${item.state === 'empty' ? `<span class="slot-hint">Selecciona el repuesto nuevo de la tienda de la derecha ➔</span>` : ''}
          ${item.state === 'new' ? `<span class="slot-success">✓ Upgrade 3D completado exitosamente</span>` : ''}
        </div>
      `;

      const unmountBtn = slotBox.querySelector('.unmount-btn');
      if (unmountBtn) {
        unmountBtn.addEventListener('click', async () => {
          item.state = 'empty';

          // Notificar al backend Python de upgrades
          try {
            await fetch('/api/hw/upgrade/unmount', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ case: this.currentCase, slot: slotKey })
            });
          } catch(err) {}

          // Animación 3D de desensamble
          if (this.installed3DMeshes[slotKey]) {
            const mesh = this.installed3DMeshes[slotKey];
            const startY = mesh.position.y;
            let p = 0;
            const liftAnim = () => {
              p += 0.08;
              mesh.position.y = startY + p * 3;
              if (p < 1) {
                requestAnimationFrame(liftAnim);
              } else {
                this.world3D.scene.remove(mesh);
                delete this.installed3DMeshes[slotKey];
              }
            };
            liftAnim();
          }

          this.renderMachineSlots();
          this.renderStore();
          if (window.showAppToast) {
            window.showAppToast(`${item.oldName} desatornillado y retirado a la bandeja.`, 'info');
          }
        });
      }

      this.machineSlotArea.appendChild(slotBox);
    });
  }

  renderStore() {
    this.storeList.innerHTML = '';
    const comps = this.components[this.currentCase];

    Object.keys(comps).forEach(slotKey => {
      const item = comps[slotKey];
      const card = document.createElement('div');
      card.className = `store-item-card ${item.state === 'new' ? 'purchased' : ''}`;

      card.innerHTML = `
        <div class="store-badge">REPUESTO DE UPGRADE 3D</div>
        <div class="store-item-name">${item.newName}</div>
        <div class="store-item-slot">Para: ${slotKey.toUpperCase()}</div>
        <button class="up-btn mount-btn" ${item.state !== 'empty' ? 'disabled' : ''}>
          ${item.state === 'new' ? '✓ Instalado en 3D' : '＋ Instalar en Máquina 3D'}
        </button>
      `;

      const mountBtn = card.querySelector('.mount-btn');
      if (mountBtn && item.state === 'empty') {
        mountBtn.addEventListener('click', async () => {
          item.state = 'new';
          this.checkTaskCompletion(slotKey);

          // Notificar al backend Python de upgrades
          try {
            await fetch('/api/hw/upgrade/install', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ case: this.currentCase, slot: slotKey })
            });
          } catch(err) {}

          // Animación 3D de inserción del nuevo componente
          if (this.world3D && item.createNewMesh) {
            const mesh = item.createNewMesh();
            this.world3D.animateSlotPlacement(mesh, item.target3DPos, () => {
              this.world3D.flashSlotBox(item.target3DPos, new THREE.Vector3(4, 1, 4), true);
            });
            this.installed3DMeshes[slotKey] = mesh;
          }

          this.renderMachineSlots();
          this.renderStore();
          this.updateBenchmarks();
          if (window.showAppToast) {
            window.showAppToast(`¡Upgrade exitoso! ${item.newName} ensamblado en 3D.`, 'success');
          }
        });
      }

      this.storeList.appendChild(card);
    });
  }

  checkTaskCompletion(slotKey) {
    const o = this.orders[this.currentCase];
    if (this.currentCase === 'desktop') {
      if (slotKey === 'storage') o.tasks[0].done = true;
      if (slotKey === 'ram') o.tasks[1].done = true;
      if (slotKey === 'gpu') o.tasks[2].done = true;
    } else {
      if (slotKey === 'battery') o.tasks[0].done = true;
      if (slotKey === 'ram') o.tasks[1].done = true;
      if (slotKey === 'cooling') o.tasks[2].done = true;
    }
    this.renderTasks();

    if (o.tasks.every(t => t.done)) {
      if (window.showAppToast) {
        window.showAppToast('🎉 ¡Misión cumplida! Computadora potenciada al máximo sin cuellos de botella.', 'success');
      }
      if (this.world3D && this.world3D.controls) {
        this.world3D.controls.autoRotate = true;
      }
    }
  }

  updateBenchmarks() {
    const comps = this.components[this.currentCase];

    if (this.currentCase === 'desktop') {
      let fps = 22;
      let boot = 180;
      let ram = 8;

      if (comps.gpu.state === 'new') fps = 145;
      if (comps.storage.state === 'new') boot = 7;
      if (comps.ram.state === 'new') ram = 32;

      this.benchFps.textContent = `${fps} FPS`;
      this.benchFpsBar.style.width = `${Math.min(100, (fps / 150) * 100)}%`;

      this.benchBoot.textContent = `${boot} segundos`;
      this.benchBootBar.style.width = `${Math.max(5, (1 - boot / 180) * 100)}%`;

      this.benchRam.textContent = `${ram} GB`;
      this.benchRamBar.style.width = `${(ram / 32) * 100}%`;
    } else {
      let bat = comps.battery.state === 'new' ? '6.5 horas' : '12 minutos';
      let boot = 150;
      let ram = comps.ram.state === 'new' ? '16 GB' : '4 GB';

      this.benchFps.textContent = bat;
      this.benchFpsBar.style.width = comps.battery.state === 'new' ? '100%' : '10%';

      this.benchBoot.textContent = `${boot}s`;
      this.benchBootBar.style.width = '20%';

      this.benchRam.textContent = ram;
      this.benchRamBar.style.width = comps.ram.state === 'new' ? '100%' : '25%';
    }
  }

  bindEvents() {
    this.btnCaseDesktop.addEventListener('click', () => this.setCase('desktop'));
    this.btnCaseLaptop.addEventListener('click', () => this.setCase('laptop'));
  }
}

window.HardwareUpgradeSim = HardwareUpgradeSim;
