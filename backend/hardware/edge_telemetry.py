"""
NEXORA Ω — Hardware Edge Telemetry & Real-Time GPS Engine
Simulates and connects to:
- Real-Time GNSS / GPS Satellite telemetry (Lat, Lon, Alt, Speed, Fix)
- ESP32 Multimodal Edge Array (Gas MQ-2, Vibration Piezo, DHT22 Temp/Humidity)
- Edge compute resource metrics (CPU, RAM, VRAM, Thermal)
"""

import math
import random
from datetime import datetime
from typing import Dict, Any


class EdgeHardwareTelemetry:
    def __init__(self):
        # Base coordinates: Center of New Delhi / Tech Hub
        self.base_lat = 28.6139
        self.base_lon = 77.2090
        self.altitude = 216.4
        self.speed_kmh = 0.0
        self.satellites = 14
        self.step = 0

    def get_realtime_telemetry(self, current_env: Dict[str, Any]) -> Dict[str, Any]:
        self.step += 1

        # Simulate realistic micro-orbital / vehicle waypoint movement
        lat_offset = math.sin(self.step * 0.05) * 0.003
        lon_offset = math.cos(self.step * 0.05) * 0.003

        current_lat = round(self.base_lat + lat_offset, 6)
        current_lon = round(self.base_lon + lon_offset, 6)
        current_alt = round(self.altitude + math.sin(self.step * 0.1) * 2.5, 1)
        current_speed = round(abs(math.sin(self.step * 0.08)) * 18.5, 1)

        # Edge hardware CPU/RAM loads
        cpu_load = round(18.0 + abs(math.sin(self.step * 0.2)) * 14.0, 1)
        ram_mb = 1420
        ram_percent = round(38.0 + (math.sin(self.step * 0.1) * 4.0), 1)

        return {
            "timestamp": datetime.now().isoformat(),
            "gps": {
                "latitude": current_lat,
                "longitude": current_lon,
                "altitude_meters": current_alt,
                "speed_kmh": current_speed,
                "satellites_locked": self.satellites,
                "fix_status": "3D_DGPS_FIX",
                "hdop": 0.8
            },
            "edge_compute": {
                "cpu_utilization_pct": cpu_load,
                "ram_usage_pct": ram_percent,
                "ram_used_mb": ram_mb,
                "board_temp_celsius": round(current_env.get("temperature", 26.4) + 6.2, 1),
                "battery_health_pct": 98.2,
                "battery_voltage": 12.4
            },
            "edge_sensors": {
                "temperature": current_env.get("temperature", 26.4),
                "humidity": current_env.get("humidity", 48.2),
                "gas_ppm": current_env.get("gas", 12.0),
                "vibration_g": current_env.get("vibration", 0.12),
                "ambient_lux": current_env.get("light", 72.0)
            }
        }


edge_telemetry = EdgeHardwareTelemetry()
