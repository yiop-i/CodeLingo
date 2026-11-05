# 🚀 CodeLingo - Plataforma Educativa Integral en Python (Estilo Duolingo)

Aplicación educativa completa desarrollada en **Python 3** diseñada para enseñar lenguajes de programación, terminales de sistemas operativos (Windows y Linux) y componentes de hardware (PC de escritorio y Notebooks), adaptada para funcionar tanto en computadoras de escritorio como en dispositivos móviles (celulares y tablets).

---

## 📋 Resumen del Proyecto y Cumplimiento de Requisitos

| Característica | Detalle Implementado |
| :--- | :--- |
| **Cursos Disponibles** | **12 Cursos completos** en 4 grupos temáticos: Lenguajes (5), Web (3), Terminales (2) y Hardware (2). |
| **Estructura por Curso** | **4 Secciones progresivas** por curso: Básico, Intermedio, Avanzado y Especialista/Integrador. |
| **Lecciones por Sección** | **Mínimo 25 lecciones pedagógicas completas por sección** (**1,202 lecciones detalladas en total**). |
| **Pedagogía Lenguajes / Web** | Introducción conceptual → Práctica guiada con editor y ejecución → Quiz de comprensión → Reto integrador. |
| **Pedagogía Terminales** | Introducción de comando → Combinación con conceptos previos → Práctica interactiva con VFS → Reto acumulativo → Quiz. |
| **Pedagogía Hardware** | Introducción → Funcionamiento en el sistema → Práctica teórica → Ubicación en placa/chasis → Selección de variables → Reto. |
| **IA Tutora ("Byte")** | Pistas pedagógicas inteligentes (sin dar la respuesta) + Evaluador de código (1 a 100) + Generador adaptativo de refuerzo. |
| **Evaluaciones de Sección (Boss)** | Examen al final de cada sección. Si se aprueba (≥ 80%), desbloquea la siguiente sección y genera el **PDF Oficial de Apuntes**. Si se reprueba, la IA genera **niveles de ejercitación de refuerzo**. |
| **Multi-Curso Simultáneo** | Permite cursar varias materias a la vez con persistencia de progreso independiente en `codelingo_progress.json`. |
| **Generador de Apuntes PDF** | Motor PDF 1.4 estándar nativo en Python (genera archivos `.pdf` reales listos para descargar e imprimir sin dependencias). |
| **Multi-Dispositivo / Móvil** | Servidor multihilo local integrado para abrir la suite en celulares Android, tablets y navegadores por Wi-Fi. |

---

## 💻 Catálogo Completo de Cursos y Temario

### 1. 💻 Lenguajes de Programación
- **Python**: Sintaxis moderna, variables dinámicas, operadores, condicionales, bucles for/while, listas, diccionarios, sets, excepciones y POO con `@dataclass`.
- **C++**: Streams `std::cout/cin`, tipos con signo, punteros, referencias `&`, gestión de memoria con `new/delete`, templates y POO con `virtual` y destructores.
- **C**: Fundamentos de sistemas, `printf/scanf`, arrays, punteros `*` y `&`, aritmética de memoria, `malloc/free`, structs y persistencia en archivos `FILE*`.
- **Javascript**: Sintaxis ES6+, `let/const`, Arrow Functions, métodos funcionales `map/filter/reduce`, objetos, desestructuración, Promesas y `async/await`.
- **Java**: Máquina Virtual (JVM), tipos primitivos, `Scanner`, arrays, Programación Orientada a Objetos, herencia con `super`, interfaces, excepciones y Streams.

### 2. 🌐 Desarrollo Web
- **HTML**: Doctype HTML5, etiquetas semánticas (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`), enlaces, imágenes adaptativas, formularios y accesibilidad ARIA.
- **CSS**: Selectores, especificidad, cascada, Box Model (`box-sizing: border-box`), Flexbox unidimensional, CSS Grid bidimensional, transiciones y Media Queries responsivas.
- **Javascript Web**: El DOM, selectores (`querySelector`), escuchadores de eventos (`addEventListener`), manipulación dinámica de clases, `localStorage` y Fetch API.

### 3. 🖥️ Terminal de Sistemas Operativos
- **Terminal de Windows**: Símbolo del Sistema (CMD) y PowerShell 7, rutas absolutas/relativas, comandos de archivo (`dir`, `mkdir`, `type`, `copy`, `move`, `del`), diagnóstico de red (`ipconfig`, `ping`, `netstat`), gestión de procesos (`tasklist`, `taskkill`) y cmdlets con tuberías.
- **Terminal de Linux**: Filosofía UNIX, estándar FHS (`/bin`, `/home`, `/etc`), navegación con `pwd`, `ls -la`, `cd`, visualización con `cat`, `less`, `head`, `tail`, permisos octales con `chmod`, tuberías (`|`), redirecciones (`>` y `>>`), `grep` y scripting Bash.

### 4. 🛠️ Hardware de Computadora
- **PC de Escritorio**: Placa madre ATX, zócalos LGA frente a AM5, instalación del CPU e IHS, memorias RAM DDR4 vs DDR5 en Dual-Channel, fuentes ATX 80 Plus, almacenamiento NVMe M.2 PCIe 4.0/5.0, tarjetas gráficas dedicadas, refrigeración por aire vs líquida AIO y secuencia POST.
- **Notebook**: Chasis compacto y bisagras, baterías de litio y diagnóstico con `powercfg`, procesadores móviles soldados (BGA), disipación por heatpipes de cobre y ventiladores tipo turbina, pasta térmica, memorias SO-DIMM, módulos Wi-Fi M.2, pantallas eDP y técnicas de desarme con herramientas plásticas.

---

## 🏃 Cómo Ejecutar la Aplicación

### Opción 1: Interfaz Gráfica Nativa de Escritorio (Recomendada)
```powershell
python "C:\Users\alast\Downloads\app\main.py"
```
O desde la carpeta del proyecto en `scratch`:
```powershell
cd "C:\Users\alast\.gemini\antigravity\scratch\code-lingo-app"
python main.py
```

### Opción 2: Modo Web / Celulares y Tablets por Wi-Fi
Para usar la aplicación en un teléfono móvil o tablet:
```powershell
python main.py --web
```
Luego abre en el navegador de tu celular: `http://<IP-DE-TU-PC>:8080`.

### Opción 3: Terminal Virtual Directa por Consola
```powershell
# Terminal Linux Ubuntu Bash virtual:
python main.py --cli=linux

# Terminal Windows CMD y PowerShell virtual:
python main.py --cli=windows
```

---

## 🤖 El Asistente IA "Byte"

- **Pistas que guían sin responder**: Si el alumno tiene problemas con su código o comando, el botón **💡 Pista IA** analiza el código escrito y proporciona un consejo heurístico sobre la sintaxis, tipos o bloques sin revelar el código resuelto.
- **Evaluador de 1 a 100**: El botón **📊 Evaluar (1-100)** analiza sintaxis, buenas prácticas, lógica y manejo de excepciones, otorgando una nota acompañada de fortalezas y sugerencias concretas de mejora.
- **Refuerzo Adaptativo Automático**: Si el usuario obtiene menos de 80% en el Examen Boss de una sección, Byte analiza automáticamente qué preguntas falló y genera **niveles de refuerzo personalizados (🛠️ Refuerzo IA)** que se insertan en el camino de aprendizaje para nivelar los conocimientos débiles.

---

## 📄 Generación y Descarga de Apuntes PDF

Al superar con éxito la evaluación Boss de cualquier sección, se genera automáticamente su **PDF Oficial de Apuntes**. Puedes consultar todos tus apuntes desbloqueados y descargarlos en cualquier momento desde el botón superior **📄 Apuntes PDF**.
