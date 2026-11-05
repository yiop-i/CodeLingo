"""
HW_PLACEMENT.PY - SIMULADOR 2 DE MONTAJE Y UBICACIÓN EN RANURA EN PYTHON
Validación estricta de ranuras, prelación mecánica y reglas de compatibilidad física
"""

class HardwarePlacementSimulator:
    def __init__(self):
        self.rules = {
            "desktop": {
                "part_cpu": {
                    "name": "Intel Core i9-14900K",
                    "valid_slot": "target_cpu",
                    "slot_desc": "Socket LGA1700",
                    "requires": None
                },
                "part_cooler": {
                    "name": "Disipador de Torre con Heatpipes",
                    "valid_slot": "target_cooler",
                    "slot_desc": "Soporte y Backplate del CPU",
                    "requires": "part_cpu"
                },
                "part_ram": {
                    "name": "Kit 32GB DDR5 RGB (Dual-Channel)",
                    "valid_slot": "target_ram",
                    "slot_desc": "Ranuras DIMM 2 y 4",
                    "requires": None
                },
                "part_gpu": {
                    "name": "NVIDIA RTX 4080 Super 16GB",
                    "valid_slot": "target_gpu",
                    "slot_desc": "Ranura PCIe 5.0 x16 Blindada",
                    "requires": None
                },
                "part_m2": {
                    "name": "SSD Samsung 990 Pro 2TB NVMe",
                    "valid_slot": "target_m2",
                    "slot_desc": "Zócalo M.2 PCIe 4.0",
                    "requires": None
                },
                "part_psu": {
                    "name": "Fuente Corsair 850W Gold",
                    "valid_slot": "target_psu",
                    "slot_desc": "Bahía de Fuente de Poder",
                    "requires": None
                }
            },
            "notebook": {
                "lap_battery": {
                    "name": "Batería Li-Ion 5200mAh",
                    "valid_slot": "target_lap_battery",
                    "slot_desc": "Bahía de Batería con Pestillos Lock",
                    "requires": None
                },
                "lap_sodimm": {
                    "name": "Memoria RAM SO-DIMM 16GB (45°)",
                    "valid_slot": "target_lap_sodimm",
                    "slot_desc": "Ranura SO-DIMM (Ángulo a 45°)",
                    "requires": None
                },
                "lap_heatpipe": {
                    "name": "Heatpipe de Cobre & Turbina Blower",
                    "valid_slot": "target_lap_cooling",
                    "slot_desc": "Circuito Térmico del CPU/GPU",
                    "requires": None
                },
                "lap_caddy": {
                    "name": "SSD 2.5\" SATA en Caddy",
                    "valid_slot": "target_lap_caddy",
                    "slot_desc": "Bahía 2.5\" SATA",
                    "requires": None
                },
                "lap_optical": {
                    "name": "Lectora DVD-RW Slim",
                    "valid_slot": "target_lap_optical",
                    "slot_desc": "Bahía de Unidad Óptica Slim",
                    "requires": None
                }
            }
        }

        self.state = {
            "desktop": {},
            "notebook": {}
        }

    def validate_and_place(self, machine_type: str, part_id: str, slot_id: str) -> dict:
        machine = self.rules.get(machine_type)
        if not machine or part_id not in machine:
            return {"success": False, "message": "Componente desconocido o no compatible con este equipo."}

        part_info = machine[part_id]

        # Validación de prelación (ej: disipador requiere CPU previo)
        if part_info["requires"]:
            req_id = part_info["requires"]
            if not self.state[machine_type].get(req_id):
                req_name = machine[req_id]["name"]
                return {
                    "success": False,
                    "error_type": "sequence_error",
                    "message": f"¡Error de secuencia técnica! Debes instalar primero el {req_name} antes de montar este componente."
                }

        # Validación estricta de ranura
        if slot_id == part_info["valid_slot"]:
            self.state[machine_type][part_id] = True
            all_parts = list(machine.keys())
            complete = all(self.state[machine_type].get(p) for p in all_parts)

            return {
                "success": True,
                "message": f"✅ {part_info['name']} ensamblado con éxito en {part_info['slot_desc']}.",
                "part_name": part_info["name"],
                "slot_desc": part_info["slot_desc"],
                "is_complete": complete
            }
        else:
            return {
                "success": False,
                "error_type": "slot_mismatch",
                "message": f"❌ ¡Incompatibilidad física! No puedes colocar {part_info['name']} en esa ranura. Su ubicación técnica correcta es: {part_info['slot_desc']}."
            }

    def reset(self, machine_type: str):
        if machine_type in self.state:
            self.state[machine_type] = {}
        return {"status": "reset", "machine": machine_type}
