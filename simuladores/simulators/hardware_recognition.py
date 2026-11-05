"""
HARDWARE_RECOGNITION.PY - Simulador 1 en Python: Reconocimiento de Componentes
Base de conocimiento de hardware, anatomía de zócalos, arquitectura y evaluación técnica.
"""

class HardwareRecognitionSimulator:
    def __init__(self):
        self.components = [
            {
                'id': 'comp_mobo',
                'name': 'Placa Base / Tarjeta Madre (Motherboard ATX)',
                'category': 'pc',
                'icon': '🖲️',
                'desc': 'Circuito impreso principal que interconecta todos los buses y componentes del sistema (CPU, RAM, GPU, Almacenamiento y periféricos).',
                'slot': 'Se atornilla sobre los 9 separadores metálicos del chasis (Gabinete ATX/Micro-ATX/ITX).',
                'voltage': 'Alimentada por conector principal ATX de 24 pines y conectores EPS de 8 pines.',
                'camera_pos': [0, 14, 18],
                'look_at': [0, 0, 0],
                'hotspots': [
                    {'name': 'Socket del Procesador (LGA1700)', 'cam': [0, 6, 6], 'look': [0, 0, 3], 'tip': 'Zócalo donde se inserta el CPU. Cuenta con 1700 contactos metálicos y palanca de acero.'},
                    {'name': 'Ranuras DIMM DDR5 (Dual-Channel)', 'cam': [6, 6, 6], 'look': [4.2, 0, 3], 'tip': 'Ranuras para memorias DDR5 de alta frecuencia con pestillos de retención en extremos.'},
                    {'name': 'Ranura Blindada PCIe 5.0 x16 (GPU)', 'cam': [-1, 5, -2], 'look': [-0.5, 0, -3.2], 'tip': 'Slot reforzado con armadura de acero para tarjetas gráficas pesadas.'},
                    {'name': 'Ranura M.2 NVMe PCIe 4.0', 'cam': [0, 4, 1], 'look': [0, 0, -1.2], 'tip': 'Zócalo compacto para almacenamiento SSD ultrarrápido conectado directo a líneas PCIe.'},
                    {'name': 'Disipadores de Aluminio VRM', 'cam': [-4, 5, 6], 'look': [-3.2, 0, 3.2], 'tip': 'Módulos reguladores de voltaje masivos que estabilizan la corriente hacia el microprocesador.'}
                ],
                'quiz': {
                    'question': '¿Cuál es el conector principal que alimenta de energía eléctrica a toda la placa madre?',
                    'options': ['Conector ATX principal de 24 pines', 'Cable HDMI de alta velocidad', 'Conector SATA de datos'],
                    'answer_index': 0,
                    'explanation': 'El conector ATX de 24 pines proporciona las líneas de voltaje de 12V, 5V y 3.3V a todos los circuitos integrados de la placa.'
                }
            },
            {
                'id': 'comp_cpu',
                'name': 'Unidad Central de Procesamiento (CPU Intel Core i9-14900K)',
                'category': 'pc',
                'icon': '🔲',
                'desc': 'El "cerebro" del ordenador. Ejecuta cálculos lógicos, aritméticos y coordina todas las instrucciones del sistema operativo.',
                'slot': 'Se coloca en el Socket de la placa madre respetando el triángulo dorado de alineación.',
                'voltage': 'Voltaje de núcleo entre 0.8V y 1.45V con un consumo pico de hasta 253W en carga máxima.',
                'camera_pos': [0, 5, 6],
                'look_at': [0, 0, 0],
                'hotspots': [
                    {'name': 'IHS (Integrated Heat Spreader)', 'cam': [0, 4, 3], 'look': [0, 0, 0], 'tip': 'Difusor térmico de níquel pulido con grabado láser que transfiere el calor al disipador.'},
                    {'name': 'Pads de Contacto LGA (Parte inferior)', 'cam': [0, -4, 3], 'look': [0, 0, 0], 'tip': 'Contactos dorados que apoyan sobre los pines elásticos del zócalo sin doblarlos.'},
                    {'name': 'Triángulo Dorado de Alineación', 'cam': [-1.5, 2, 2], 'look': [-1.5, 0, 1.5], 'tip': 'Guía visual indispensable: debe coincidir exactamente con la flecha del socket de la placa.'}
                ],
                'quiz': {
                    'question': '¿Qué componente se debe aplicar siempre entre el IHS del CPU y la base del disipador?',
                    'options': ['Pasta térmica de alta conductividad', 'Alcohol en gel', 'Aceite mineral'],
                    'answer_index': 0,
                    'explanation': 'La pasta térmica llena las microscópicas imperfecciones del metal para lograr una transferencia de calor eficiente hacia el disipador.'
                }
            },
            {
                'id': 'comp_ram',
                'name': 'Memoria RAM DDR5 Gamer (32GB 6000MHz Dual Channel)',
                'category': 'pc',
                'icon': '💾',
                'desc': 'Memoria volátil ultrarrápida. Almacena en tiempo real los datos que el procesador necesita inmediatamente para evitar cuellos de botella.',
                'slot': 'Se instala en las ranuras DIMM abriendo los pestillos y ejerciendo presión uniforme hasta escuchar el "clic".',
                'voltage': 'DDR5 estándar a 1.1V (hasta 1.35V con perfiles XMP 3.0 / EXPO overclocking).',
                'camera_pos': [0, 4, 7],
                'look_at': [0, 0, 0],
                'hotspots': [
                    {'name': 'Muesca Central de Seguridad (Key Notch)', 'cam': [0, 1, 3], 'look': [0, -0.9, 0], 'tip': 'Ranura física descentrada que impide instalar el módulo al revés o forzar DDR4 en DDR5.'},
                    {'name': 'Disipador Térmico de Aluminio', 'cam': [0, 2, 4], 'look': [0, 0, 0], 'tip': 'Cuerpo de aleación de aluminio que absorbe el calor de los chips de memoria a 6000+ MHz.'},
                    {'name': 'Barra Difusora Superior RGB', 'cam': [0, 3, 2], 'look': [0, 0.95, 0], 'tip': 'Polímero acrílico translúcido con diodos LED direccionables sincronizados por software.'}
                ],
                'quiz': {
                    'question': '¿Qué ocurre con la información en la memoria RAM al apagar por completo la computadora?',
                    'options': ['Se borra completamente por ser memoria volátil', 'Se guarda para siempre como en un disco rígido', 'Se envía a la nube automáticamente'],
                    'answer_index': 0,
                    'explanation': 'La memoria RAM es volátil; requiere energía eléctrica constante para mantener los transistores cargados. Al cortar la corriente, los datos desaparecen.'
                }
            },
            {
                'id': 'comp_gpu',
                'name': 'Tarjeta Gráfica Dedicada (NVIDIA GeForce RTX 4080 Super)',
                'category': 'pc',
                'icon': '🎮',
                'desc': 'Aceleradora gráfica masiva con miles de núcleos CUDA / RT Cores dedicada al renderizado 3D en tiempo real, trazado de rayos (Ray Tracing) e Inteligencia Artificial.',
                'slot': 'Se conecta en la ranura PCIe 5.0 x16 y se atornilla al chasis con dos tornillos metálicos.',
                'voltage': 'Requiere alimentación suplementaria mediante conector 12VHPWR (hasta 450W).',
                'camera_pos': [0, 7, 13],
                'look_at': [0, 0, 0],
                'hotspots': [
                    {'name': 'Conector Dorado PCIe x16', 'cam': [-1, 2, 4], 'look': [-1, 0.4, 2.3], 'tip': 'Peine de 164 contactos dorados que se inserta firmemente en la ranura PCIe blindada.'},
                    {'name': 'Sistema de Refrigeración Triple Fan', 'cam': [0, 2, 6], 'look': [0, -1.8, 0], 'tip': 'Tres ventiladores axiales con aspas invertidas y disipador atravesado por tubos de cobre.'},
                    {'name': 'Soporte Metálico Posterior (I/O Bracket)', 'cam': [-5, 2, 3], 'look': [-5.8, -0.6, 0], 'tip': 'Sujeta la tarjeta al gabinete y aloja los puertos DisplayPort 1.4a y HDMI 2.1.'}
                ],
                'quiz': {
                    'question': '¿En qué ranura específica de la placa madre se instala la tarjeta gráfica principal?',
                    'options': ['Ranura PCIe x16 (blindada)', 'Ranura DIMM de memoria RAM', 'Puerto SATA'],
                    'answer_index': 0,
                    'explanation': 'La ranura PCIe x16 es la única con el ancho de banda y conexiones físicas necesarias para tarjetas de video de alto rendimiento.'
                }
            },
            {
                'id': 'comp_laptop_sodimm',
                'name': 'Memoria RAM SO-DIMM (Laptop Form Factor 16GB)',
                'category': 'laptop',
                'icon': '💻💾',
                'desc': 'Módulo de memoria RAM compacto diseñado específicamente para ordenadores portátiles, mini PCs y consolas.',
                'slot': 'Se inserta obligatoriamente en un ángulo inclinado de 30° a 45° antes de presionar hacia abajo hasta el bloqueo.',
                'voltage': '1.2V (DDR4) o 1.1V (DDR5).',
                'camera_pos': [0, 3, 5],
                'look_at': [0, 0, 0],
                'hotspots': [
                    {'name': 'Borde de Contactos a 45°', 'cam': [0, 1, 3], 'look': [0, -0.7, 0], 'tip': 'Debe ingresar completamente en la ranura con inclinación antes de presionar hacia abajo.'},
                    {'name': 'Muescas Laterales de Sujeción', 'cam': [0, 1, 2], 'look': [0, 0, 0], 'tip': 'Donde traban los dos resortes metálicos laterales de la bahía SO-DIMM.'}
                ],
                'quiz': {
                    'question': '¿A qué ángulo se introduce un módulo de memoria RAM SO-DIMM en su ranura en una notebook?',
                    'options': ['A un ángulo inclinado de 30° a 45°', 'Totalmente vertical a 90°', 'Completamente plana a 0°'],
                    'answer_index': 0,
                    'explanation': 'Las ranuras SO-DIMM de computadoras portátiles exigen insertar el conector con inclinación de 30-45 grados antes de empujarlo hacia abajo hasta que los pestillos de resorte hagan clic.'
                }
            }
        ]

    def get_catalog(self, category: str = "all") -> list:
        if category == "all":
            return self.components
        return [c for c in self.components if c['category'] == category]

    def get_component(self, comp_id: str) -> dict:
        for c in self.components:
            if c['id'] == comp_id:
                return c
        return None

    def validate_quiz_answer(self, comp_id: str, selected_index: int) -> dict:
        comp = self.get_component(comp_id)
        if not comp:
            return {'valid': False, 'error': 'Componente no encontrado'}

        q = comp['quiz']
        is_correct = (selected_index == q['answer_index'])
        return {
            'valid': True,
            'is_correct': is_correct,
            'correct_index': q['answer_index'],
            'correct_text': q['options'][q['answer_index']],
            'explanation': q['explanation']
        }


if __name__ == '__main__':
    sim = HardwareRecognitionSimulator()
    print("Módulo de Reconocimiento de Hardware en Python")
    for c in sim.get_catalog():
        print(f" - [{c['id']}] {c['name']}")
