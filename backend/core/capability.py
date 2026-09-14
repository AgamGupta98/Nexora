"""
NEXORA Ω — Hierarchical Capability Graph & Adaptive Substitution Engine
Organizes all system competencies across:
- Perception (Vision, Thermal, Gas, Vibration, Acoustic, GPS)
- Reasoning (Planning, Task Decomposition, Consensus, Self-Model)
- Communication (WiFi, Bluetooth, MQTT, WebSocket, RF-Mesh)
- Actuation (Servo, Motor, Relay, GPIO, Quarantine-Switch)
- Resilience (Self-Healing, Backup-Path, Sandbox-Isolation)
"""

from typing import Dict, List, Any, Optional


class HierarchicalCapabilityRegistry:
    def __init__(self):
        self.capabilities: Dict[str, Dict[str, Any]] = {
            # --- Perception Competencies ---
            "vision.object_detection": {
                "name": "Object Detection",
                "category": "Perception",
                "providers": ["vision.local", "onnx.yolo"],
                "status": "available",
                "offline": True,
                "latency_ms": 72
            },
            "vision.scene_understanding": {
                "name": "Scene Understanding",
                "category": "Perception",
                "providers": ["vision.local"],
                "status": "available",
                "offline": True,
                "latency_ms": 110
            },
            "perception.sensor_fusion": {
                "name": "Multimodal Sensor Fusion",
                "category": "Perception",
                "providers": ["sensor.engine", "esp32.telemetry"],
                "status": "available",
                "offline": True,
                "latency_ms": 18
            },
            "perception.gps_tracking": {
                "name": "Geospatial GPS Telemetry",
                "category": "Perception",
                "providers": ["gps.satellite", "gnss.receiver"],
                "status": "available",
                "offline": True,
                "latency_ms": 25
            },
            "perception.anomaly_detection": {
                "name": "Temporal Anomaly Detection",
                "category": "Perception",
                "providers": ["predictor.local", "isolation_forest"],
                "status": "available",
                "offline": True,
                "latency_ms": 32
            },

            # --- Reasoning Competencies ---
            "reasoning.planning": {
                "name": "Hierarchical Task Planner",
                "category": "Reasoning",
                "providers": ["planner.core", "llm.local"],
                "status": "available",
                "offline": True,
                "latency_ms": 45
            },
            "reasoning.conversation": {
                "name": "Natural Language Cognitive Agent",
                "category": "Reasoning",
                "providers": ["llm.local", "ollama.local", "cloud.llm"],
                "status": "available",
                "offline": True,
                "latency_ms": 120
            },
            "reasoning.risk_prediction": {
                "name": "Predictive Risk Modeling",
                "category": "Reasoning",
                "providers": ["predictor.local"],
                "status": "available",
                "offline": True,
                "latency_ms": 41
            },
            "reasoning.self_model": {
                "name": "Introspection & Self-Diagnostics",
                "category": "Reasoning",
                "providers": ["self_model.engine"],
                "status": "available",
                "offline": True,
                "latency_ms": 15
            },

            # --- Communication Competencies ---
            "comm.wifi_rf": {
                "name": "WiFi & RF High-Throughput",
                "category": "Communication",
                "providers": ["comm.primary"],
                "status": "available",
                "offline": True,
                "latency_ms": 8
            },
            "comm.aux_mesh": {
                "name": "Auxiliary Resilient Mesh Link",
                "category": "Communication",
                "providers": ["comm.backup"],
                "status": "available",
                "offline": True,
                "latency_ms": 14
            },
            "comm.websocket_stream": {
                "name": "Full-Duplex Telemetry WebSocket",
                "category": "Communication",
                "providers": ["ws.broadcaster"],
                "status": "available",
                "offline": True,
                "latency_ms": 5
            },

            # --- Actuation & Safety Competencies ---
            "actuation.quarantine": {
                "name": "Zero-Trust Node Quarantine Switch",
                "category": "Actuation",
                "providers": ["quarantine.core"],
                "status": "available",
                "offline": True,
                "latency_ms": 10
            },
            "actuation.recovery": {
                "name": "Autonomous Self-Healing Failover",
                "category": "Resilience",
                "providers": ["recovery.core"],
                "status": "available",
                "offline": True,
                "latency_ms": 30
            },
            "actuation.simulation_sandbox": {
                "name": "Digital Twin Comparative Sandbox",
                "category": "Simulation",
                "providers": ["simulator.core"],
                "status": "available",
                "offline": True,
                "latency_ms": 22
            }
        }

    def all(self) -> List[Dict[str, Any]]:
        result = []
        for cap_id, data in self.capabilities.items():
            result.append({"id": cap_id, **data})
        return result

    def get(self, capability: str) -> Optional[Dict[str, Any]]:
        return self.capabilities.get(capability)

    def providers(self, capability: str) -> List[str]:
        item = self.get(capability)
        return item["providers"] if item else []

    def disable_provider(self, provider_id: str):
        """
        Dynamically disables a degraded or quarantined provider across the capability graph,
        marking capabilities degraded if no healthy provider remains.
        """
        for cap in self.capabilities.values():
            if provider_id in cap["providers"]:
                cap["providers"] = [p for p in cap["providers"] if p != provider_id]
                if not cap["providers"]:
                    cap["status"] = "degraded"

    def substitute_provider(self, capability: str, fallback_provider: str) -> bool:
        """
        Performs adaptive substitution when primary provider fails.
        """
        item = self.get(capability)
        if not item:
            return False
        if fallback_provider not in item["providers"]:
            item["providers"].append(fallback_provider)
        item["status"] = "available"
        return True

    def add_provider(self, capability: str, provider: str) -> bool:
        item = self.get(capability)
        if not item:
            return False
        if provider not in item["providers"]:
            item["providers"].append(provider)
        item["status"] = "available"
        return True


capability_registry = HierarchicalCapabilityRegistry()
