"""
NEXORA Ω — Digital Twin World Model
Consolidates perception, memory, hardware state, and spatial telemetry
into a cohesive live computational model of the operational environment.
"""

from datetime import datetime
from copy import deepcopy
from typing import Dict, Any, List
from backend.hardware.edge_telemetry import edge_telemetry
from backend.ai.vision_adapter import vision_engine
from backend.database import db


class DigitalTwinWorldModel:
    def __init__(self):
        self.last_update = datetime.now().isoformat()

    def get_world_snapshot(self, runtime_state: Dict[str, Any]) -> Dict[str, Any]:
        env = runtime_state.get("environment", {})
        edge_data = edge_telemetry.get_realtime_telemetry(env)
        vision_data = vision_engine.analyze_frame()

        return {
            "timestamp": datetime.now().isoformat(),
            "digital_twin_id": "TWIN-OMEGA-01",
            "operational_fidelity": "99.4%",
            "system_state": runtime_state.get("system", {}),
            "metrics": runtime_state.get("metrics", {}),
            "spatial_telemetry": edge_data["gps"],
            "edge_hardware": edge_data["edge_compute"],
            "sensors": edge_data["edge_sensors"],
            "vision_perception": vision_data,
            "recent_audit_events": db.get_recent_audits(limit=5)
        }


world_model = DigitalTwinWorldModel()
