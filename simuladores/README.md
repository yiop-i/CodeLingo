# Dev & Hardware 3D Simulator Suite (Python Edition)

Suite integral y modular de simuladores de desarrollo de software y montaje de computadoras en 3D (PC y Notebook CISCO estilo `pclab.eniun.com`), **programada en su totalidad en Python 3**.

Diseñada para funcionar de manera nativa y adaptativa en **Windows, Linux y Android**.

---

## 🚀 Cómo Iniciar la Suite

Solo necesitas tener instalado **Python 3.8 o superior**. No requiere paquetes de terceros ni dependencias externas de `pip`.

### 1. Iniciar la Aplicación Completa con Visor 3D WebGL:
```bash
python main.py
```
* Abrirá automáticamente el simulador en tu navegador predeterminado.
* Estará accesible en tu PC en `http://localhost:8080`.
* Estará accesible desde tu teléfono móvil **Android** en la misma red Wi-Fi ingresando a la IP mostrada en la consola (ej: `http://192.168.1.105:8080`).

### 2. Modos CLI directos por Terminal en Python:
Si prefieres interactuar con los simuladores directamente desde tu terminal de Python sin abrir el navegador:

```bash
# Terminal Linux Bash virtual escrita en Python:
python main.py --cli=linux

# Terminal Windows CMD y PowerShell escrita en Python:
python main.py --cli=windows
```

---

## 📁 Arquitectura del Proyecto en Python

```
dev-simulator-suite/
├── main.py                          # Punto de entrada principal (python main.py)
├── requirements.txt                 # Cero dependencias externas requeridas
├── simulators/                      # Motores de simulación 100% en Python
│   ├── __init__.py
│   ├── vscode_engine.py             # Ejecución y compilación de Python, C, C++, Java y JS
│   ├── linux_terminal.py            # Terminal Linux Bash con Sistema de Archivos Virtual (VFS)
│   ├── windows_terminal.py          # Símbolo del Sistema de Windows (CMD.EXE) y PowerShell
│   ├── web_studio.py                # Ensamblado y validación de HTML5/CSS3/JS en vivo
│   ├── hardware_recognition.py      # Simulador 1: Catálogo 3D, zócalos, arquitectura y Quiz
│   ├── hardware_placement.py        # Simulador 2: Validación estricta de ranuras y prelación
│   ├── hardware_upgrade.py          # Simulador 3: Sustitución de piezas viejas y benchmarks
│   └── hardware_maintenance.py      # Simulador 4: Termodinámica del CPU, pasta y limpieza
├── server/                          # Servidor y API REST multihilo en Python
│   ├── __init__.py
│   ├── api_handler.py               # Enrutador de peticiones y endpoints JSON
│   └── app_server.py                # Servidor HTTP multihilo con soporte CORS y LAN
├── js/
│   ├── client-api.js                # Puente en tiempo real entre la vista y el backend Python
│   ├── hardware-3d.js               # Renderizado WebGL 3D procedimental (Three.js)
│   ├── three.min.js                 # Motor 3D local offline
│   └── OrbitControls.js             # Controles orbitales 360° táctiles y de ratón
├── css/
│   └── hardware-sims.css            # Estilos del taller 3D y controles de cámara
└── index.html                       # Interfaz universal responsiva
```

---

## 🛠️ Detalle de los 8 Simuladores

### Software
1. **VS Code Multi-Lenguaje (`vscode_engine.py`):** Ejecuta código real en Python 3, compila C y C++ con GCC/G++, Java con OpenJDK y Node.js para JavaScript.
2. **Terminal Linux Bash (`linux_terminal.py`):** Emula un entorno Debian GNU/Linux completo con inodos, permisos, carpetas `/bin`, `/home`, `/etc`, y comandos `ls -la`, `cd`, `pwd`, `mkdir`, `rm`, `cat`, `echo`, `grep`, `touch`, `neofetch`, `python3`, etc.
3. **Terminal Windows (`windows_terminal.py`):** Emula CMD y PowerShell 7 con árbol de discos `C:\`, comandos `dir`, `cd`, `type`, `systeminfo`, `ipconfig`, `tasklist`, `Get-Process`, etc.
4. **Web Studio (`web_studio.py`):** Compila páginas web dinámicamente con inyección segura de consola y recarga en tiempo real.

### Hardware 3D (Estilo PC Lab)
5. **1. Reconocimiento 3D (`hardware_recognition.py`):** Inspección orbital 360° de placa base, CPU LGA1700, DDR5, RTX 4080, SO-DIMM, con zoom cinemático a hotspots y test de diagnóstico.
6. **2. Montaje en su Lugar 3D (`hardware_placement.py`):** Máquina de estados con validación estricta de ranuras: rechaza con animación de error si intentas poner RAM en PCIe o procesador en M.2.
7. **3. Upgrades 3D (`hardware_upgrade.py`):** Desmontaje de piezas viejas y montaje de repuestos modernos con cálculo en vivo de FPS (de 22 a 145 FPS), tiempos de booteo y memoria.
8. **4. Limpieza y Mantenimiento 3D (`hardware_maintenance.py`):** Cálculo de física térmica y partículas: aire comprimido para ventiladores, destornillador para disipador, alcohol isopropílico para disolver pasta seca y jeringa para aplicar pasta fresca (baja de 95°C a 31°C).
