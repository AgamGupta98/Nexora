"""
NEXORA Ω — Universal Adaptive Intelligence Runtime
FastAPI Production Server with Real-Time WebSockets, SQLite Persistence,
NIST AI RMF Governance, Memory Fabric, and Digital Twin.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict

from backend.state import runtime
from backend.database import db
from backend.websocket_manager import ws_manager
from backend.core.orchestrator import orchestrator
from backend.core.capability import capability_registry
from backend.core.memory import memory_fabric
from backend.core.self_model import self_model
from backend.core.world_model import world_model
from backend.ai.model_router import model_router
from backend.ai.anomaly import anomaly_engine
from backend.ai.prediction import prediction_engine
from backend.security.trust import trust_engine
from backend.security.quarantine import quarantine_engine
from backend.security.governance import governance_engine
from backend.recovery.recovery_engine import recovery_engine
from backend.simulation.simulator import simulation_engine
from backend.hardware.edge_telemetry import edge_telemetry
from backend.plugins.plugin_manager import plugin_manager

app = FastAPI(
    title="NEXORA Ω",
    description="Universal Adaptive Intelligence Runtime — Enterprise AI RMF Architecture",
    version="0.2.0-PRO"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Resolve directories
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    assets_dir = FRONTEND_DIR / "assets"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


# --- Pydantic Data Models ---
class Command(BaseModel):
    command: str


class TelemetryInput(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    gas: Optional[float] = None
    vibration: Optional[float] = None
    light: Optional[float] = None


class DeviceToggle(BaseModel):
    device_id: str
    action: Optional[str] = "toggle"


class ModeChange(BaseModel):
    mode: str


class ApprovalDecision(BaseModel):
    approval_id: str
    approved: bool
    operator_notes: Optional[str] = "Approved via Cyber Console"


class RouteRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_type: str = "language"
    offline_required: bool = False
    low_energy: bool = False


# Connected Fleet State
DEVICES = [
    {
        "id": "core.compute",
        "name": "Neural Compute Core",
        "type": "compute",
        "status": "online",
        "trust": 99.0,
        "energy": 18.0,
        "ip": "192.168.1.10"
    },
    {
        "id": "camera.primary",
        "name": "Primary Vision Node",
        "type": "camera",
        "status": "online",
        "trust": 98.0,
        "energy": 7.0,
        "ip": "192.168.1.24"
    },
    {
        "id": "sensor.env",
        "name": "Multimodal Environment Array",
        "type": "sensor",
        "status": "online",
        "trust": 97.0,
        "energy": 3.0,
        "ip": "192.168.1.42"
    },
    {
        "id": "comm.primary",
        "name": "Primary RF Transceiver",
        "type": "communication",
        "status": "online",
        "trust": 98.0,
        "energy": 5.0,
        "ip": "192.168.1.80"
    },
    {
        "id": "comm.backup",
        "name": "Auxiliary Mesh Link",
        "type": "communication",
        "status": "standby",
        "trust": 95.0,
        "energy": 8.0,
        "ip": "192.168.1.81"
    }
]


# --- Root & Static Routes ---
@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    index_file = FRONTEND_DIR / "index.html"
    if "text/html" in accept and index_file.exists():
        return FileResponse(str(index_file))
    return {
        "name": "NEXORA Ω",
        "status": "ONLINE",
        "version": "0.2.0-PRO",
        "dashboard": "/dashboard",
        "architecture": "NIST AI RMF Compliant Adaptive Runtime"
    }


@app.get("/dashboard")
def dashboard():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"error": "Dashboard not found"}


# --- Real-Time WebSocket Endpoint ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Initial greeting and state sync
        await websocket.send_text(json.dumps({
            "type": "SYSTEM_SYNC",
            "state": runtime.snapshot(),
            "world": world_model.get_world_snapshot(runtime.snapshot())
        }))
        while True:
            data_text = await websocket.receive_text()
            try:
                msg = json.loads(data_text)
                if msg.get("type") == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except Exception:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# --- Core State & World Model APIs ---
@app.get("/api/state")
def get_state():
    return runtime.snapshot()


@app.get("/api/world-model")
def get_world_model():
    return world_model.get_world_snapshot(runtime.snapshot())


@app.get("/api/self-model")
def get_self_model():
    return self_model.introspect(runtime.snapshot(), DEVICES, capability_registry.all())


@app.get("/api/memory")
def get_memory_snapshot():
    return memory_fabric.snapshot()


@app.get("/api/gps")
def get_gps_telemetry():
    return edge_telemetry.get_realtime_telemetry(runtime.data["environment"])["gps"]


@app.get("/api/plugins")
def get_plugins():
    return plugin_manager.list_plugins()


@app.get("/api/capabilities")
def get_capabilities():
    return capability_registry.all()


@app.get("/api/models")
def get_models():
    return model_router.available()


@app.get("/api/devices")
def get_devices():
    return DEVICES


# --- Cognitive Command Orchestrator ---
@app.post("/api/command")
async def command(payload: Command):
    result = orchestrator.process(payload.command)

    # Broadcast update to all WebSocket clients
    await ws_manager.broadcast({
        "type": "COMMAND_RESULT",
        "result": result,
        "state": runtime.snapshot()
    })

    return {
        "result": result,
        "state": runtime.snapshot()
    }


# --- Telemetry & Sensor Drift Injection ---
@app.post("/api/telemetry")
async def update_telemetry(payload: TelemetryInput):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        runtime.update_environment(**updates)

    analysis = anomaly_engine.analyze(runtime.data["environment"])
    prediction = prediction_engine.predict(
        analysis["risk"],
        len(analysis["signals"])
    )

    new_health = max(50.0, 100.0 - (analysis["risk"] * 0.25))
    new_energy = 54.0 + len(analysis["signals"]) * 6.0

    runtime.update_metrics(
        health=new_health,
        risk=analysis["risk"],
        prediction=prediction["predicted_risk"],
        energy=new_energy
    )

    if analysis["anomaly"]:
        if runtime.data["system"]["mode"] not in ["RECOVERY", "ALERT", "EMERGENCY"]:
            runtime.set_mode("ADAPTIVE")
        runtime.event(f"Sensor anomaly detected -> {', '.join(analysis['signals'])}", severity="WARNING")
    else:
        if runtime.data["system"]["mode"] == "ADAPTIVE":
            runtime.set_mode("NORMAL")

    snap = runtime.snapshot()
    await ws_manager.broadcast({
        "type": "TELEMETRY_UPDATE",
        "analysis": analysis,
        "prediction": prediction,
        "state": snap
    })

    return {
        "analysis": analysis,
        "prediction": prediction,
        "state": snap
    }


# --- Human-in-the-Loop Governance Endpoints ---
@app.get("/api/governance/approvals")
def get_approvals():
    return db.get_pending_approvals()


@app.post("/api/governance/approve")
async def resolve_approval(payload: ApprovalDecision):
    db.resolve_approval(payload.approval_id, payload.approved, resolved_by="Operator")
    status = "APPROVED" if payload.approved else "REJECTED"
    runtime.event(f"Human-in-the-loop decision -> {payload.approval_id} {status}")

    await ws_manager.broadcast({
        "type": "APPROVAL_RESOLVED",
        "approval_id": payload.approval_id,
        "status": status
    })

    return {"status": "SUCCESS", "approval_id": payload.approval_id, "decision": status}


@app.get("/api/database/audit")
def get_audit_trail():
    return db.get_recent_audits(limit=40)


# --- Simulation & Model Routing ---
@app.post("/api/simulate")
def simulate_action(action: str = "contingency_failover"):
    result = simulation_engine.simulate(action, runtime.snapshot())
    runtime.event(f"Simulation benchmark executed -> {result['selected_name']}")
    return result


@app.post("/api/model/route")
def test_model_route(payload: RouteRequest):
    candidates = model_router.candidates(payload.model_type)
    if payload.offline_required:
        candidates = [x for x in candidates if x["offline"]]

    scored = []
    for m in candidates:
        s = m["trust"] * 2 - m["latency"] * 0.1
        if payload.low_energy:
            s -= m["energy"] * 5
        if m["status"] == "online":
            s += 10
        scored.append({"model": m, "score": round(s, 2)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]["model"] if scored else None

    return {
        "selected": best,
        "candidates": scored
    }


# --- Device Isolation & Hardware Controls ---
@app.post("/api/device/toggle")
async def toggle_device(payload: DeviceToggle):
    dev = next((d for d in DEVICES if d["id"] == payload.device_id), None)
    if not dev:
        return {"error": "Device not found"}

    if payload.action == "isolate" or (payload.action == "toggle" and dev["status"] != "QUARANTINED"):
        dev["status"] = "QUARANTINED"
        dev["trust"] = 20.0
        quarantine_engine.isolate(dev["id"])
        capability_registry.disable_provider(dev["id"])
        runtime.event(f"Security isolation initiated -> {dev['id']}", severity="ALERT")
    else:
        dev["status"] = "online"
        dev["trust"] = 98.0
        quarantine_engine.release(dev["id"])
        capability_registry.add_provider("comm.wifi_rf", dev["id"])
        runtime.event(f"Device released from quarantine -> {dev['id']}")

    snap = runtime.snapshot()
    await ws_manager.broadcast({"type": "DEVICE_STATE_CHANGE", "device": dev, "state": snap})
    return {"device": dev, "state": snap}


# --- Autonomous Failure & Healing Test Triggers ---
@app.post("/api/anomaly")
async def trigger_anomaly():
    runtime.data["environment"].update({
        "temperature": 47.2,
        "gas": 71.0,
        "vibration": 0.91
    })

    analysis = anomaly_engine.analyze(runtime.data["environment"])
    prediction = prediction_engine.predict(analysis["risk"], len(analysis["signals"]))

    runtime.update_metrics(
        health=88.2,
        risk=analysis["risk"],
        prediction=prediction["predicted_risk"],
        energy=61.0
    )

    runtime.set_mode("ADAPTIVE")
    runtime.event("Environmental sensor anomaly detected", severity="WARNING")
    runtime.event(f"Signals -> {', '.join(analysis['signals'])}")
    runtime.event(f"AI Risk Projection -> {prediction['level']}")

    snap = runtime.snapshot()
    await ws_manager.broadcast({"type": "ANOMALY_TRIGGERED", "state": snap})
    return {"analysis": analysis, "prediction": prediction, "state": snap}


@app.post("/api/failure")
async def trigger_failure():
    primary = next(x for x in DEVICES if x["id"] == "comm.primary")
    backup = next(x for x in DEVICES if x["id"] == "comm.backup")

    primary["trust"] = 21.0
    primary["status"] = "QUARANTINED"
    trust_result = trust_engine.evaluate(primary["trust"])

    runtime.update_metrics(security=91.2, health=84.7, energy=58.0)
    result = recovery_engine.recover(primary["id"], backup["id"], runtime)
    backup["status"] = "online"

    snap = runtime.snapshot()
    await ws_manager.broadcast({"type": "FAILOVER_COMPLETED", "recovery": result, "state": snap})
    return {"trust": trust_result, "recovery": result, "state": snap}


@app.post("/api/reset")
async def trigger_reset():
    DEVICES[3].update({"trust": 98.0, "status": "online"})
    DEVICES[4].update({"trust": 95.0, "status": "standby"})

    quarantine_engine.release("comm.primary")
    capability_registry.add_provider("comm.wifi_rf", "comm.primary")

    runtime.data["metrics"].update({
        "health": 96.8,
        "security": 98.4,
        "risk": 39.0,
        "prediction": 82.0,
        "energy": 54.0
    })

    runtime.data["environment"].update({
        "temperature": 26.4,
        "humidity": 48.2,
        "gas": 12.0,
        "vibration": 0.12,
        "light": 72.0
    })

    runtime.data["spatial_gps"].update({
        "latitude": 28.6139,
        "longitude": 77.2090,
        "altitude": 216.4,
        "speed": 0.0,
        "satellites": 14
    })

    runtime.set_mode("NORMAL")
    runtime.data["recovery"] = {
        "active": False,
        "last_action": None,
        "status": "No recovery required"
    }

    runtime.event("Mission runtime reset to baseline operational parameters")

    snap = runtime.snapshot()
    await ws_manager.broadcast({"type": "SYSTEM_RESET", "state": snap})
    return snap
