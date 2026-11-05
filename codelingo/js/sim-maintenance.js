/**
 * SIM-MAINTENANCE.JS - SIMULADOR 4 DEDICADO: LIMPIEZA Y MANTENIMIENTO TÉCNICO 3D
 * Partículas de aire WebGL, giro de ventiladores, desatornillado 3D de disipador,
 * remoción de pasta seca con alcohol isopropílico y aplicación térmica (Estilo pclab.eniun.com)
 */

class HardwareMaintenanceSim {
  constructor() {
    this.activeTool = 'blower'; // blower, brush, screwdriver, alcohol, paste
    this.world3D = null;

    // Estado del mantenimiento
    this.dustLevel = 100; // 100% sucio -> 0% limpio
    this.pasteDryPercent = 100; // 100% pasta seca -> 0% limpia
    this.freshPasteApplied = false;
    this.heatsinkMounted = true;
    this.screwsTightened = true;

    this.coolerMesh = null;
    this.pasteBlobMesh = null;

    this.initDOM();
    this.init3DScene();
    this.bindEvents();
    this.updateMeters();
  }

  initDOM() {
    this.meterDust = document.getElementById('maintDustVal');
    this.meterTemp = document.getElementById('maintTempVal');
    this.meterNoise = document.getElementById('maintNoiseVal');
    this.statusText = document.getElementById('maintStatusText');
    this.canvasArea = document.getElementById('maintCanvasArea');
    this.btnReset = document.getElementById('btnMaintReset');

    // Preparar el área de canvas para renderizado 3D WebGL
    if (this.canvasArea) {
      this.canvasArea.innerHTML = '';
      this.canvasArea.style.width = '100%';
      this.canvasArea.style.height = '420px';
      this.canvasArea.style.position = 'relative';
      this.canvasArea.style.background = '#0e1017';
      this.canvasArea.style.overflow = 'hidden';
    }
  }

  init3DScene() {
    if (!window.Hardware3DWorld) return;

    this.world3D = new Hardware3DWorld('maintCanvasArea', {
      cameraPos: [0, 14, 18],
      lookAt: [0, 0, 0],
      autoRotate: false,
      enableGrid: true
    });

    // Inyectar HUD de control 3D y atajos de cámara
    const hud = document.createElement('div');
    hud.className = 'canvas-3d-hud';
    hud.innerHTML = `
      <button class="hud-3d-btn" id="btnMaintAutoRotate">🔄 Girar 360°</button>
      <button class="hud-3d-btn" id="btnMaintFocusCpu">🔍 Enfocar CPU</button>
      <button class="hud-3d-btn" id="btnMaintGeneralCam">🎯 Vista General</button>
    `;
    this.canvasArea.appendChild(hud);

    document.getElementById('btnMaintAutoRotate').addEventListener('click', () => {
      if (this.world3D.controls) {
        this.world3D.controls.autoRotate = !this.world3D.controls.autoRotate;
        document.getElementById('btnMaintAutoRotate').classList.toggle('active', this.world3D.controls.autoRotate);
      }
    });

    document.getElementById('btnMaintFocusCpu').addEventListener('click', () => {
      this.world3D.focusCamera([0, 6, 7], [0, 1, 3], 600);
    });

    document.getElementById('btnMaintGeneralCam').addEventListener('click', () => {
      this.world3D.focusCamera([0, 14, 18], [0, 0, 0], 600);
    });

    // Cargar la placa madre y los componentes que recibirán mantenimiento
    this.loadMaintScene();
  }

  loadMaintScene() {
    if (!this.world3D) return;
    this.world3D.clearScene();

    // 1. Placa madre base
    this.moboMesh = this.world3D.createMotherboard3D();
    this.world3D.scene.add(this.moboMesh);

    // 2. Procesador en el socket
    this.cpuMesh = this.world3D.createCpu3D();
    this.cpuMesh.position.set(0, 0.35, 3);
    this.world3D.scene.add(this.cpuMesh);

    // 3. Disipador de calor montado sobre el CPU
    if (this.heatsinkMounted) {
      this.coolerMesh = this.world3D.createCooler3D();
      this.coolerMesh.position.set(0, 0.5, 3);
      this.world3D.scene.add(this.coolerMesh);
    }

    // 4. Capa de polvo procedural en 3D
    this.createDustParticles3D();
  }

  createDustParticles3D() {
    if (this.dustParticlesMesh) {
      this.world3D.scene.remove(this.dustParticlesMesh);
    }

    const count = 350;
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 14;
      pos[i * 3 + 1] = 0.4 + Math.random() * 0.8;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 16;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    this.dustMat = new THREE.PointsMaterial({
      color: 0x9c8f78,
      size: 0.22,
      transparent: true,
      opacity: this.dustLevel / 100
    });
    this.dustParticlesMesh = new THREE.Points(geo, this.dustMat);
    this.world3D.scene.add(this.dustParticlesMesh);
  }

  setTool(tool) {
    this.activeTool = tool;
    document.querySelectorAll('.clean-tool-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.tool === tool);
    });

    const toolNames = {
      blower: '💨 Lata de Aire Comprimido (Haz clic en el escenario para soplar polvo con partículas 3D)',
      brush: '🖌️ Brocha Antiestática (Haz clic para barrer circuitos y ranuras)',
      screwdriver: '🪛 Destornillador Magnético (Haz clic sobre el disipador para aflojar sus tornillos y retirarlo)',
      alcohol: '🧽 Alcohol Isopropílico 99.9% (Haz clic sobre el CPU expuesto para disolver la pasta seca)',
      paste: '🧴 Jeringa de Pasta Térmica (Haz clic sobre el CPU limpio para aplicar una gota nueva)'
    };

    this.statusText.innerHTML = `<strong>Herramienta activa:</strong> ${toolNames[tool]}`;
    if (window.showAppToast) {
      window.showAppToast(`Herramienta equipada: ${toolNames[tool].split('(')[0]}`, 'info');
    }
  }

  updateMeters() {
    this.meterDust.textContent = `${this.dustLevel}% (${this.dustLevel === 0 ? 'Impecable' : this.dustLevel < 50 ? 'Poco Polvo' : 'Muy Sucio'})`;
    this.meterDust.className = `clean-meter-val ${this.dustLevel === 0 ? 'cold' : 'hot'}`;

    let temp = 95;
    let noise = 58;

    if (this.dustLevel < 50) { temp -= 15; noise -= 10; }
    if (this.dustLevel === 0) { temp -= 20; noise -= 15; }
    if (this.freshPasteApplied && this.heatsinkMounted) { temp = 31; noise = 19; }

    this.meterTemp.textContent = `${temp}°C (${temp <= 45 ? 'Óptima' : temp < 75 ? 'Media' : 'Recalentado'})`;
    this.meterTemp.className = `clean-meter-val ${temp <= 45 ? 'cold' : 'hot'}`;

    this.meterNoise.textContent = `${noise} dB (${noise <= 25 ? 'Silencioso' : 'Turbina Ruidosa'})`;
  }

  blowAir() {
    if (this.activeTool !== 'blower') return;
    this.notifyBackendTool('blower');

    // Disparar ráfaga de partículas de aire WebGL 3D
    const origin = new THREE.Vector3(2, 6, 6);
    const target = new THREE.Vector3(0, 2, 3);
    this.world3D.createAirBlastParticleSystem(origin, target);

    if (this.world3D.coolerFan) {
      // Hacer girar el ventilador violentamente
      let spinCount = 0;
      const spinInterval = setInterval(() => {
        spinCount++;
        this.world3D.coolerFan.rotation.z += 0.5;
        if (spinCount > 25) clearInterval(spinInterval);
      }, 20);
    }

    if (this.dustLevel > 0) {
      this.dustLevel = Math.max(0, this.dustLevel - 35);
      if (this.dustMat) this.dustMat.opacity = this.dustLevel / 100;
      this.updateMeters();
      if (window.showAppToast) {
        window.showAppToast('💨 ¡Ráfaga de aire a alta presión disparada! Ventiladores girando y polvo expulsado.', 'success');
      }
    }
  }

  sweepBrush() {
    if (this.activeTool !== 'brush') return;

    if (this.dustLevel > 0) {
      this.dustLevel = Math.max(0, this.dustLevel - 40);
      if (this.dustMat) this.dustMat.opacity = this.dustLevel / 100;
      this.updateMeters();
      if (window.showAppToast) {
        window.showAppToast('🖌️ Brocha antiestática pasada por ranuras y pistas. Pelusa barrida.', 'success');
      }
    }
  }

  toggleHeatsink() {
    if (this.activeTool === 'screwdriver') {
      this.screwsTightened = !this.screwsTightened;
      if (!this.screwsTightened) {
        // Desmontar el disipador en 3D
        if (this.coolerMesh) {
          const startY = this.coolerMesh.position.y;
          let p = 0;
          const liftAnim = () => {
            p += 0.08;
            this.coolerMesh.position.y = startY + p * 5;
            if (p < 1) {
              requestAnimationFrame(liftAnim);
            } else {
              this.world3D.scene.remove(this.coolerMesh);
              this.heatsinkMounted = false;
              this.world3D.focusCamera([0, 5, 6], [0, 0.4, 3], 600);
            }
          };
          liftAnim();
        }
        if (window.showAppToast) {
          window.showAppToast('🪛 Tornillos en cruz aflojados. Disipador levantado. Procesador visible.', 'info');
        }
      } else {
        // Volver a montar el disipador
        this.heatsinkMounted = true;
        this.coolerMesh = this.world3D.createCooler3D();
        this.world3D.animateSlotPlacement(this.coolerMesh, new THREE.Vector3(0, 0.5, 3));
        this.updateMeters();
        if (window.showAppToast) {
          window.showAppToast('🪛 Disipador colocado y tornillos apretados en cruz firmemente.', 'success');
        }
      }
    }
  }

  cleanWithAlcohol() {
    if (this.activeTool !== 'alcohol') return;

    if (this.heatsinkMounted) {
      if (window.showAppToast) {
        window.showAppToast('Primero debes desatornillar y levantar el disipador con el destornillador.', 'error');
      }
      return;
    }

    if (this.pasteDryPercent > 0) {
      this.pasteDryPercent = 0;
      if (this.cpuMesh) {
        this.cpuMesh.traverse(child => {
          if (child.material && child.material === this.world3D.materials.nickelShiny) {
            child.material.metalness = 0.95;
            child.material.roughness = 0.15;
          }
        });
      }
      this.updateMeters();
      if (window.showAppToast) {
        window.showAppToast('🧽 Pasta térmica seca disuelta al 100%. El IHS quedó brillante con acabado espejo.', 'success');
      }
    }
  }

  applyFreshThermalPaste() {
    if (this.activeTool !== 'paste') return;

    if (this.heatsinkMounted) {
      if (window.showAppToast) {
        window.showAppToast('Retira el disipador antes de aplicar la pasta.', 'error');
      }
      return;
    }

    if (this.pasteDryPercent > 0) {
      if (window.showAppToast) {
        window.showAppToast('¡Error de mantenimiento! No apliques pasta nueva sobre la pasta vieja reseca. Límpiala primero con alcohol isopropílico.', 'error');
      }
      return;
    }

    if (!this.freshPasteApplied) {
      this.freshPasteApplied = true;
      this.pasteBlobMesh = this.world3D.createThermalPasteBlob(new THREE.Vector3(0, 0.5, 3));
      this.updateMeters();
      if (window.showAppToast) {
        window.showAppToast('🧴 Gota perfecta de pasta térmica de alta conductividad aplicada sobre el procesador.', 'success');
      }
    }
  }

  reset() {
    this.dustLevel = 100;
    this.pasteDryPercent = 100;
    this.freshPasteApplied = false;
    this.heatsinkMounted = true;
    this.screwsTightened = true;
    this.loadMaintScene();
    this.updateMeters();
    if (window.showAppToast) {
      window.showAppToast('Mantenimiento 3D reiniciado al estado inicial sucio.', 'info');
    }
  }

  bindEvents() {
    document.querySelectorAll('.clean-tool-btn').forEach(btn => {
      btn.addEventListener('click', () => this.setTool(btn.dataset.tool));
    });

    if (this.btnReset) this.btnReset.addEventListener('click', () => this.reset());

    // Interacción al hacer clic en el escenario 3D
    if (this.canvasArea) {
      this.canvasArea.addEventListener('click', () => {
        if (this.activeTool === 'blower') {
          this.blowAir();
        } else if (this.activeTool === 'brush') {
          this.sweepBrush();
        } else if (this.activeTool === 'screwdriver') {
          this.toggleHeatsink();
        } else if (this.activeTool === 'alcohol') {
          this.cleanWithAlcohol();
        } else if (this.activeTool === 'paste') {
          this.applyFreshThermalPaste();
        }
      });
    }
  }
}

window.HardwareMaintenanceSim = HardwareMaintenanceSim;
