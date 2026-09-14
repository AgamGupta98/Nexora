"""
NEXORA Ω — Plugin Registry & Sandbox Security Manager
Manages external plugins, permission manifests (camera.read, filesystem.write, etc.),
and execution sandboxing to enforce Zero-Trust access controls.
"""

from typing import Dict, Any, List, Optional


class PluginSandboxManager:
    def __init__(self):
        self.plugins: Dict[str, Dict[str, Any]] = {
            "vision.yolo": {
                "id": "vision.yolo",
                "name": "YOLO Spatial Vision Adapter",
                "version": "1.4.0",
                "capabilities": ["vision.object_detection"],
                "permissions": ["camera.read", "memory.read"],
                "offline": True,
                "status": "LOADED_SANDBOXED",
                "author": "NEXORA Core Systems"
            },
            "sensor.esp32_mqtt": {
                "id": "sensor.esp32_mqtt",
                "name": "ESP32 Multimodal Edge Driver",
                "version": "2.1.0",
                "capabilities": ["perception.sensor_fusion"],
                "permissions": ["network.local", "telemetry.write"],
                "offline": True,
                "status": "LOADED_SANDBOXED",
                "author": "Edge Fabric Team"
            },
            "gps.gnss_driver": {
                "id": "gps.gnss_driver",
                "name": "NMEA GNSS Satellite Receiver",
                "version": "1.0.2",
                "capabilities": ["perception.gps_tracking"],
                "permissions": ["serial.read", "telemetry.write"],
                "offline": True,
                "status": "LOADED_SANDBOXED",
                "author": "Geospatial Labs"
            },
            "speech.whisper_edge": {
                "id": "speech.whisper_edge",
                "name": "Edge Speech-to-Text Transcriber",
                "version": "0.9.1",
                "capabilities": ["perception.speech_stt"],
                "permissions": ["audio.record"],
                "offline": True,
                "status": "STANDBY",
                "author": "Open Source AI"
            }
        }

        # Strict Permission Matrix
        self.allowed_permissions = {
            "camera.read": True,
            "memory.read": True,
            "network.local": True,
            "telemetry.write": True,
            "serial.read": True,
            "audio.record": True,
            # Blocked by default in sandbox
            "filesystem.write": False,
            "shell.execute": False,
            "network.external": False
        }

    def list_plugins(self) -> List[Dict[str, Any]]:
        return list(self.plugins.values())

    def verify_and_sandbox(self, plugin_id: str) -> Dict[str, Any]:
        plugin = self.plugins.get(plugin_id)
        if not plugin:
            return {"valid": False, "reason": "Plugin not registered"}

        granted = []
        denied = []
        for perm in plugin.get("permissions", []):
            if self.allowed_permissions.get(perm, False):
                granted.append(perm)
            else:
                denied.append(perm)

        return {
            "plugin_id": plugin_id,
            "sandboxed": True,
            "granted_permissions": granted,
            "denied_permissions": denied,
            "security_policy": "STRICT_SANDBOX_ENFORCED"
        }


plugin_manager = PluginSandboxManager()
