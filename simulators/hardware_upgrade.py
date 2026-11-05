"""
HARDWARE_UPGRADE.PY - Simulador 3 en Python: Upgrades y Reemplazo de Componentes
Diagnóstico de cuellos de botella, cálculo de benchmarks y órdenes de servicio técnico.
"""

class HardwareUpgradeSimulator:
    def __init__(self):
        self.cases = {
            'desktop': {
                'client': 'Marcos R. (Gamer & Creador de Contenido)',
                'problem': 'Mi PC tarda 3 minutos en prender, los juegos van a tirones (22 FPS) y el disco duro hace un ruido insoportable. Necesito un upgrade urgente.',
                'components': {
                    'storage': {
                        'name': 'Almacenamiento',
                        'old': 'HDD Seagate 500GB 5400RPM Mecánico',
                        'new': 'SSD Samsung 990 Pro 2TB NVMe 7450MB/s',
                        'state': 'old' # old, empty, new
                    },
                    'ram': {
                        'name': 'Memoria RAM',
                        'old': '1x 8GB DDR4 2133MHz Verde Genérica',
                        'new': '32GB (2x16GB) Corsair DDR5 6000MHz RGB Dual Channel',
                        'state': 'old'
                    },
                    'gpu': {
                        'name': 'Tarjeta Gráfica',
                        'old': 'NVIDIA GeForce GTX 1050 Ti 4GB',
                        'new': 'NVIDIA GeForce RTX 4080 Super 16GB Triple Fan',
                        'state': 'old'
                    }
                }
            },
            'laptop': {
                'client': 'Elena G. (Diseñadora & Trabajo Remoto)',
                'problem': 'Mi notebook hierve en las piernas, la batería solo dura 10 minutos y se congela al abrir Photoshop. Necesito batería nueva, más RAM y un disipador limpio.',
                'components': {
                    'battery': {
                        'name': 'Batería Li-Ion',
                        'old': 'Batería Li-Ion Degradada (Hinchada 15% vida)',
                        'new': 'Batería Original 5200mAh 4 Celdas Nueva',
                        'state': 'old'
                    },
                    'ram': {
                        'name': 'Memoria SO-DIMM',
                        'old': 'SO-DIMM 4GB DDR4 2133MHz',
                        'new': 'SO-DIMM 16GB DDR4 3200MHz Kingston',
                        'state': 'old'
                    },
                    'cooling': {
                        'name': 'Sistema Térmico',
                        'old': 'Disipador Térmico con pasta seca petrificada',
                        'new': 'Sistema Térmico Limpio con Pasta Fresca',
                        'state': 'old'
                    }
                }
            }
        }
        self.active_case = 'desktop'

    def set_case(self, case_id: str):
        if case_id in self.cases:
            self.active_case = case_id

    def unmount_component(self, slot_key: str) -> dict:
        """Desmonta la pieza vieja del equipo y la deja en estado 'empty'"""
        c = self.cases[self.active_case]['components'].get(slot_key)
        if not c:
            return {'success': False, 'error': f"Ranura '{slot_key}' no válida."}
        if c['state'] != 'old':
            return {'success': False, 'error': f"La pieza ya no está en estado viejo (estado actual: {c['state']})."}

        c['state'] = 'empty'
        benchmarks = self.calculate_benchmarks()
        return {
            'success': True,
            'slot_key': slot_key,
            'new_state': 'empty',
            'message': f"Pieza '{c['old']}' desatornillada y retirada a la bandeja de desensamble.",
            'benchmarks': benchmarks
        }

    def install_upgrade(self, slot_key: str) -> dict:
        """Instala el repuesto nuevo si la ranura está vacía"""
        c = self.cases[self.active_case]['components'].get(slot_key)
        if not c:
            return {'success': False, 'error': f"Ranura '{slot_key}' no válida."}
        if c['state'] == 'old':
            return {'success': False, 'error': f"Debes desmontar primero la pieza vieja '{c['old']}' antes de instalar el repuesto."}
        if c['state'] == 'new':
            return {'success': False, 'error': f"El repuesto nuevo ya está instalado en esta ranura."}

        c['state'] = 'new'
        benchmarks = self.calculate_benchmarks()
        all_completed = all(item['state'] == 'new' for item in self.cases[self.active_case]['components'].values())

        return {
            'success': True,
            'slot_key': slot_key,
            'new_state': 'new',
            'installed_name': c['new'],
            'all_completed': all_completed,
            'message': f"¡Upgrade exitoso! '{c['new']}' instalado correctamente en el equipo.",
            'benchmarks': benchmarks
        }

    def calculate_benchmarks(self) -> dict:
        comps = self.cases[self.active_case]['components']
        if self.active_case == 'desktop':
            fps = 145 if comps['gpu']['state'] == 'new' else (0 if comps['gpu']['state'] == 'empty' else 22)
            boot = 7 if comps['storage']['state'] == 'new' else (999 if comps['storage']['state'] == 'empty' else 180)
            ram = 32 if comps['ram']['state'] == 'new' else (0 if comps['ram']['state'] == 'empty' else 8)
            return {
                'fps': f"{fps} FPS",
                'fps_val': fps,
                'boot_time': f"{boot}s" if boot < 999 else "Sin SO",
                'boot_val': boot,
                'ram': f"{ram} GB",
                'ram_val': ram
            }
        else:
            bat = "6.5 hrs" if comps['battery']['state'] == 'new' else ("Sin batería" if comps['battery']['state'] == 'empty' else "12 min")
            ram = 16 if comps['ram']['state'] == 'new' else (0 if comps['ram']['state'] == 'empty' else 4)
            return {
                'fps': bat,
                'fps_val': 100 if comps['battery']['state'] == 'new' else 10,
                'boot_time': "8s",
                'boot_val': 8,
                'ram': f"{ram} GB",
                'ram_val': ram
            }


if __name__ == '__main__':
    sim = HardwareUpgradeSimulator()
    print("Probando Simulador de Upgrades en Python...")
    print("Benchmarks iniciales:", sim.calculate_benchmarks())
    sim.unmount_component('gpu')
    sim.install_upgrade('gpu')
    print("Benchmarks tras upgrade de GPU:", sim.calculate_benchmarks())
