# NEXORA Ω — Universal Adaptive Intelligence Runtime

An adaptive, resilient, offline-first autonomous runtime architecture equipped with dynamic model routing, self-healing capability graph, trust evaluation, simulation-before-action engine, and a sci-fi cybernetic Command Center HUD.

---

## ⚡ Quick Start on Windows (1-Click)

FastAPI and Uvicorn are already installed in your Python environment. You can start NEXORA instantly:

### Method 1: One-Click Launcher (Recommended)
Double-click **`run_nexora.bat`** in the `NEXORA-OMEGA/` folder (or at project root).

### Method 2: Terminal / PowerShell
```powershell
cd NEXORA-OMEGA
python -m uvicorn backend.main:app --reload --port 8000
```

Open your browser:
- 🌐 **Holographic Command Center**: [http://localhost:8000](http://localhost:8000)
- 📑 **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Fully Automatic Prototype Features

1. **🤖 Autonomous Autopilot Mode (`AUTOPILOT` Toggle)**:
   - Click the green **AUTOPILOT** switch in the top header.
   - The autonomous daemon simulates continuous realistic environmental telemetry drift every 3.5 seconds.
   - Automatically executes periodic energy optimizations, safety audits, and predictive risk evaluations without requiring manual operator intervention.

2. **🗣️ AI Voice Synthesizer & Speech Recognition (`🎙️ MIC` + `🗣️ VOICE ON`)**:
   - **Voice Output**: Speaks status alerts, anomaly warnings, and AI reasoning in a futuristic voice.
   - **Voice Input**: Click the **🎙️** button on the tactical input bar and speak your command naturally (e.g., *"system status"*, *"optimize energy"*).

3. **🌀 Dual Holographic 3D Visualizer**:
   - **Arc Reactor**: Particle orbits, rotating containment rings, and core energy flares that accelerate and change hue with system threat levels.
   - **3D Digital Twin**: Interactive rotating 3D wireframe mesh with real-time green/cyan telemetry sensors pulsating on vertices.

4. **🎛️ Live Sensor Sliders (Interactive Drift Injection)**:
   - Drag **TEMP INJECT** (15°C - 65°C), **GAS INJECT** (5 - 95 ppm), or **VIB INJECT** (0.05g - 1.30g).
   - Watch the UI instantly transition to `ADAPTIVE` or `ALERT` mode, elevating the AI prediction index and triggering safety gates.

5. **📈 Real-Time Multi-Channel Oscilloscope**:
   - Smooth Canvas graph rendering live 30-frame temporal history of **Health (Green)**, **Risk (Red)**, and **Temperature (Cyan)**.

6. **⚡ Self-Healing Failover (`⚡ FAILOVER & HEAL`)**:
   - Simulates primary transceiver failure.
   - Zero-trust quarantine instantly isolates the degraded node.
   - Simulator validates backup communication channel.
   - System autonomously reroutes traffic to `comm.backup` and resumes operation in `RECOVERY` mode.

7. **🛡️ Dynamic Device Fleet & Quarantine Matrix**:
   - Connected nodes (`core.compute`, `camera.primary`, `sensor.env`, `comm.primary`, `comm.backup`) with trust score gauges, power draw metrics, and manual **`[ISOLATE]`** / **`[RESTORE]`** security sandbox overrides.

---

## 🏗️ Project Structure

```text
NEXORA-OMEGA/
├── backend/
│   ├── main.py                  # FastAPI server & route orchestration
│   ├── config.py                # System thresholds, constants & runtime modes
│   ├── state.py                 # Live Digital Twin world state & temporal history
│   │
│   ├── core/
│   │   ├── orchestrator.py      # Core brain: intent -> planner -> capability execution
│   │   ├── intent.py            # Natural language intent classifier
│   │   ├── planner.py           # Multi-step task decomposition engine
│   │   └── capability.py        # Dynamic capability graph & provider manager
│   │
│   ├── ai/
│   │   ├── model_router.py      # Weighted model selector (latency, energy, trust)
│   │   ├── prediction.py        # Risk forecasting & anomaly projection
│   │   └── anomaly.py           # Environmental multi-sensor drift detector
│   │
│   ├── security/
│   │   ├── trust.py             # Device & model zero-trust evaluation
│   │   └── quarantine.py        # Micro-isolation & sandbox controller
│   │
│   ├── recovery/
│   │   └── recovery_engine.py   # Autonomous self-healing & failover rerouting
│   │
│   └── simulation/
│       └── simulator.py         # "Simulate-before-execute" digital twin sandbox
│
├── frontend/
│   ├── index.html               # Cyber-HUD Command Center dashboard
│   ├── css/nexora.css           # Sci-Fi aesthetic styles, glow & scanlines
│   └── js/app.js                # Dual 3D visualizer, Web Voice/Audio & Autopilot
│
├── hardware/
│   └── esp32/
│       └── telemetry.ino        # ESP32 WiFi multi-sensor telemetry agent
│
├── config/
│   └── models.json              # Model registry configurations
│
├── requirements.txt             # Dependencies (fastapi, uvicorn, pydantic)
├── run_nexora.bat               # Windows one-click runner
└── README.md
```

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Web Dashboard (HTML) or System Status (JSON) |
| `GET` | `/api/state` | Current Digital Twin world state |
| `GET` | `/api/history` | Temporal metrics buffer (for Oscilloscope) |
| `GET` | `/api/capabilities`| Dynamic Capability Graph nodes & providers |
| `GET` | `/api/models` | Available AI models & latency/trust metrics |
| `GET` | `/api/devices` | Connected hardware fleet & quarantine status |
| `POST` | `/api/command` | Issue command `{"command": "system status"}` |
| `POST` | `/api/telemetry`| Inject sensor readings `{"temperature": 45.0, ...}` |
| `POST` | `/api/device/toggle` | Quarantine/restore device `{"device_id": "comm.primary"}` |
| `POST` | `/api/mode` | Manually switch mode `{"mode": "ADAPTIVE"}` |
| `POST` | `/api/anomaly` | Trigger simulated environmental sensor anomaly |
| `POST` | `/api/failure` | Trigger primary node failure & auto-recovery |
| `POST` | `/api/reset` | Restore baseline state & clear quarantines |
