# 🚀 CodeLingo - Plataforma Educativa Integral en Python (Estilo Duolingo)

Aplicación educativa completa desarrollada en **Python 3** diseñada para enseñar lenguajes de programación, terminales de sistemas operativos (Windows y Linux) y componentes de hardware (PC de escritorio y Notebooks), adaptada tanto para computadoras de escritorio como para dispositivos móviles (celulares y tablets).

---

## 🎯 Flujo Pedagógico Obligatorio en 4 Fases por Lección

Cada una de las **1,202 lecciones** cuenta con un asistente secuencial estricto que guía al estudiante a través de 4 fases obligatorias:

```
[ Fase 1: Introducción Teórica Extensa ]
                  ⬇
[ Fase 2: Práctica Activa (Creación desde cero sin código hecho) ]
                  ⬇
[ Fase 3: Larga Fase de Evaluación de Teoría (Batería de Preguntas) ]
                  ⬇
[ Fase 4: Reto Integrador Acumulativo de Todo lo Visto ]
```

1. **Fase 1: Extensa Introducción Teórica al Tema**
   - **Marco Teórico Profundo:** Explicación detallada de qué es el concepto, por qué existe en la arquitectura del sistema y qué problemas del mundo real resuelve.
   - **Anatomía y Funcionamiento Interno:** Desglose formal de sintaxis, gestión de memoria (Stack/Heap), zócalos o parámetros de terminal.
   - **Ejemplo Teórico Comentado:** Código o comando ilustrativo analizado línea por línea que sirve como referencia conceptual.
   - **Errores Frecuentes y Consejos de Byte:** Gotchas comunes, mejores prácticas y advertencias para evitar fallos.

2. **Fase 2: Práctica Activa (Creación desde Cero - ¡Sin Código Hecho!)**
   - El editor o la consola virtual **NO entrega el código ya resuelto**.
   - El estudiante recibe la consigna, objetivos y directivas claras para escribir su propia solución desde cero.
   - Cuenta con ejecución en vivo, consola de salida interactiva, **💡 Pista IA** (consejos pedagógicos sin dar la solución) y **📊 Evaluar Código (1-100)**.
   - Es obligatorio escribir y probar una solución para poder validar y avanzar.

3. **Fase 3: Larga Fase de Evaluación de Teoría**
   - Batería interactiva de **3 preguntas teóricas profundas** por lección (>3,600 preguntas en todo el sistema).
   - Evalúa fundamentos conceptuales, comportamiento y sintaxis, y análisis de casos técnicos o errores.
   - Cada opción cuenta con retroalimentación inmediata y explicaciones técnicas detalladas proporcionadas por Byte.

4. **Fase 4: Reto Integrador Acumulativo**
   - Desafío práctico acumulativo que exige combinar el nuevo concepto aprendido con los temas vistos previamente a lo largo de la sección y del curso.
   - Al completar el reto integrador, se otorgan +15 XP y +5 Gemas, marcando la lección como aprobada y desbloqueando el siguiente nivel en el camino de CodeLingo.

---

## 📊 Catálogo de Cursos (12 Cursos, 48 Secciones, 1,202 Lecciones)

| Grupo | Cursos Disponibles | Secciones | Total Lecciones |
| :--- | :--- | :---: | :---: |
| **Lenguajes** | Python, C++, C, Javascript, Java | 20 (4 por curso) | **500 lecciones** |
| **Desarrollo Web** | HTML, CSS, Javascript Web | 12 (4 por curso) | **300 lecciones** |
| **Terminales** | Terminal de Windows (CMD/PowerShell), Terminal de Linux (Ubuntu Bash) | 8 (4 por curso) | **202 lecciones** |
| **Hardware** | PC de Escritorio (ATX/PCIe/DDR), Notebook (BGA/SO-DIMM/Flex) | 8 (4 por curso) | **200 lecciones** |
| **TOTALES** | **12 Cursos Completos** | **48 Secciones** | **1,202 Lecciones** |

---

## 🤖 El Asistente IA "Byte"

- **Pistas que guían sin revelar la respuesta:** Consejos heurísticos que orientan el razonamiento del usuario sin darle el código resuelto.
- **Evaluador de 1 a 100:** Análisis de calidad, legibilidad, robustez y manejo de excepciones con desglose de fortalezas y mejoras.
- **Refuerzo Adaptativo Automático:** Si el estudiante no alcanza el 80% en el Examen Boss de una sección, Byte analiza las fallas y genera niveles de refuerzo personalizados en el camino de aprendizaje.

---

## 📜 Generación de Apuntes Oficiales en PDF

Al aprobar el Examen Boss de cualquier sección ($\ge 80\%$), se genera automáticamente un documento **PDF 1.4 oficial** con el resumen y apuntes técnicos de las 25 lecciones para descargar, consultar o imprimir.

---

## 💻 Modos de Ejecución

### Opción 1: Interfaz Gráfica Nativa de Escritorio
```powershell
python "C:\Users\alast\Downloads\app\main.py"
```

### Opción 2: Modo Web para Celulares y Tablets
```powershell
python "C:\Users\alast\Downloads\app\main.py" --web
```
Luego abre en tu navegador móvil: `http://<IP-DE-TU-PC>:8080`.

### Opción 3: Terminal Virtual CLI Directa
```powershell
python "C:\Users\alast\Downloads\app\main.py" --cli=linux
python "C:\Users\alast\Downloads\app\main.py" --cli=windows
```
