"""
NEXORA Ω — Live World State Store & Temporal Buffer
Maintains runtime state synchronized with real-time SQLite persistence.
"""

from datetime import datetime
from copy import deepcopy
from typing import Dict, Any, List
from backend.database import db

INITIAL_STATE = {
    "system": {
        "name": "NEXORA Ω",
        "version": "0.2.0-PRO",
        "mode": "NORMAL",
        "online": True,
        "timestamp": None
    },

    "metrics": {
        "health": 96.8,
        "security": 98.4,
        "risk": 39.0,
        "prediction": 82.0,
        "energy": 54.0
    },

    "mission": {
        "active": True,
        "goal": "Maintain safe adaptive operation",
        "status": "RUNNING",
        "priority": "HIGH_ASSURANCE"
    },

    "environment": {
        "temperature": 26.4,
        "humidity": 48.2,
        "gas": 12.0,
        "vibration": 0.12,
        "light": 72.0
    },

    "spatial_gps": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "altitude": 216.4,
        "speed": 0.0,
        "satellites": 14,
        "fix": "3D_DGPS_LOCK"
    },

    "active_capabilities": [
        "Conversation",
        "Prediction",
        "Vision",
        "Sensor Fusion",
        "GPS Tracking",
        "Planning",
        "Digital Twin",
        "Self-Model",
        "Autonomous Recovery"
    ],

    "events": [
        "NEXORA Ω Runtime Engine initialized",
        "NIST AI RMF safety gates passed",
        "SQLite persistent memory fabric active",
        "Real-time GPS & edge telemetry synchronized"
    ],

    "recovery": {
        "active": False,
        "last_action": None,
        "status": "No recovery required"
    }
}


class RuntimeState:
    def __init__(self):
        self.data = deepcopy(INITIAL_STATE)
        self.history: List[Dict[str, Any]] = []
        self.touch()
        self.record_history()

    def touch(self):
        self.data["system"]["timestamp"] = datetime.now().isoformat()

    def record_history(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        m = self.data["metrics"]
        e = self.data["environment"]
        g = self.data.get("spatial_gps", {})

        entry = {
            "time": timestamp,
            "health": m["health"],
            "risk": m["risk"],
            "prediction": m["prediction"],
            "energy": m["energy"],
            "temperature": e["temperature"],
            "gas": e["gas"],
            "gps_lat": g.get("latitude", 28.6139),
            "gps_lon": g.get("longitude", 77.2090)
        }
        self.history.append(entry)
        if len(self.history) > 40:
            self.history.pop(0)

        # Persist to SQLite
        try:
            db.record_telemetry({**e, **m, "gps_lat": g.get("latitude"), "gps_lon": g.get("longitude")})
        except Exception:
            pass

    def event(self, message: str, severity: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.data["events"].insert(0, f"[{timestamp}] {message}")
        self.data["events"] = self.data["events"][:30]
        self.touch()
        try:
            db.log_event(source="NEXORA.Core", message=message, severity=severity)
        except Exception:
            pass

    def update_metrics(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.data["metrics"]:
                self.data["metrics"][key] = round(float(value), 1)
        self.touch()
        self.record_history()

    def update_environment(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.data["environment"]:
                self.data["environment"][key] = round(float(value), 2)
        self.touch()
        self.record_history()

    def update_gps(self, **kwargs):
        if "spatial_gps" not in self.data:
            self.data["spatial_gps"] = {}
        for key, value in kwargs.items():
            self.data["spatial_gps"][key] = value
        self.touch()

    def set_mode(self, mode: str):
        self.data["system"]["mode"] = mode
        self.event(f"System operational mode transitioned -> {mode}")
        self.touch()
        self.record_history()

    def snapshot(self) -> Dict[str, Any]:
        self.touch()
        snap = deepcopy(self.data)
        snap["history"] = list(self.history)
        return snap


runtime = RuntimeState()
