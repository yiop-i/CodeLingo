"""
HARDWARE_MAINTENANCE.PY - Simulador 4 en Python: Limpieza y Mantenimiento Técnico
Cálculo termodinámico de disipación de calor, nivel de polvo y física de pasta térmica.
"""

class HardwareMaintenanceSimulator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dust_percent = 100       # 100% muy sucio -> 0% impecable
        self.paste_dry_percent = 100  # 100% pasta seca petrificada -> 0% limpia
        self.fresh_paste_applied = False
        self.heatsink_mounted = True
        self.screws_tightened = True
        return self.get_telemetry()

    def get_telemetry(self) -> dict:
        """Calcula temperatura de CPU (°C) y ruido acústico (dB) en tiempo real"""
        temp = 95
        noise = 58

        if self.dust_percent < 50:
            temp -= 15
            noise -= 10
        if self.dust_percent == 0:
            temp -= 20
            noise -= 15

        if not self.heatsink_mounted:
            temp = 100 # Peligro de apagón térmico sin disipador
            noise = 12
        elif self.fresh_paste_applied and self.screws_tightened:
            temp = 31 # Temperatura óptima en reposo
            noise = 19 # Silencioso

        return {
            'dust_percent': self.dust_percent,
            'dust_status': 'Impecable' if self.dust_percent == 0 else ('Poco Polvo' if self.dust_percent < 50 else 'Muy Sucio'),
            'cpu_temp': temp,
            'temp_status': 'Óptima' if temp <= 45 else ('Media' if temp < 75 else 'Recalentado'),
            'fan_noise_db': noise,
            'noise_status': 'Silencioso' if noise <= 25 else 'Turbina Ruidosa',
            'heatsink_mounted': self.heatsink_mounted,
            'screws_tightened': self.screws_tightened,
            'paste_dry_percent': self.paste_dry_percent,
            'fresh_paste_applied': self.fresh_paste_applied
        }

    def apply_tool(self, tool_name: str) -> dict:
        """
        Ejecuta la acción de una herramienta técnica:
        'blower', 'brush', 'screwdriver', 'alcohol', 'paste'
        """
        tool = tool_name.lower()
        msg = ""
        success = True

        if tool == "blower":
            if self.dust_percent > 0:
                self.dust_percent = max(0, self.dust_percent - 35)
                msg = "💨 ¡Ráfaga de aire comprimido disparada! Aspas girando y polvo expulsado."
            else:
                msg = "Los ventiladores y aletas ya están completamente libres de polvo."

        elif tool == "brush":
            if self.dust_percent > 0:
                self.dust_percent = max(0, self.dust_percent - 40)
                msg = "🖌️ Brocha antiestática pasada por ranuras y pistas. Pelusa barrida."
            else:
                msg = "La placa base ya está limpia."

        elif tool == "screwdriver":
            if self.heatsink_mounted:
                self.screws_tightened = not self.screws_tightened
                if not self.screws_tightened:
                    self.heatsink_mounted = False
                    msg = "🪛 Tornillos en cruz aflojados. Disipador levantado. Procesador visible."
                else:
                    msg = "🪛 Tornillos apretados firmemente en patrón de cruz."
            else:
                self.heatsink_mounted = True
                self.screws_tightened = True
                msg = "🪛 Disipador colocado sobre el CPU y tornillos apretados."

        elif tool == "alcohol":
            if self.heatsink_mounted:
                success = False
                msg = "Primero debes desatornillar y levantar el disipador para acceder a la pasta térmica."
            elif self.paste_dry_percent > 0:
                self.paste_dry_percent = 0
                msg = "🧽 Pasta térmica seca disuelta al 100%. El IHS quedó brillante con acabado espejo."
            else:
                msg = "El IHS del procesador ya está totalmente limpio y desengrasado."

        elif tool == "paste":
            if self.heatsink_mounted:
                success = False
                msg = "Retira el disipador antes de aplicar la pasta térmica."
            elif self.paste_dry_percent > 0:
                success = False
                msg = "¡Error de mantenimiento! No apliques pasta nueva sobre la pasta vieja reseca. Límpiala primero con alcohol."
            elif not self.fresh_paste_applied:
                self.fresh_paste_applied = True
                msg = "🧴 Gota calibrada de pasta térmica de alta conductividad aplicada en el centro del procesador."
            else:
                msg = "La pasta térmica fresca ya ha sido aplicada."

        else:
            success = False
            msg = f"Herramienta '{tool_name}' no reconocida."

        telemetry = self.get_telemetry()
        return {
            'success': success,
            'message': msg,
            'telemetry': telemetry
        }


if __name__ == '__main__':
    sim = HardwareMaintenanceSimulator()
    print("Probando Simulador de Mantenimiento en Python...")
    print("Telemetría inicial:", sim.get_telemetry())
    print(sim.apply_tool("blower")['message'])
    print(sim.apply_tool("screwdriver")['message'])
    print(sim.apply_tool("alcohol")['message'])
    print(sim.apply_tool("paste")['message'])
    print(sim.apply_tool("screwdriver")['message'])
    print("Telemetría final:", sim.get_telemetry())
