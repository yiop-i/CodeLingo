"""
HW_RECOGNITION.PY - SIMULADOR 1 DE RECONOCIMIENTO DE COMPONENTES 3D EN PYTHON
Base de datos de anatomía, especificaciones técnicas, zócalos, voltajes y evaluación interactiva
"""

class HardwareRecognitionSimulator:
    def __init__(self):
        self.catalog = [
            {
                "id": "comp_mobo",
                "name": "Placa Base / Tarjeta Madre (Motherboard ATX)",
                "category": "pc",
                "icon": "🖲️",
                "desc": "Circuito impreso principal que interconecta todos los buses y componentes del sistema (CPU, RAM, GPU, Almacenamiento y periféricos).",
                "slot": "Se atornilla sobre los 9 separadores metálicos del chasis (Gabinete ATX/Micro-ATX/ITX).",
                "voltage": "Alimentada por el conector principal ATX de 24 pines y conectores EPS de 8 pines.",
                "hotspots": [
                    {"name": "Socket del Procesador (LGA1700)", "tip": "Zócalo donde se inserta el CPU. Cuenta con 1700 contactos dorados y palanca de acero."},
                    {"name": "Ranuras DIMM DDR5", "tip": "Ranuras para memorias DDR5 de alta frecuencia con pestillos de retención en extremos."},
                    {"name": "Ranura Blindada PCIe 5.0 x16 (GPU)", "tip": "Slot reforzado con armadura de acero para tarjetas gráficas pesadas."},
                    {"name": "Ranura M.2 NVMe PCIe 4.0", "tip": "Zócalo compacto para almacenamiento SSD ultrarrápido conectado directo a líneas PCIe."},
                    {"name": "Disipadores de Aluminio VRM", "tip": "Módulos reguladores de voltaje masivos que estabilizan la corriente hacia el microprocesador."}
                ],
                "quiz": {
                    "question": "¿Cuál es el conector principal que alimenta de energía eléctrica a toda la placa madre?",
                    "options": ["Conector ATX principal de 24 pines", "Cable HDMI de alta velocidad", "Conector SATA de datos"],
                    "answer_index": 0
                }
            },
            {
                "id": "comp_cpu",
                "name": "Unidad Central de Procesamiento (CPU Intel Core i9-14900K)",
                "category": "pc",
                "icon": "🔲",
                "desc": "El 'cerebro' del ordenador. Ejecuta cálculos lógicos, aritméticos y coordina todas las instrucciones del sistema operativo.",
                "slot": "Se coloca en el Socket de la placa madre respetando el triángulo dorado de alineación.",
                "voltage": "Voltaje de núcleo entre 0.8V y 1.45V con un consumo pico de hasta 253W en carga máxima.",
                "hotspots": [
                    {"name": "IHS (Integrated Heat Spreader)", "tip": "Difusor térmico de níquel pulido con grabado láser que transfiere el calor al disipador."},
                    {"name": "Pads de Contacto LGA", "tip": "Contactos dorados que apoyan sobre los pines elásticos del zócalo sin doblarlos."},
                    {"name": "Triángulo Dorado de Alineación", "tip": "Guía visual indispensable: debe coincidir exactamente con la flecha del socket de la placa."}
                ],
                "quiz": {
                    "question": "¿Qué componente se debe aplicar siempre entre el IHS del CPU y la base del disipador?",
                    "options": ["Pasta térmica de alta conductividad", "Alcohol en gel", "Aceite mineral"],
                    "answer_index": 0
                }
            },
            {
                "id": "comp_ram",
                "name": "Memoria RAM DDR5 Gamer (32GB 6000MHz Dual Channel)",
                "category": "pc",
                "icon": "💾",
                "desc": "Memoria volátil ultrarrápida. Almacena en tiempo real los datos que el procesador necesita inmediatamente para evitar cuellos de botella.",
                "slot": "Se instala en las ranuras DIMM abriendo los pestillos y ejerciendo presión uniforme hasta escuchar el 'clic'.",
                "voltage": "DDR5 estándar a 1.1V (hasta 1.35V con perfiles XMP 3.0 / EXPO overclocking).",
                "hotspots": [
                    {"name": "Muesca Central de Seguridad (Key Notch)", "tip": "Ranura física descentrada que impide instalar el módulo al revés o forzar DDR4 en DDR5."},
                    {"name": "Disipador Térmico de Aluminio", "tip": "Cuerpo de aleación de aluminio que absorbe el calor de los chips de memoria a 6000+ MHz."},
                    {"name": "Barra Difusora Superior RGB", "tip": "Polímero acrílico translúcido con diodos LED direccionables sincronizados por software."}
                ],
                "quiz": {
                    "question": "¿Qué ocurre con la información en la memoria RAM al apagar por completo la computadora?",
                    "options": ["Se borra completamente por ser memoria volátil", "Se guarda para siempre como en un disco rígido", "Se envía a la nube automáticamente"],
                    "answer_index": 0
                }
            },
            {
                "id": "comp_gpu",
                "name": "Tarjeta Gráfica Dedicada (NVIDIA GeForce RTX 4080 Super)",
                "category": "pc",
                "icon": "🎮",
                "desc": "Aceleradora gráfica masiva con miles de núcleos CUDA / RT Cores dedicada al renderizado 3D en tiempo real, trazado de rayos (Ray Tracing) e Inteligencia Artificial.",
                "slot": "Se conecta en la ranura PCIe 5.0 x16 y se atornilla al chasis con dos tornillos metálicos.",
                "voltage": "Requiere alimentación suplementaria mediante conector 12VHPWR (hasta 450W).",
                "hotspots": [
                    {"name": "Conector Dorado PCIe x16", "tip": "Peine de 164 contactos dorados que se inserta firmemente en la ranura PCIe blindada."},
                    {"name": "Sistema de Refrigeración Triple Fan", "tip": "Tres ventiladores axiales con aspas invertidas y disipador atravesado por tubos de cobre."},
                    {"name": "Soporte Metálico Posterior (I/O Bracket)", "tip": "Sujeta la tarjeta al gabinete y aloja los puertos DisplayPort 1.4a y HDMI 2.1."}
                ],
                "quiz": {
                    "question": "¿En qué ranura específica de la placa madre se instala la tarjeta gráfica principal?",
                    "options": ["Ranura PCIe x16 (blindada)", "Ranura DIMM de memoria RAM", "Puerto SATA"],
                    "answer_index": 0
                }
            },
            {
                "id": "comp_laptop_battery",
                "name": "Batería de Notebook Li-Ion (4 Celdas 5200mAh)",
                "category": "laptop",
                "icon": "🔋",
                "desc": "Módulo de energía autónomo para portátiles con celdas de iones de litio y circuito BMS de protección contra sobrecargas.",
                "slot": "Bahía inferior asegurada con pestillos mecánicos Lock (bloqueo) y Release (expulsión).",
                "voltage": "Voltaje nominal de 11.1V a 14.8V.",
                "hotspots": [
                    {"name": "Terminal de Conexión Multipin", "tip": "Conecta el bus de energía y comunicación SMBus con la placa madre de la notebook."},
                    {"name": "Pestillos de Seguridad (Lock & Release)", "tip": "Traban mecánicamente el pack al chasis para evitar desconexiones accidentales."}
                ],
                "quiz": {
                    "question": "¿Cuál es la primera regla de seguridad técnica antes de abrir una notebook para mantenimiento?",
                    "options": ["Desconectar el cargador de pared y retirar la batería", "Poner la notebook sobre una toalla mojada", "Acelerar los ventiladores"],
                    "answer_index": 0
                }
            },
            {
                "id": "comp_laptop_sodimm",
                "name": "Memoria RAM SO-DIMM (Laptop Form Factor 16GB)",
                "category": "laptop",
                "icon": "💻💾",
                "desc": "Módulo de memoria RAM compacto diseñado específicamente para ordenadores portátiles, mini PCs y consolas.",
                "slot": "Se inserta obligatoriamente en un ángulo inclinado de 30° a 45° antes de presionar hacia abajo hasta el bloqueo.",
                "voltage": "1.2V (DDR4) o 1.1V (DDR5).",
                "hotspots": [
                    {"name": "Borde de Contactos a 45°", "tip": "Debe ingresar completamente en la ranura con inclinación antes de presionar hacia abajo."},
                    {"name": "Muescas Laterales de Sujeción", "tip": "Donde traban los dos resortes metálicos laterales de la bahía SO-DIMM."}
                ],
                "quiz": {
                    "question": "¿A qué ángulo se introduce un módulo de memoria RAM SO-DIMM en su ranura en una notebook?",
                    "options": ["A un ángulo inclinado de 30° a 45°", "Totalmente vertical a 90°", "Completamente plana a 0°"],
                    "answer_index": 0
                }
            }
        ]

    def get_catalog(self, category: str = "all") -> list:
        if category == "all":
            return self.catalog
        return [c for c in self.catalog if c.get("category") == category]

    def get_component(self, comp_id: str) -> dict:
        for c in self.catalog:
            if c["id"] == comp_id:
                return c
        return {}

    def evaluate_quiz(self, comp_id: str, selected_option_idx: int) -> dict:
        comp = self.get_component(comp_id)
        if not comp or "quiz" not in comp:
            return {"valid": False, "message": "Componente no encontrado"}

        quiz = comp["quiz"]
        is_correct = selected_option_idx == quiz["answer_index"]
        correct_answer_text = quiz["options"][quiz["answer_index"]]

        return {
            "correct": is_correct,
            "message": "¡Excelente! Respuesta técnica acertada." if is_correct else f"Incorrecto. La respuesta correcta era: {correct_answer_text}",
            "correct_answer": correct_answer_text
        }
