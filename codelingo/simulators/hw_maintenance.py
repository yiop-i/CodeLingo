"""
HW_MAINTENANCE.PY - SIMULADOR 4 DE LIMPIEZA Y MANTENIMIENTO TÉCNICO EN PYTHON
Máquina de estados de disipación de polvo, pasta térmica, alcohol isopropílico y telemetría
"""

class HardwareMaintenanceSimulator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dust_level = 100 # 100% sucio -> 0% limpio
        self.paste_dry_percent = 100 # 100% pasta vieja seca -> 0% limpia
        self.fresh_paste_applied = False
        self.heatsink_mounted = True
        self.screws_tightened = True
        return self.get_telemetry()

    def apply_tool(self, tool: str) -> dict:
        tool = (tool or "").lower()

        if tool == "blower":
            # Soplar con aire comprimido
            self.dust_level = max(0, self.dust_level - 35)
            telemetry = self.get_telemetry()
            return {
                "success": True,
                "tool": "blower",
                "message": "💨 ¡Ráfaga de aire disparada a alta presión! Ventiladores girando y polvo expulsado.",
                "telemetry": telemetry
            }

        elif tool == "brush":
            # Barrer con brocha antiestática
            self.dust_level = max(0, self.dust_level - 40)
            telemetry = self.get_telemetry()
            return {
                "success": True,
                "tool": "brush",
                "message": "🖌️ Brocha antiestática pasada por ranuras y circuitos. Pelusa removida.",
                "telemetry": telemetry
            }

        elif tool == "screwdriver":
            # Aflojar o apretar tornillos en cruz del disipador
            if self.screws_tightened and self.heatsink_mounted:
                self.screws_tightened = False
                self.heatsink_mounted = False
                telemetry = self.get_telemetry()
                return {
                    "success": True,
                    "tool": "screwdriver",
                    "action": "unmounted",
                    "message": "🪛 Tornillos en cruz aflojados. Disipador levantado. Procesador visible con pasta seca.",
                    "telemetry": telemetry
                }
            else:
                self.screws_tightened = True
                self.heatsink_mounted = True
                telemetry = self.get_telemetry()
                return {
                    "success": True,
                    "tool": "screwdriver",
                    "action": "mounted",
                    "message": "🪛 Disipador colocado sobre el procesador y tornillos apretados en forma de cruz.",
                    "telemetry": telemetry
                }

        elif tool == "alcohol":
            # Limpiar pasta térmica vieja con alcohol isopropílico 99.9%
            if self.heatsink_mounted:
                return {
                    "success": False,
                    "tool": "alcohol",
                    "message": "Primero debes aflojar los tornillos y retirar el disipador para acceder a la pasta térmica."
                }

            self.paste_dry_percent = 0
            telemetry = self.get_telemetry()
            return {
                "success": True,
                "tool": "alcohol",
                "message": "🧽 Pasta térmica seca completamente disuelta. El difusor metálico (IHS) quedó con acabado espejo.",
                "telemetry": telemetry
            }

        elif tool == "paste":
            # Aplicar pasta térmica fresca de alta conductividad
            if self.heatsink_mounted:
                return {
                    "success": False,
                    "tool": "paste",
                    "message": "Retira el disipador antes de aplicar la pasta térmica."
                }

            if self.paste_dry_percent > 0:
                return {
                    "success": False,
                    "tool": "paste",
                    "message": "¡Error de procedimiento! No apliques pasta nueva sobre la pasta vieja reseca. Límpiala primero con alcohol isopropílico."
                }

            self.fresh_paste_applied = True
            telemetry = self.get_telemetry()
            return {
                "success": True,
                "tool": "paste",
                "message": "🧴 Gota perfecta de pasta térmica nueva aplicada sobre el centro del procesador.",
                "telemetry": telemetry
            }

        return {"success": False, "message": f"Herramienta desconocida: {tool}"}

    def get_telemetry(self) -> dict:
        temp = 95
        noise = 58

        if self.dust_level < 50:
            temp -= 15
            noise -= 10
        if self.dust_level == 0:
            temp -= 20
            noise -= 15

        if self.fresh_paste_applied and self.heatsink_mounted and self.screws_tightened:
            temp = 31
            noise = 19

        dust_desc = "Impecable" if self.dust_level == 0 else ("Poco Polvo" if self.dust_level < 50 else "Muy Sucio")
        temp_desc = "Óptima" if temp <= 45 else ("Media" if temp < 75 else "Recalentado")
        noise_desc = "Silencioso" if noise <= 25 else "Turbina Ruidosa"

        return {
            "dust": f"{self.dust_level}% ({dust_desc})",
            "dust_val": self.dust_level,
            "temp": f"{temp}°C ({temp_desc})",
            "temp_val": temp,
            "noise": f"{noise} dB ({noise_desc})",
            "noise_val": noise,
            "heatsink_mounted": self.heatsink_mounted,
            "screws_tightened": self.screws_tightened,
            "fresh_paste_applied": self.fresh_paste_applied,
            "clean_complete": self.dust_level == 0 and self.fresh_paste_applied and self.heatsink_mounted
        }
