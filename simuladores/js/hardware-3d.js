/**
 * HARDWARE-3D.JS - MOTOR DE GRÁFICOS 3D PROCEDURALES CON THREE.JS
 * Modelos 3D interactivos hiperrealistas para placas madre, procesadores,
 * memorias RAM, GPUs, coolers, zócalos mecánicos, herramientas de taller
 * y animación de montaje al estilo de pclab.eniun.com
 */

class Hardware3DWorld {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.warn(`Contenedor 3D no encontrado: #${containerId}`);
      return;
    }

    this.options = Object.assign({
      cameraPos: [0, 18, 22],
      lookAt: [0, 0, 0],
      autoRotate: false,
      enableGrid: true,
      enableShadows: true,
      backgroundColor: 0x0f1118
    }, options);

    this.models = {};
    this.animations = [];
    this.initScene();
    this.initLights();
    this.initTextures();
    this.initMaterials();
    this.bindResize();
    this.animate();
  }

  initScene() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.options.backgroundColor);
    this.scene.fog = new THREE.FogExp2(this.options.backgroundColor, 0.015);

    const w = this.container.clientWidth || 600;
    const h = this.container.clientHeight || 400;

    this.camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
    this.camera.position.set(...this.options.cameraPos);
    this.camera.lookAt(...this.options.lookAt);

    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    this.renderer.setSize(w, h);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    if (this.options.enableShadows) {
      this.renderer.shadowMap.enabled = true;
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;

    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // OrbitControls para rotación 360°, zoom y paneo táctil en Android y Desktop
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.08;
      this.controls.maxPolarAngle = Math.PI / 2 + 0.05; // No ir por debajo del suelo
      this.controls.minDistance = 2;
      this.controls.maxDistance = 60;
      this.controls.autoRotate = this.options.autoRotate;
      this.controls.autoRotateSpeed = 1.0;
    }

    // Grid del banco de trabajo estilo laboratorio
    if (this.options.enableGrid) {
      const grid = new THREE.GridHelper(40, 40, 0x007acc, 0x1e2436);
      grid.position.y = -0.05;
      this.scene.add(grid);

      // Suelo reflectivo sutil
      const floorGeo = new THREE.PlaneGeometry(100, 100);
      const floorMat = new THREE.MeshStandardMaterial({
        color: 0x0d0f14,
        roughness: 0.85,
        metalness: 0.2
      });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.rotation.x = -Math.PI / 2;
      floor.position.y = -0.06;
      floor.receiveShadow = true;
      this.scene.add(floor);
    }
  }

  initLights() {
    // Luz ambiental suave para no dejar sombras negras
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    this.scene.add(ambientLight);

    // Luz principal de estudio (Key Light)
    const keyLight = new THREE.DirectionalLight(0xffffff, 1.4);
    keyLight.position.set(12, 24, 14);
    keyLight.castShadow = this.options.enableShadows;
    if (keyLight.castShadow) {
      keyLight.shadow.mapSize.width = 1024;
      keyLight.shadow.mapSize.height = 1024;
      keyLight.shadow.camera.near = 0.5;
      keyLight.shadow.camera.far = 70;
      keyLight.shadow.camera.left = -18;
      keyLight.shadow.camera.right = 18;
      keyLight.shadow.camera.top = 18;
      keyLight.shadow.camera.bottom = -18;
      keyLight.shadow.bias = -0.0005;
    }
    this.scene.add(keyLight);

    // Luz de relleno azul frío estilo gamer (Fill / Rim Light)
    const rimLight = new THREE.DirectionalLight(0x00d2ff, 0.9);
    rimLight.position.set(-15, 12, -10);
    this.scene.add(rimLight);

    // Luz cálida sutil en el lado opuesto
    const warmLight = new THREE.DirectionalLight(0xffb703, 0.45);
    warmLight.position.set(10, 8, -12);
    this.scene.add(warmLight);
  }

  // Generador de texturas de alta resolución mediante Canvas 2D
  initTextures() {
    this.textures = {
      pcbTraces: this.createPCBTexture('#0a1b12', '#143825', '#c8963e'),
      pcbTracesDark: this.createPCBTexture('#101216', '#1a1e27', '#007acc'),
      cpuIHS: this.createCpuIHSTexture(),
      ramSticker: this.createRamStickerTexture(),
      fanBlades: this.createFanBladesTexture(),
      dustOverlay: this.createDustTexture()
    };
  }

  createPCBTexture(bg, traceColor, padColor) {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d');

    // Fondo PCB
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, 1024, 1024);

    // Pistas de cobre impresas
    ctx.strokeStyle = traceColor;
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i < 180; i++) {
      const x1 = Math.random() * 1024;
      const y1 = Math.random() * 1024;
      const len = 40 + Math.random() * 120;
      const angle = (Math.floor(Math.random() * 4) * 45) * (Math.PI / 180);
      ctx.moveTo(x1, y1);
      ctx.lineTo(x1 + Math.cos(angle) * len, y1 + Math.sin(angle) * len);
    }
    ctx.stroke();

    // Puntos de soldadura y vias doradas
    ctx.fillStyle = padColor;
    for (let i = 0; i < 240; i++) {
      ctx.beginPath();
      ctx.arc(Math.random() * 1024, Math.random() * 1024, 2 + Math.random() * 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Serigrafía de componentes
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.font = 'bold 14px monospace';
    ctx.fillText('ENIUN-PRO Z790 DDR5', 60, 80);
    ctx.fillText('LGA1700 SOCKET', 350, 420);
    ctx.fillText('PCIe 5.0 x16', 120, 680);
    ctx.fillText('M.2 NVMe PCIe 4.0', 420, 560);
    ctx.fillText('DIMM_A1 DIMM_A2 DIMM_B1 DIMM_B2', 680, 260);

    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    return texture;
  }

  createCpuIHSTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Acabado metálico con degradado
    const grad = ctx.createLinearGradient(0, 0, 512, 512);
    grad.addColorStop(0, '#d8dbe2');
    grad.addColorStop(0.5, '#f4f5f7');
    grad.addColorStop(1, '#b5bac9');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 512, 512);

    // Marco exterior biselado
    ctx.strokeStyle = '#8a92a6';
    ctx.lineWidth = 12;
    ctx.strokeRect(10, 10, 492, 492);

    // Grabado láser Intel Core i9
    ctx.fillStyle = '#2c3345';
    ctx.textAlign = 'center';
    ctx.font = 'bold 32px sans-serif';
    ctx.fillText('intel.', 256, 150);

    ctx.font = 'bold 44px sans-serif';
    ctx.fillText('CORE i9', 256, 210);

    ctx.font = '600 24px monospace';
    ctx.fillText('i9-14900K', 256, 260);
    ctx.fillText('SRN48 3.20GHz', 256, 300);
    ctx.fillText('MALAY L324F918', 256, 340);

    // Código QR en miniatura
    ctx.fillRect(216, 370, 80, 80);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(226, 380, 60, 60);
    ctx.fillStyle = '#2c3345';
    ctx.fillRect(236, 390, 40, 40);

    // Triángulo dorado de alineación en esquina inferior izquierda
    ctx.fillStyle = '#f5b700';
    ctx.beginPath();
    ctx.moveTo(35, 480);
    ctx.lineTo(85, 480);
    ctx.lineTo(35, 430);
    ctx.closePath();
    ctx.fill();

    return new THREE.CanvasTexture(canvas);
  }

  createRamStickerTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#161922';
    ctx.fillRect(0, 0, 512, 128);

    ctx.strokeStyle = '#007acc';
    ctx.lineWidth = 4;
    ctx.strokeRect(4, 4, 504, 120);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 24px sans-serif';
    ctx.fillText('CORSAIR VENGEANCE', 20, 45);

    ctx.fillStyle = '#00d2ff';
    ctx.font = 'bold 18px monospace';
    ctx.fillText('DDR5 32GB (2x16GB) 6000MHz CL30', 20, 80);
    ctx.fillText('1.35V XMP 3.0 READY', 20, 108);

    return new THREE.CanvasTexture(canvas);
  }

  createFanBladesTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 256, 256);

    ctx.fillStyle = '#1e222d';
    ctx.beginPath();
    ctx.arc(128, 128, 45, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#11141c';
    for (let i = 0; i < 9; i++) {
      ctx.save();
      ctx.translate(128, 128);
      ctx.rotate((i * 40) * Math.PI / 180);
      ctx.beginPath();
      ctx.ellipse(55, 0, 45, 16, Math.PI / 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    return new THREE.CanvasTexture(canvas);
  }

  createDustTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 512, 512);

    ctx.fillStyle = 'rgba(160, 140, 110, 0.65)';
    for (let i = 0; i < 1800; i++) {
      ctx.beginPath();
      ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 3.5, 0, Math.PI * 2);
      ctx.fill();
    }
    return new THREE.CanvasTexture(canvas);
  }

  initMaterials() {
    this.materials = {
      pcb: new THREE.MeshStandardMaterial({
        map: this.textures.pcbTraces,
        roughness: 0.6,
        metalness: 0.2
      }),
      pcbDark: new THREE.MeshStandardMaterial({
        map: this.textures.pcbTracesDark,
        roughness: 0.5,
        metalness: 0.3
      }),
      nickelShiny: new THREE.MeshStandardMaterial({
        map: this.textures.cpuIHS,
        roughness: 0.25,
        metalness: 0.85
      }),
      goldContacts: new THREE.MeshStandardMaterial({
        color: 0xf5b700,
        roughness: 0.2,
        metalness: 0.95
      }),
      copperPipes: new THREE.MeshStandardMaterial({
        color: 0xc86432,
        roughness: 0.3,
        metalness: 0.9
      }),
      aluminumHeatsink: new THREE.MeshStandardMaterial({
        color: 0x222630,
        roughness: 0.4,
        metalness: 0.8
      }),
      blackPlastic: new THREE.MeshStandardMaterial({
        color: 0x14161d,
        roughness: 0.7,
        metalness: 0.1
      }),
      rgbGlow: new THREE.MeshStandardMaterial({
        color: 0x00d2ff,
        emissive: 0x007acc,
        emissiveIntensity: 0.9,
        roughness: 0.2,
        metalness: 0.1
      }),
      glassCase: new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.35,
        roughness: 0.1,
        metalness: 0.1,
        transmission: 0.75,
        ior: 1.5
      }),
      dryThermalPaste: new THREE.MeshStandardMaterial({
        color: 0x6e685f,
        roughness: 0.95,
        metalness: 0.05
      }),
      freshThermalPaste: new THREE.MeshStandardMaterial({
        color: 0x8a9ba8,
        roughness: 0.3,
        metalness: 0.4
      }),
      slotHighlight: new THREE.MeshStandardMaterial({
        color: 0x27c93f,
        emissive: 0x27c93f,
        emissiveIntensity: 0.6,
        transparent: true,
        opacity: 0.65
      }),
      slotError: new THREE.MeshStandardMaterial({
        color: 0xf14c4c,
        emissive: 0xf14c4c,
        emissiveIntensity: 0.8,
        transparent: true,
        opacity: 0.75
      })
    };
  }

  // ==========================================================================
  // CONSTRUCTORES PROCEDURALES DE MODELOS 3D
  // ==========================================================================

  /**
   * Construye una Placa Base ATX Gamer completa en 3D
   */
  createMotherboard3D() {
    const moboGroup = new THREE.Group();
    moboGroup.name = 'motherboard';

    // 1. Placa PCB principal
    const pcbGeo = new THREE.BoxGeometry(15, 0.35, 19);
    const pcbMesh = new THREE.Mesh(pcbGeo, this.materials.pcb);
    pcbMesh.receiveShadow = true;
    pcbMesh.castShadow = true;
    moboGroup.add(pcbMesh);

    // Orificios metálicos para tornillos de sujeción
    const holePositions = [
      [-6.5, 8.5], [0, 8.5], [6.5, 8.5],
      [-6.5, 0], [0, 0], [6.5, 0],
      [-6.5, -8.5], [0, -8.5], [6.5, -8.5]
    ];
    holePositions.forEach(([x, z]) => {
      const ringGeo = new THREE.RingGeometry(0.18, 0.4, 16);
      const ring = new THREE.Mesh(ringGeo, this.materials.goldContacts);
      ring.rotation.x = -Math.PI / 2;
      ring.position.set(x, 0.18, z);
      moboGroup.add(ring);
    });

    // 2. Socket del Procesador LGA1700
    const socketGroup = new THREE.Group();
    socketGroup.name = 'socket_cpu';
    socketGroup.position.set(0, 0.2, 3);

    // Base del socket con pines
    const socketBase = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 0.25, 4.2),
      this.materials.blackPlastic
    );
    socketBase.receiveShadow = true;
    socketGroup.add(socketBase);

    // Malla de pines dorados central
    const pinGrid = new THREE.Mesh(
      new THREE.PlaneGeometry(3.2, 3.2),
      this.materials.goldContacts
    );
    pinGrid.rotation.x = -Math.PI / 2;
    pinGrid.position.y = 0.13;
    socketGroup.add(pinGrid);

    // Marco metálico perimetral y palanca de sujeción (lever)
    const socketFrame = new THREE.Mesh(
      new THREE.BoxGeometry(4.4, 0.15, 4.4),
      this.materials.aluminumHeatsink
    );
    socketFrame.position.y = 0.1;
    socketGroup.add(socketFrame);

    const lever = new THREE.Mesh(
      new THREE.CylinderGeometry(0.06, 0.06, 4.6),
      this.materials.nickelShiny
    );
    lever.rotation.x = Math.PI / 2;
    lever.position.set(2.35, 0.18, 0);
    socketGroup.add(lever);

    moboGroup.add(socketGroup);

    // 3. Disipadores VRM masivos de aluminio cepillado
    const vrmLeft = new THREE.Mesh(
      new THREE.BoxGeometry(1.6, 2.2, 6.5),
      this.materials.aluminumHeatsink
    );
    vrmLeft.position.set(-3.2, 1.1, 3.2);
    vrmLeft.castShadow = true;
    moboGroup.add(vrmLeft);

    const vrmTop = new THREE.Mesh(
      new THREE.BoxGeometry(5.2, 1.8, 1.4),
      this.materials.aluminumHeatsink
    );
    vrmTop.position.set(0.6, 0.9, 6.2);
    vrmTop.castShadow = true;
    moboGroup.add(vrmTop);

    // 4. Ranuras DIMM para memoria RAM (4 ranuras Dual-Channel)
    const ramSlotsGroup = new THREE.Group();
    ramSlotsGroup.name = 'slot_ram_group';
    ramSlotsGroup.position.set(4.2, 0.2, 3.0);

    for (let i = 0; i < 4; i++) {
      const zOffset = (i - 1.5) * 0.9;
      const slotBar = new THREE.Mesh(
        new THREE.BoxGeometry(0.35, 0.6, 5.5),
        this.materials.blackPlastic
      );
      slotBar.position.set(zOffset, 0.15, 0);

      // Contactos dorados centrales
      const slotPin = new THREE.Mesh(
        new THREE.BoxGeometry(0.08, 0.2, 5.2),
        this.materials.goldContacts
      );
      slotPin.position.set(zOffset, 0.35, 0);

      // Clips de bloqueo en ambos extremos
      const clipTop = new THREE.Mesh(
        new THREE.BoxGeometry(0.38, 0.45, 0.3),
        this.materials.nickelShiny
      );
      clipTop.position.set(zOffset, 0.3, 2.85);

      const clipBottom = clipTop.clone();
      clipBottom.position.set(zOffset, 0.3, -2.85);

      ramSlotsGroup.add(slotBar, slotPin, clipTop, clipBottom);
    }
    moboGroup.add(ramSlotsGroup);

    // 5. Ranuras PCIe 5.0 x16 para tarjeta gráfica
    const pcieGroup = new THREE.Group();
    pcieGroup.name = 'slot_gpu';
    pcieGroup.position.set(-0.5, 0.2, -3.2);

    const pcieSlot = new THREE.Mesh(
      new THREE.BoxGeometry(8.5, 0.55, 0.55),
      this.materials.aluminumHeatsink // Blindaje metálico Armor
    );
    pcieSlot.position.set(0, 0.15, 0);

    const pcieClip = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 0.4, 0.7),
      this.materials.blackPlastic
    );
    pcieClip.position.set(4.4, 0.15, 0);

    pcieGroup.add(pcieSlot, pcieClip);
    moboGroup.add(pcieGroup);

    // Segunda ranura PCIe x4 inferior
    const pcie2 = pcieSlot.clone();
    pcie2.position.set(-0.5, 0.35, -7.0);
    moboGroup.add(pcie2);

    // 6. Ranuras M.2 NVMe con disipador pasivo
    const m2Heatsink = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 0.3, 1.2),
      this.materials.aluminumHeatsink
    );
    m2Heatsink.position.set(0, 0.3, -1.2);
    m2Heatsink.name = 'slot_m2';
    moboGroup.add(m2Heatsink);

    // 7. Panel I/O trasero con puertos USB, HDMI, LAN
    const ioShield = new THREE.Mesh(
      new THREE.BoxGeometry(1.4, 2.4, 8.5),
      this.materials.nickelShiny
    );
    ioShield.position.set(-6.8, 1.2, 4.0);
    moboGroup.add(ioShield);

    // 8. Capacitores cilíndricos japoneses de audio y VRM
    for (let c = 0; c < 12; c++) {
      const cap = new THREE.Mesh(
        new THREE.CylinderGeometry(0.25, 0.25, 0.6, 12),
        c % 2 === 0 ? this.materials.goldContacts : this.materials.nickelShiny
      );
      cap.position.set(-5.5 + (c % 4) * 0.6, 0.3, -5 - Math.floor(c / 4) * 0.8);
      moboGroup.add(cap);
    }

    // 9. Conector ATX 24 pines lateral
    const atx24 = new THREE.Mesh(
      new THREE.BoxGeometry(0.8, 0.8, 4.2),
      this.materials.blackPlastic
    );
    atx24.position.set(6.8, 0.4, 2.5);
    moboGroup.add(atx24);

    return moboGroup;
  }

  /**
   * Construye un Procesador Intel Core i9 3D con IHS metálico pulido y sustrato
   */
  createCpu3D() {
    const cpuGroup = new THREE.Group();
    cpuGroup.name = 'cpu_part';

    // Sustrato PCB verde inferior
    const substrate = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 0.12, 3.6),
      new THREE.MeshStandardMaterial({ color: 0x184428, roughness: 0.4 })
    );
    substrate.castShadow = true;
    cpuGroup.add(substrate);

    // IHS (Integrated Heat Spreader) metálico con grabado láser
    const ihs = new THREE.Mesh(
      new THREE.BoxGeometry(3.2, 0.18, 3.2),
      this.materials.nickelShiny
    );
    ihs.position.y = 0.12;
    ihs.castShadow = true;
    cpuGroup.add(ihs);

    // Triángulo dorado de esquina inferior izquierda
    const tri = new THREE.Mesh(
      new THREE.BufferGeometry(),
      this.materials.goldContacts
    );
    const vertices = new Float32Array([
      -1.7, 0.07, 1.7,
      -1.3, 0.07, 1.7,
      -1.7, 0.07, 1.3
    ]);
    tri.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    const triMesh = new THREE.Mesh(tri, this.materials.goldContacts);
    cpuGroup.add(triMesh);

    // Contactos dorados inferiores (LGA pads)
    const bottomPads = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 3.4),
      this.materials.goldContacts
    );
    bottomPads.rotation.x = Math.PI / 2;
    bottomPads.position.y = -0.07;
    cpuGroup.add(bottomPads);

    return cpuGroup;
  }

  /**
   * Construye un Módulo de Memoria RAM DDR5 Gamer con barra RGB
   */
  createRamDDR53D() {
    const ramGroup = new THREE.Group();
    ramGroup.name = 'ram_part';

    // PCB de la memoria
    const pcb = new THREE.Mesh(
      new THREE.BoxGeometry(0.12, 1.8, 5.2),
      new THREE.MeshStandardMaterial({ color: 0x11141c, roughness: 0.6 })
    );
    pcb.castShadow = true;
    ramGroup.add(pcb);

    // Contactos dorados inferiores con muesca central
    const pins = new THREE.Mesh(
      new THREE.BoxGeometry(0.14, 0.25, 5.0),
      this.materials.goldContacts
    );
    pins.position.y = -0.9;
    ramGroup.add(pins);

    // Disipador de aluminio negro con cortes angulares
    const spreader = new THREE.Mesh(
      new THREE.BoxGeometry(0.3, 1.5, 5.2),
      this.materials.aluminumHeatsink
    );
    spreader.position.y = 0.1;
    spreader.castShadow = true;
    ramGroup.add(spreader);

    // Sticker de especificaciones
    const sticker = new THREE.Mesh(
      new THREE.PlaneGeometry(4.0, 0.8),
      new THREE.MeshBasicMaterial({ map: this.textures.ramSticker, transparent: true })
    );
    sticker.position.set(0.16, 0.05, 0);
    sticker.rotation.y = Math.PI / 2;
    ramGroup.add(sticker);

    // Barra superior RGB difusa con brillo neón
    const rgbBar = new THREE.Mesh(
      new THREE.BoxGeometry(0.32, 0.28, 5.2),
      this.materials.rgbGlow
    );
    rgbBar.position.y = 0.95;
    ramGroup.add(rgbBar);

    return ramGroup;
  }

  /**
   * Construye un Módulo de Memoria RAM SO-DIMM (Laptop) a 45°
   */
  createRamSODIMM3D() {
    const soGroup = new THREE.Group();
    soGroup.name = 'sodimm_part';

    // PCB compacto (la mitad de largo de una RAM de escritorio)
    const pcb = new THREE.Mesh(
      new THREE.BoxGeometry(0.1, 1.4, 2.8),
      new THREE.MeshStandardMaterial({ color: 0x1a452a, roughness: 0.5 })
    );
    soGroup.add(pcb);

    // Chips de memoria BGA soldados negros
    for (let c = 0; c < 4; c++) {
      const chip = new THREE.Mesh(
        new THREE.BoxGeometry(0.16, 0.45, 0.45),
        this.materials.blackPlastic
      );
      chip.position.set(0.06, 0.1, (c - 1.5) * 0.65);
      soGroup.add(chip);
    }

    // Contactos dorados con muesca
    const pins = new THREE.Mesh(
      new THREE.BoxGeometry(0.12, 0.22, 2.7),
      this.materials.goldContacts
    );
    pins.position.y = -0.7;
    soGroup.add(pins);

    return soGroup;
  }

  /**
   * Construye una Tarjeta Gráfica NVIDIA RTX 4080 Super en 3D
   */
  createGPU3D() {
    const gpuGroup = new THREE.Group();
    gpuGroup.name = 'gpu_part';

    // Backplate de metal posterior
    const backplate = new THREE.Mesh(
      new THREE.BoxGeometry(11.5, 0.2, 4.5),
      this.materials.aluminumHeatsink
    );
    backplate.position.y = 0.1;
    backplate.castShadow = true;
    gpuGroup.add(backplate);

    // Bloque denso de aletas de disipación de aluminio
    const fins = new THREE.Mesh(
      new THREE.BoxGeometry(11.0, 1.6, 4.2),
      new THREE.MeshStandardMaterial({ color: 0x5a6275, roughness: 0.35, metalness: 0.7 })
    );
    fins.position.y = -0.8;
    gpuGroup.add(fins);

    // Heatpipes de cobre que atraviesan las aletas
    for (let p = 0; p < 4; p++) {
      const pipe = new THREE.Mesh(
        new THREE.CylinderGeometry(0.15, 0.15, 11.2, 12),
        this.materials.copperPipes
      );
      pipe.rotation.z = Math.PI / 2;
      pipe.position.set(0, -0.8, (p - 1.5) * 1.0);
      gpuGroup.add(pipe);
    }

    // Carcasa exterior (Shroud)
    const shroud = new THREE.Mesh(
      new THREE.BoxGeometry(11.6, 0.4, 4.6),
      this.materials.blackPlastic
    );
    shroud.position.y = -1.8;
    gpuGroup.add(shroud);

    // 3 Ventiladores axiales con aspas detalladas
    this.gpuFans = [];
    for (let f = 0; f < 3; f++) {
      const fanHub = new THREE.Mesh(
        new THREE.CylinderGeometry(0.6, 0.6, 0.2, 16),
        this.materials.aluminumHeatsink
      );
      fanHub.position.set((f - 1) * 3.6, -1.85, 0);

      // Aspas
      const blades = new THREE.Mesh(
        new THREE.PlaneGeometry(2.8, 2.8),
        new THREE.MeshBasicMaterial({ map: this.textures.fanBlades, transparent: true, side: THREE.DoubleSide })
      );
      blades.rotation.x = Math.PI / 2;
      blades.position.set((f - 1) * 3.6, -1.87, 0);

      gpuGroup.add(fanHub, blades);
      this.gpuFans.push(blades);
    }

    // Conector PCIe x16 dorado inferior
    const pcieEdge = new THREE.Mesh(
      new THREE.BoxGeometry(7.5, 0.5, 0.15),
      this.materials.goldContacts
    );
    pcieEdge.position.set(-1.0, 0.4, 2.3);
    gpuGroup.add(pcieEdge);

    // Soporte metálico I/O Bracket trasero con puertos
    const bracket = new THREE.Mesh(
      new THREE.BoxGeometry(0.15, 3.2, 4.8),
      this.materials.nickelShiny
    );
    bracket.position.set(-5.8, -0.6, 0);
    gpuGroup.add(bracket);

    // Logo GeForce RTX RGB lateral
    const logoRgb = new THREE.Mesh(
      new THREE.BoxGeometry(3.5, 0.4, 0.1),
      this.materials.rgbGlow
    );
    logoRgb.position.set(0, -0.8, 2.3);
    gpuGroup.add(logoRgb);

    return gpuGroup;
  }

  /**
   * Construye un Disco SSD M.2 NVMe 3D
   */
  createM2SSD3D() {
    const m2Group = new THREE.Group();
    m2Group.name = 'm2_ssd_part';

    // PCB factor 2280 negro
    const pcb = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 0.1, 1.2),
      this.materials.pcbDark
    );
    m2Group.add(pcb);

    // Controlador y memoria NAND Flash
    const nand1 = new THREE.Mesh(
      new THREE.BoxGeometry(0.9, 0.12, 0.9),
      this.materials.blackPlastic
    );
    nand1.position.set(0.6, 0.08, 0);

    const nand2 = nand1.clone();
    nand2.position.set(1.6, 0.08, 0);

    const controller = new THREE.Mesh(
      new THREE.BoxGeometry(0.7, 0.15, 0.7),
      this.materials.nickelShiny
    );
    controller.position.set(-0.6, 0.08, 0);

    // Conector dorado M-Key
    const mKeyPins = new THREE.Mesh(
      new THREE.BoxGeometry(0.4, 0.12, 1.1),
      this.materials.goldContacts
    );
    mKeyPins.position.set(-2.0, 0, 0);

    m2Group.add(nand1, nand2, controller, mKeyPins);
    return m2Group;
  }

  /**
   * Construye un Disipador de Aire de Torre CPU con Ventilador y Heatpipes
   */
  createCooler3D() {
    const coolerGroup = new THREE.Group();
    coolerGroup.name = 'cooler_part';

    // Base de contacto de cobre con el CPU
    const copperBase = new THREE.Mesh(
      new THREE.BoxGeometry(3.4, 0.35, 3.4),
      this.materials.copperPipes
    );
    copperBase.position.y = 0.2;
    coolerGroup.add(copperBase);

    // 4 Heatpipes dobles en forma de U
    for (let h = 0; h < 4; h++) {
      const hp = new THREE.Mesh(
        new THREE.CylinderGeometry(0.2, 0.2, 6.5, 12),
        this.materials.copperPipes
      );
      hp.position.set((h - 1.5) * 0.8, 3.4, 0);
      coolerGroup.add(hp);
    }

    // Torre de aletas de aluminio radiadoras
    const finTower = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 4.5, 2.6),
      new THREE.MeshStandardMaterial({ color: 0x444b5c, roughness: 0.3, metalness: 0.8 })
    );
    finTower.position.set(0, 3.8, 0);
    finTower.castShadow = true;
    coolerGroup.add(finTower);

    // Ventilador frontal de 120mm
    const fanFrame = new THREE.Mesh(
      new THREE.BoxGeometry(4.0, 4.0, 0.8),
      this.materials.blackPlastic
    );
    fanFrame.position.set(0, 3.8, 1.7);
    coolerGroup.add(fanFrame);

    this.coolerFan = new THREE.Mesh(
      new THREE.PlaneGeometry(3.6, 3.6),
      new THREE.MeshBasicMaterial({ map: this.textures.fanBlades, transparent: true, side: THREE.DoubleSide })
    );
    this.coolerFan.position.set(0, 3.8, 2.12);
    coolerGroup.add(this.coolerFan);

    return coolerGroup;
  }

  /**
   * Construye el Sistema Térmico de Notebook (Heatpipe plano de cobre & Turbina Blower)
   */
  createLaptopHeatpipe3D() {
    const lapCoolingGroup = new THREE.Group();
    lapCoolingGroup.name = 'laptop_cooling_part';

    // Placa de contacto del procesador
    const cpuContact = new THREE.Mesh(
      new THREE.BoxGeometry(2.2, 0.15, 2.2),
      this.materials.copperPipes
    );
    cpuContact.position.set(-2, 0.1, 0);
    lapCoolingGroup.add(cpuContact);

    // 4 Tornillos diagonales numerados 1, 2, 3, 4
    const screwPositions = [[-2.8, -0.8], [-1.2, -0.8], [-1.2, 0.8], [-2.8, 0.8]];
    screwPositions.forEach(([x, z]) => {
      const screw = new THREE.Mesh(
        new THREE.CylinderGeometry(0.18, 0.18, 0.25, 12),
        this.materials.nickelShiny
      );
      screw.position.set(x, 0.2, z);
      lapCoolingGroup.add(screw);
    });

    // Tubo plano de cobre curvado (Heatpipe)
    const pipe = new THREE.Mesh(
      new THREE.BoxGeometry(4.5, 0.12, 0.6),
      this.materials.copperPipes
    );
    pipe.position.set(0.5, 0.18, 0.5);
    lapCoolingGroup.add(pipe);

    // Turbina centrífuga Blower negra
    const blower = new THREE.Mesh(
      new THREE.CylinderGeometry(1.6, 1.6, 0.8, 24),
      this.materials.blackPlastic
    );
    blower.position.set(3.2, 0.45, 0.8);
    lapCoolingGroup.add(blower);

    // Rejilla de aletas de escape de calor
    const radiatorGrill = new THREE.Mesh(
      new THREE.BoxGeometry(0.8, 0.7, 1.8),
      this.materials.copperPipes
    );
    radiatorGrill.position.set(4.6, 0.45, 0.8);
    lapCoolingGroup.add(radiatorGrill);

    return lapCoolingGroup;
  }

  /**
   * Construye la Batería Extraíble de Laptop 3D
   */
  createLaptopBattery3D() {
    const batGroup = new THREE.Group();
    batGroup.name = 'battery_part';

    // Cuerpo plástico estriado de la batería
    const body = new THREE.Mesh(
      new THREE.BoxGeometry(9.0, 1.1, 2.2),
      this.materials.blackPlastic
    );
    body.castShadow = true;
    batGroup.add(body);

    // Conector terminal de pines
    const pins = new THREE.Mesh(
      new THREE.BoxGeometry(1.4, 0.4, 0.2),
      this.materials.goldContacts
    );
    pins.position.set(2.8, 0, 1.15);
    batGroup.add(pins);

    // Pestillos de traba
    const latch1 = new THREE.Mesh(
      new THREE.BoxGeometry(0.6, 0.3, 0.2),
      new THREE.MeshStandardMaterial({ color: 0xe76f51, roughness: 0.5 })
    );
    latch1.position.set(-3.2, 0.3, -1.15);
    batGroup.add(latch1);

    return batGroup;
  }

  // ==========================================================================
  // HERRAMIENTAS Y EFECTOS DE TALLER EN 3D
  // ==========================================================================

  /**
   * Genera el efecto de ráfaga de aire comprimido con partículas 3D
   */
  createAirBlastParticleSystem(origin, target) {
    const particleCount = 250;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const velocities = [];

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = origin.x + (Math.random() - 0.5) * 0.4;
      positions[i * 3 + 1] = origin.y + (Math.random() - 0.5) * 0.4;
      positions[i * 3 + 2] = origin.z + (Math.random() - 0.5) * 0.4;

      const dir = new THREE.Vector3().subVectors(target, origin).normalize();
      dir.x += (Math.random() - 0.5) * 0.4;
      dir.y += (Math.random() - 0.5) * 0.4;
      dir.z += (Math.random() - 0.5) * 0.4;
      velocities.push(dir.multiplyScalar(0.4 + Math.random() * 0.6));
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.PointsMaterial({
      color: 0x90e0ef,
      size: 0.18,
      transparent: true,
      opacity: 0.85
    });

    const pSystem = new THREE.Points(geometry, mat);
    this.scene.add(pSystem);

    let frames = 0;
    const anim = () => {
      frames++;
      const pos = pSystem.geometry.attributes.position.array;
      for (let i = 0; i < particleCount; i++) {
        pos[i * 3] += velocities[i].x;
        pos[i * 3 + 1] += velocities[i].y;
        pos[i * 3 + 2] += velocities[i].z;
      }
      pSystem.geometry.attributes.position.needsUpdate = true;
      mat.opacity -= 0.025;

      if (frames < 35 && mat.opacity > 0) {
        requestAnimationFrame(anim);
      } else {
        this.scene.remove(pSystem);
      }
    };
    anim();
  }

  /**
   * Crea una gota 3D de pasta térmica fresca viscosa sobre el CPU
   */
  createThermalPasteBlob(pos = new THREE.Vector3(0, 0.45, 3)) {
    const blobGeo = new THREE.SphereGeometry(0.35, 16, 12);
    blobGeo.scale(1.2, 0.4, 1.2);
    const blob = new THREE.Mesh(blobGeo, this.materials.freshThermalPaste);
    blob.position.copy(pos);
    blob.name = 'thermal_paste_blob';
    this.scene.add(blob);
    return blob;
  }

  // ==========================================================================
  // ANIMACIONES CINEMÁTICAS Y CONTROL DE CÁMARA
  // ==========================================================================

  /**
   * Mueve suavemente la cámara a una posición y objetivo determinados
   */
  focusCamera(targetPos, lookAtPos, duration = 800) {
    if (!this.camera || !this.controls) return;

    const startPos = this.camera.position.clone();
    const startTarget = this.controls.target.clone();
    const endPos = new THREE.Vector3(...targetPos);
    const endTarget = new THREE.Vector3(...lookAtPos);
    const startTime = performance.now();

    const updateCam = () => {
      const now = performance.now();
      const progress = Math.min((now - startTime) / duration, 1.0);
      const ease = 0.5 - Math.cos(progress * Math.PI) / 2; // Ease in-out

      this.camera.position.lerpVectors(startPos, endPos, ease);
      this.controls.target.lerpVectors(startTarget, endTarget, ease);
      this.controls.update();

      if (progress < 1.0) {
        requestAnimationFrame(updateCam);
      }
    };
    updateCam();
  }

  /**
   * Animación de inserción suave en 3D de una pieza en su zócalo
   */
  animateSlotPlacement(object3D, targetPos, onComplete) {
    const startPos = object3D.position.clone();
    // Inicia 4 unidades por encima de su slot
    startPos.y += 4.5;
    object3D.position.copy(startPos);
    this.scene.add(object3D);

    const startTime = performance.now();
    const duration = 750;

    const step = () => {
      const now = performance.now();
      const p = Math.min((now - startTime) / duration, 1.0);
      const ease = 1 - Math.pow(1 - p, 3); // Ease out cubic

      object3D.position.lerpVectors(startPos, targetPos, ease);

      if (p < 1.0) {
        requestAnimationFrame(step);
      } else {
        // Efecto de rebote ligero al encajar
        object3D.position.copy(targetPos);
        if (onComplete) onComplete();
      }
    };
    step();
  }

  /**
   * Resalta temporalmente una zona o slot con halo de éxito o error
   */
  flashSlotBox(pos, size, isSuccess = true) {
    const boxGeo = new THREE.BoxGeometry(size.x, size.y, size.z);
    const mat = (isSuccess ? this.materials.slotHighlight : this.materials.slotError).clone();
    const mesh = new THREE.Mesh(boxGeo, mat);
    mesh.position.copy(pos);
    this.scene.add(mesh);

    let opacity = 0.8;
    const fade = () => {
      opacity -= 0.035;
      mat.opacity = opacity;
      if (opacity > 0) {
        requestAnimationFrame(fade);
      } else {
        this.scene.remove(mesh);
      }
    };
    fade();
  }

  // Bucle de renderizado
  animate() {
    requestAnimationFrame(() => this.animate());

    if (this.controls) {
      this.controls.update();
    }

    // Rotación suave continua de ventiladores si existen
    if (this.gpuFans && this.gpuFans.length) {
      this.gpuFans.forEach(f => f.rotation.z += 0.08);
    }
    if (this.coolerFan) {
      this.coolerFan.rotation.z += 0.08;
    }

    this.renderer.render(this.scene, this.camera);
  }

  bindResize() {
    window.addEventListener('resize', () => {
      if (!this.container) return;
      const w = this.container.clientWidth;
      const h = this.container.clientHeight;
      if (w > 0 && h > 0) {
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(w, h);
      }
    });
  }

  clearScene() {
    const toRemove = [];
    this.scene.children.forEach(child => {
      if (child !== this.camera && !child.isLight && !(child instanceof THREE.GridHelper) && child.name !== 'floor') {
        toRemove.push(child);
      }
    });
    toRemove.forEach(c => this.scene.remove(c));
  }
}

window.Hardware3DWorld = Hardware3DWorld;
