"""
HW_UPGRADE.PY - SIMULADOR 3 DE UPGRADES Y CAMBIO DE COMPONENTES OBSOLETOS EN PYTHON
Gestión de órdenes de clientes, desmontaje de piezas viejas, repuestos nuevos y benchmarks
"""

class HardwareUpgradeSimulator:
    def __init__(self):
        self.cases = {
            "desktop": {
                "client": "Marcos R. (Gamer & Creador de Contenido)",
                "problem": "Mi PC tarda 3 minutos en prender, los juegos van a tirones (22 FPS) y el disco duro hace un ruido mecánico insoportable. Necesito un upgrade urgente.",
                "slots": {
                    "storage": {
                        "old_name": "HDD Seagate 500GB 5400RPM Lento",
                        "new_name": "SSD Samsung 990 Pro 2TB NVMe 7450MB/s",
                        "state": "old" # old -> empty -> new
                    },
                    "ram": {
                        "old_name": "1x 8GB DDR4 2133MHz Verde Genérica",
                        "new_name": "32GB (2x16GB) Corsair DDR5 6000MHz RGB",
                        "state": "old"
                    },
                    "gpu": {
                        "old_name": "NVIDIA GeForce GTX 1050 Ti 4GB (Monoventilador)",
                        "new_name": "NVIDIA GeForce RTX 4080 Super 16GB Triple Fan",
                        "state": "old"
                    }
                }
            },
            "laptop": {
                "client": "Elena G. (Diseñadora & Trabajo Remoto)",
                "problem": "Mi notebook hierve en las piernas, la batería solo dura 10 minutos y se congela al abrir Photoshop. Necesito batería nueva, más RAM y un disco rápido.",
                "slots": {
                    "battery": {
                        "old_name": "Batería Li-Ion Degradada (Hinchada 15% vida útil)",
                        "new_name": "Batería Original 5200mAh 4 Celdas Nueva",
                        "state": "old"
                    },
                    "ram": {
                        "old_name": "SO-DIMM 4GB DDR4 2133MHz Lenta",
                        "new_name": "SO-DIMM 16GB DDR4 3200MHz Kingston",
                        "state": "old"
                    },
                    "cooling": {
                        "old_name": "Disipador Térmico con pasta seca petrificada",
                        "new_name": "Sistema Térmico Limpio con Pasta Fresca",
                        "state": "old"
                    }
                }
            }
        }

    def unmount_part(self, case_key: str, slot_key: str) -> dict:
        case = self.cases.get(case_key)
        if not case or slot_key not in case["slots"]:
            return {"success": False, "message": "Ranura no encontrada"}

        slot = case["slots"][slot_key]
        if slot["state"] != "old":
            return {"success": False, "message": "Solo puedes desmontar componentes viejos instalados."}

        slot["state"] = "empty"
        bench = self.calculate_benchmarks(case_key)
        return {
            "success": True,
            "message": f"⬇ {slot['old_name']} desatornillado y colocado en la bandeja de reciclaje.",
            "state": "empty",
            "benchmarks": bench
        }

    def install_upgrade(self, case_key: str, slot_key: str) -> dict:
        case = self.cases.get(case_key)
        if not case or slot_key not in case["slots"]:
            return {"success": False, "message": "Ranura no encontrada"}

        slot = case["slots"][slot_key]
        if slot["state"] != "empty":
            return {"success": False, "message": "Debes desmontar la pieza vieja primero antes de colocar el repuesto."}

        slot["state"] = "new"
        bench = self.calculate_benchmarks(case_key)
        all_new = all(s["state"] == "new" for s in case["slots"].values())

        return {
            "success": True,
            "message": f"✅ ¡Upgrade completado! {slot['new_name']} instalado en el equipo.",
            "state": "new",
            "benchmarks": bench,
            "mission_completed": all_new
        }

    def calculate_benchmarks(self, case_key: str) -> dict:
        case = self.cases.get(case_key)
        if not case:
            return {}

        slots = case["slots"]

        if case_key == "desktop":
            fps = 22
            boot_time = 180
            ram_gb = 8

            if slots["gpu"]["state"] == "new":
                fps = 145
            if slots["storage"]["state"] == "new":
                boot_time = 7
            if slots["ram"]["state"] == "new":
                ram_gb = 32

            return {
                "fps": f"{fps} FPS",
                "fps_percent": min(100, int((fps / 150) * 100)),
                "boot_time": f"{boot_time} segundos",
                "boot_percent": max(5, int((1 - boot_time / 180) * 100)),
                "ram": f"{ram_gb} GB",
                "ram_percent": int((ram_gb / 32) * 100)
            }
        else:
            battery = "6.5 horas" if slots["battery"]["state"] == "new" else "12 minutos"
            bat_percent = 100 if slots["battery"]["state"] == "new" else 10
            ram_gb = 16 if slots["ram"]["state"] == "new" else 4
            cooling_status = "Frío (32°C)" if slots["cooling"]["state"] == "new" else "Recalentado (92°C)"

            return {
                "battery": battery,
                "battery_percent": bat_percent,
                "ram": f"{ram_gb} GB",
                "ram_percent": int((ram_gb / 16) * 100),
                "cooling": cooling_status
            }
