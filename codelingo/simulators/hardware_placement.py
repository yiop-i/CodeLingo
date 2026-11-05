"""
HARDWARE_PLACEMENT.PY - Simulador 2 en Python: Montaje y Validación Estricta de Ranuras
Controlador de estados, reglas de incompatibilidad de zócalos y verificación de secuencia.
"""

class HardwarePlacementSimulator:
    def __init__(self):
        self.machines = {
            'desktop': {
                'name': 'Gabinete Gamer ATX (Montaje de Escritorio)',
                'parts': {
                    'part_cpu': {'name': 'Intel Core i9-14900K', 'valid_slot': 'target_cpu', 'requires': None, 'desc': 'Socket LGA1700'},
                    'part_cooler': {'name': 'Disipador de Torre con Heatpipes', 'valid_slot': 'target_cooler', 'requires': 'part_cpu', 'desc': 'Soporte y Backplate del CPU'},
                    'part_ram': {'name': 'Kit 32GB DDR5 RGB', 'valid_slot': 'target_ram', 'requires': None, 'desc': 'Ranuras DIMM 2 y 4'},
                    'part_gpu': {'name': 'NVIDIA RTX 4080 Super', 'valid_slot': 'target_gpu', 'requires': None, 'desc': 'Ranura PCIe 5.0 x16 Blindada'},
                    'part_m2': {'name': 'SSD Samsung 990 Pro 2TB NVMe', 'valid_slot': 'target_m2', 'requires': None, 'desc': 'Zócalo M.2 PCIe 4.0'},
                    'part_psu': {'name': 'Fuente Corsair 850W Gold', 'valid_slot': 'target_psu', 'requires': None, 'desc': 'Bahía de Fuente de Poder'}
                },
                'slots': {
                    'target_cpu': {'name': 'Socket LGA1700', 'occupied_by': None},
                    'target_cooler': {'name': 'Soporte Disipador CPU', 'occupied_by': None},
                    'target_ram': {'name': 'Ranuras DIMM DDR5', 'occupied_by': None},
                    'target_gpu': {'name': 'Ranura PCIe 5.0 x16', 'occupied_by': None},
                    'target_m2': {'name': 'Zócalo M.2 PCIe', 'occupied_by': None},
                    'target_psu': {'name': 'Bahía PSU', 'occupied_by': None}
                }
            },
            'notebook': {
                'name': 'Chasis de Notebook (CISCO Virtual Laptop)',
                'parts': {
                    'lap_battery': {'name': 'Batería Li-Ion 5200mAh', 'valid_slot': 'target_lap_battery', 'requires': None, 'desc': 'Bahía de Batería con Pestillos Lock'},
                    'lap_sodimm': {'name': 'Memoria RAM SO-DIMM 16GB (45°)', 'valid_slot': 'target_lap_sodimm', 'requires': None, 'desc': 'Ranura SO-DIMM (Ángulo 45°)'},
                    'lap_caddy': {'name': 'SSD 2.5" SATA en Caddy', 'valid_slot': 'target_lap_caddy', 'requires': None, 'desc': 'Bahía 2.5" SATA HDD/SSD'},
                    'lap_cooling': {'name': 'Heatpipe de Cobre & Turbina', 'valid_slot': 'target_lap_cooling', 'requires': None, 'desc': 'Circuito Térmico del CPU/GPU'},
                    'lap_optical': {'name': 'Lectora DVD-RW Slim', 'valid_slot': 'target_lap_optical', 'requires': None, 'desc': 'Bahía de Unidad Óptica Slim'}
                },
                'slots': {
                    'target_lap_battery': {'name': 'Bahía Batería', 'occupied_by': None},
                    'target_lap_sodimm': {'name': 'Ranura SO-DIMM', 'occupied_by': None},
                    'target_lap_caddy': {'name': 'Bahía 2.5" SATA', 'occupied_by': None},
                    'target_lap_cooling': {'name': 'Circuito Térmico', 'occupied_by': None},
                    'target_lap_optical': {'name': 'Bahía Óptica', 'occupied_by': None}
                }
            }
        }
        self.active_machine = 'desktop'

    def set_active_machine(self, machine_type: str):
        if machine_type in self.machines:
            self.active_machine = machine_type
            self.reset_machine(machine_type)

    def reset_machine(self, machine_type: str = None):
        target = machine_type or self.active_machine
        for s in self.machines[target]['slots'].values():
            s['occupied_by'] = None

    def validate_and_place(self, part_id: str, slot_id: str) -> dict:
        """
        Valida rigurosamente si una pieza física encaja en la ranura seleccionada.
        """
        m = self.machines[self.active_machine]
        part = m['parts'].get(part_id)
        slot = m['slots'].get(slot_id)

        if not part:
            return {'success': False, 'reason': f"Componente '{part_id}' no reconocido en esta máquina."}
        if not slot:
            return {'success': False, 'reason': f"Ranura '{slot_id}' no reconocida en este chasis."}

        # Verificación de prelación (ej: disipador requiere procesador instalado primero)
        if part['requires']:
            req_id = part['requires']
            req_part = m['parts'][req_id]
            req_slot = req_part['valid_slot']
            if m['slots'][req_slot]['occupied_by'] != req_id:
                return {
                    'success': False,
                    'error_type': 'sequence_error',
                    'reason': f"¡Error de secuencia técnica! Debes instalar primero '{req_part['name']}' antes de montar '{part['name']}'."
                }

        # Validación física estricta de ranura
        if slot_id != part['valid_slot']:
            valid_slot_name = m['slots'][part['valid_slot']]['name']
            return {
                'success': False,
                'error_type': 'incompatible_slot',
                'reason': f"❌ ¡Incompatibilidad física! No puedes colocar '{part['name']}' en '{slot['name']}'. Su ranura técnica correcta es: '{valid_slot_name}' ({part['desc']})."
            }

        # Comprobar si ya está ocupada
        if slot['occupied_by'] is not None and slot['occupied_by'] != part_id:
            return {
                'success': False,
                'error_type': 'slot_occupied',
                'reason': f"La ranura '{slot['name']}' ya se encuentra ocupada por otro componente."
            }

        # Éxito: asignar pieza al slot
        slot['occupied_by'] = part_id

        # Comprobar si todas las piezas están instaladas
        all_done = all(s['occupied_by'] is not None for s in m['slots'].values())

        return {
            'success': True,
            'part_id': part_id,
            'slot_id': slot_id,
            'part_name': part['name'],
            'slot_name': slot['name'],
            'all_completed': all_done,
            'message': f"✅ '{part['name']}' instalado correctamente en '{slot['name']}'."
        }


if __name__ == '__main__':
    sim = HardwarePlacementSimulator()
    print("Probando validador de ranuras en Python...")
    # Prueba errónea
    err = sim.validate_and_place('part_ram', 'target_gpu')
    print("Prueba de error (RAM en GPU):", err['reason'])
    # Prueba correcta
    ok = sim.validate_and_place('part_cpu', 'target_cpu')
    print("Prueba de éxito (CPU en Socket):", ok['message'])
