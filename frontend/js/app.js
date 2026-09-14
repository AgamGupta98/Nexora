/**
 * NEXORA Ω v0.2.0-PRO — Universal Adaptive Intelligence Runtime
 * Real-Time WebSocket, Multi-Canvas Digital Twin, GPS Radar,
 * Floating Assistant Widget, and NIST AI RMF Governance.
 */

// --- Cyber Audio & Speech Synthesis Engine ---
class CyberAudioEngine {
  constructor() {
    this.sfxEnabled = true;
    this.voiceEnabled = true;
    this.ctx = null;
    this.synth = window.speechSynthesis || null;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  }

  playTone(freq = 800, type = 'sine', duration = 0.08, gainVal = 0.04) {
    if (!this.sfxEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {}
  }

  click() { this.playTone(1200, 'triangle', 0.04, 0.03); }
  anomaly() { this.playTone(320, 'sawtooth', 0.35, 0.07); }
  recovery() {
    this.playTone(880, 'sine', 0.12, 0.05);
    setTimeout(() => this.playTone(1320, 'triangle', 0.22, 0.05), 100);
  }
  success() { this.playTone(1050, 'sine', 0.09, 0.04); }

  speak(text) {
    if (!this.voiceEnabled || !this.synth) return;
    try {
      this.synth.cancel();
      const cleanText = text.replace(/[^\w\s.,?!-]/gi, '');
      const utter = new SpeechSynthesisUtterance(cleanText);
      utter.rate = 1.05;
      utter.pitch = 0.95;
      const voices = this.synth.getVoices();
      const eng = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Zira')));
      if (eng) utter.voice = eng;
      this.synth.speak(utter);
    } catch (e) {}
  }
}

const sfx = new CyberAudioEngine();

// --- Tri-View Canvas: Reactor, 3D Digital Twin, GPS Radar ---
class TriVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.mode = 'NORMAL';
    this.view = 'reactor'; // 'reactor', 'twin', 'radar'
    this.angle = 0;
    this.health = 96.8;
    this.risk = 39.0;
    this.gps = { lat: 28.6139, lon: 77.2090, alt: 216.4, speed: 0.0 };

    // Reactor particles
    this.particles = [];
    for (let i = 0; i < 40; i++) {
      this.particles.push({
        r: Math.random() * 60 + 18,
        speed: (Math.random() * 0.02 + 0.008) * (Math.random() > 0.5 ? 1 : -1),
        size: Math.random() * 2.2 + 1,
        angle: Math.random() * Math.PI * 2,
        color: Math.random() > 0.3 ? '#00f0ff' : '#b055ff'
      });
    }

    // 3D Cube / Satellite Wireframe
    this.vertices = [
      [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
      [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
    ];
    this.edges = [
      [0,1],[1,2],[2,3],[3,0],
      [4,5],[5,6],[6,7],[7,4],
      [0,4],[1,5],[2,6],[3,7]
    ];
    this.rotX = 0;
    this.rotY = 0;

    this.render = this.render.bind(this);
    requestAnimationFrame(this.render);
  }

  setView(v) {
    this.view = v;
    sfx.click();
  }

  update(mode, health, risk, gps) {
    this.mode = mode || 'NORMAL';
    if (health !== undefined) this.health = health;
    if (risk !== undefined) this.risk = risk;
    if (gps) this.gps = gps;
  }

  render() {
    if (!this.ctx) return;
    const w = this.canvas.width = this.canvas.offsetWidth || 300;
    const h = this.canvas.height = this.canvas.offsetHeight || 195;
    const cx = w / 2;
    const cy = h / 2;

    this.ctx.clearRect(0, 0, w, h);

    let speed = 1.0;
    let mainColor = '#00f0ff';
    let ringColor = 'rgba(0, 240, 255, 0.25)';

    if (this.mode === 'ADAPTIVE') {
      speed = 1.6;
      mainColor = '#ffaa00';
      ringColor = 'rgba(255, 170, 0, 0.35)';
    } else if (this.mode === 'RECOVERY') {
      speed = 1.3;
      mainColor = '#b055ff';
      ringColor = 'rgba(176, 85, 255, 0.4)';
    } else if (this.mode === 'ALERT' || this.mode === 'EMERGENCY' || this.risk > 65) {
      speed = 2.4;
      mainColor = '#ff3366';
      ringColor = 'rgba(255, 51, 102, 0.45)';
    }

    this.angle += 0.015 * speed;

    if (this.view === 'reactor') {
      // --- ARC REACTOR CORE ---
      const corePulse = 16 + Math.sin(this.angle * 3.5) * 3;
      const grad = this.ctx.createRadialGradient(cx, cy, 2, cx, cy, corePulse * 2.5);
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.35, mainColor);
      grad.addColorStop(1, 'transparent');

      this.ctx.fillStyle = grad;
      this.ctx.beginPath();
      this.ctx.arc(cx, cy, corePulse * 2.2, 0, Math.PI * 2);
      this.ctx.fill();

      // Triple Rings
      [38, 58, 78].forEach((r, i) => {
        this.ctx.save();
        this.ctx.translate(cx, cy);
        this.ctx.rotate((i % 2 === 0 ? 1 : -1) * this.angle * (0.8 + i * 0.2));
        this.ctx.strokeStyle = ringColor;
        this.ctx.lineWidth = 1.5;
        this.ctx.setLineDash([10, 6, 4, 6]);
        this.ctx.beginPath();
        this.ctx.arc(0, 0, r, 0, Math.PI * 2);
        this.ctx.stroke();

        this.ctx.fillStyle = mainColor;
        for (let a = 0; a < 3; a++) {
          const na = (Math.PI * 2 / 3) * a;
          this.ctx.beginPath();
          this.ctx.arc(Math.cos(na) * r, Math.sin(na) * r, 2.2, 0, Math.PI * 2);
          this.ctx.fill();
        }
        this.ctx.restore();
      });

      this.particles.forEach(p => {
        p.angle += p.speed * speed;
        const px = cx + Math.cos(p.angle) * p.r;
        const py = cy + Math.sin(p.angle) * p.r;
        this.ctx.fillStyle = this.mode === 'NORMAL' ? p.color : mainColor;
        this.ctx.beginPath();
        this.ctx.arc(px, py, p.size, 0, Math.PI * 2);
        this.ctx.fill();
      });

    } else if (this.view === 'twin') {
      // --- 3D DIGITAL TWIN WIREFRAME ---
      this.rotX += 0.012 * speed;
      this.rotY += 0.018 * speed;
      const fov = 160;
      const distance = 3.4;

      const projected = this.vertices.map(v => {
        let x = v[0], y = v[1], z = v[2];
        let cosY = Math.cos(this.rotY), sinY = Math.sin(this.rotY);
        let x1 = x * cosY - z * sinY;
        let z1 = x * sinY + z * cosY;

        let cosX = Math.cos(this.rotX), sinX = Math.sin(this.rotX);
        let y2 = y * cosX - z1 * sinX;
        let z2 = y * sinX + z1 * cosX;

        let scale = fov / (distance + z2);
        return { x: cx + x1 * scale, y: cy + y2 * scale, z: z2 };
      });

      this.ctx.strokeStyle = mainColor;
      this.ctx.lineWidth = 1.6;
      this.ctx.beginPath();
      this.edges.forEach(e => {
        this.ctx.moveTo(projected[e[0]].x, projected[e[0]].y);
        this.ctx.lineTo(projected[e[1]].x, projected[e[1]].y);
      });
      this.ctx.stroke();

      projected.forEach((p, idx) => {
        this.ctx.fillStyle = idx % 2 === 0 ? '#00ffaa' : mainColor;
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, 3.5, 0, Math.PI * 2);
        this.ctx.fill();
      });

    } else if (this.view === 'radar') {
      // --- REAL-TIME GPS RADAR ---
      const maxR = 75;
      this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.2)';
      this.ctx.lineWidth = 1;
      [25, 50, 75].forEach(r => {
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, r, 0, Math.PI * 2);
        this.ctx.stroke();
      });

      // Crosshairs
      this.ctx.beginPath();
      this.ctx.moveTo(cx - maxR, cy); this.ctx.lineTo(cx + maxR, cy);
      this.ctx.moveTo(cx, cy - maxR); this.ctx.lineTo(cx, cy + maxR);
      this.ctx.stroke();

      // Sweeping radar beam
      this.ctx.save();
      this.ctx.translate(cx, cy);
      this.ctx.rotate(this.angle * 1.5);
      const sweepGrad = this.ctx.createLinearGradient(0, 0, maxR, maxR);
      sweepGrad.addColorStop(0, 'rgba(0, 240, 255, 0.4)');
      sweepGrad.addColorStop(1, 'transparent');
      this.ctx.fillStyle = sweepGrad;
      this.ctx.beginPath();
      this.ctx.moveTo(0, 0);
      this.ctx.arc(0, 0, maxR, 0, Math.PI / 3);
      this.ctx.closePath();
      this.ctx.fill();
      this.ctx.restore();

      // Center Node (You / Edge satellite)
      this.ctx.fillStyle = '#00ffaa';
      this.ctx.beginPath();
      this.ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      this.ctx.fill();

      // Satellite target blips
      const blips = [
        { x: cx + 32, y: cy - 25, id: 'SAT-04' },
        { x: cx - 45, y: cy + 30, id: 'SAT-11' },
        { x: cx + 55, y: cy + 40, id: 'SAT-19' }
      ];
      this.ctx.fillStyle = mainColor;
      this.ctx.font = '9px monospace';
      blips.forEach(b => {
        this.ctx.beginPath();
        this.ctx.arc(b.x, b.y, 3, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.fillText(b.id, b.x + 5, b.y - 2);
      });
    }

    requestAnimationFrame(this.render);
  }
}

// --- Multi-Channel Temporal Oscilloscope Canvas ---
class OscilloscopeChart {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
  }

  draw(history) {
    if (!this.ctx || !history || history.length < 2) return;
    const w = this.canvas.width = this.canvas.offsetWidth || 300;
    const h = this.canvas.height = this.canvas.offsetHeight || 75;
    this.ctx.clearRect(0, 0, w, h);

    // Gridlines
    this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.08)';
    this.ctx.lineWidth = 1;
    for (let y = 10; y < h; y += 18) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(w, y);
      this.ctx.stroke();
    }

    const n = history.length;
    const step = w / (n - 1);

    this.drawLine(history.map(d => d.risk), step, h, '#ff3366', 100);
    this.drawLine(history.map(d => d.health), step, h, '#00ffaa', 100);
    this.drawLine(history.map(d => d.temperature), step, h, '#00f0ff', 70);
  }

  drawLine(data, step, h, color, maxVal) {
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = 1.8;
    this.ctx.beginPath();
    data.forEach((val, i) => {
      const x = i * step;
      const norm = Math.max(0, Math.min(val / maxVal, 1));
      const y = h - (norm * (h - 8) + 4);
      if (i === 0) this.ctx.moveTo(x, y);
      else this.ctx.lineTo(x, y);
    });
    this.ctx.stroke();
  }
}

// --- Master Command Center Application ---
class NexoraMasterApp {
  constructor() {
    this.apiBase = window.location.origin;
    this.ws = null;
    this.visualizer = new TriVisualizer('mainVisualizerCanvas');
    this.chart = new OscilloscopeChart('historyChart');
    this.isAutopilot = false;
    this.autopilotTimer = null;
    this.recognition = null;
    this.isRecording = false;
    this.isUserDraggingSliders = false;
    this.lastEventCount = 0;

    this.initDOM();
    this.bindEvents();
    this.initWebSocket();
    this.initSpeechRec();
    this.fetchInitialData();
    this.startPolling();

    setTimeout(() => {
      sfx.speak("NEXORA Omega runtime active. Quantum core and digital twin synchronized.");
    }, 1200);
  }

  initDOM() {
    this.elModeBadge = document.getElementById('modeBadge');
    this.elMissionGoal = document.getElementById('missionGoal');
    this.elUptimeClock = document.getElementById('uptimeClock');

    // Metrics
    this.elValHealth = document.getElementById('valHealth');
    this.elBarHealth = document.getElementById('barHealth');
    this.elValSecurity = document.getElementById('valSecurity');
    this.elBarSecurity = document.getElementById('barSecurity');
    this.elValRisk = document.getElementById('valRisk');
    this.elBarRisk = document.getElementById('barRisk');
    this.elValPrediction = document.getElementById('valPrediction');
    this.elBarPrediction = document.getElementById('barPrediction');
    this.elValEnergy = document.getElementById('valEnergy');
    this.elBarEnergy = document.getElementById('barEnergy');

    // Environment & GPS
    this.elEnvTemp = document.getElementById('envTemp');
    this.elEnvHumidity = document.getElementById('envHumidity');
    this.elEnvGas = document.getElementById('envGas');
    this.elEnvVib = document.getElementById('envVib');
    this.elEnvLight = document.getElementById('envLight');
    this.elGpsCoordinates = document.getElementById('gpsCoordinates');

    // Sliders
    this.sliderTemp = document.getElementById('sliderTemp');
    this.sliderGas = document.getElementById('sliderGas');
    this.sliderVib = document.getElementById('sliderVib');
    this.valSliderTemp = document.getElementById('valSliderTemp');
    this.valSliderGas = document.getElementById('valSliderGas');
    this.valSliderVib = document.getElementById('valSliderVib');

    // Lists
    this.elDeviceList = document.getElementById('deviceList');
    this.elModelList = document.getElementById('modelList');
    this.elCapabilityList = document.getElementById('capabilityList');
    this.elEventLogs = document.getElementById('eventLogs');

    // Terminal
    this.elChatHistory = document.getElementById('chatHistory');
    this.elCommandInput = document.getElementById('commandInput');
    this.elBtnSend = document.getElementById('btnSend');
    this.elBtnMic = document.getElementById('btnMic');

    // Floating Chat
    this.floatingTrigger = document.getElementById('floatingChatTrigger');
    this.floatingWindow = document.getElementById('floatingChatWindow');
    this.floatingClose = document.getElementById('floatingChatClose');
    this.floatingMessages = document.getElementById('floatingChatMessages');
    this.floatingInput = document.getElementById('floatingChatInput');
    this.floatingSend = document.getElementById('floatingChatSend');

    // Governance Modal
    this.modalOverlay = document.getElementById('modalOverlay');
    this.approvalAction = document.getElementById('approvalAction');
    this.approvalReason = document.getElementById('approvalReason');
    this.btnApprove = document.getElementById('btnApprove');
    this.btnReject = document.getElementById('btnReject');
    this.currentPendingApproval = null;

    // Header buttons
    this.elBtnAnomaly = document.getElementById('btnAnomaly');
    this.elBtnFailure = document.getElementById('btnFailure');
    this.elBtnReset = document.getElementById('btnReset');
    this.elBtnAudio = document.getElementById('btnAudio');
    this.elBtnVoice = document.getElementById('btnVoice');
    this.elAutopilotSwitch = document.getElementById('autopilotSwitch');
  }

  bindEvents() {
    // Main terminal submit
    if (this.elBtnSend) this.elBtnSend.addEventListener('click', () => this.handleCommandSubmit(this.elCommandInput.value));
    if (this.elCommandInput) {
      this.elCommandInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') this.handleCommandSubmit(this.elCommandInput.value);
      });
    }

    // Floating Chat Window Trigger & Close
    if (this.floatingTrigger) {
      this.floatingTrigger.addEventListener('click', () => {
        sfx.click();
        this.floatingWindow.classList.toggle('open');
      });
    }
    if (this.floatingClose) {
      this.floatingClose.addEventListener('click', () => {
        this.floatingWindow.classList.remove('open');
      });
    }
    if (this.floatingSend) {
      this.floatingSend.addEventListener('click', () => {
        const txt = this.floatingInput.value;
        this.floatingInput.value = '';
        this.handleCommandSubmit(txt);
      });
    }
    if (this.floatingInput) {
      this.floatingInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const txt = this.floatingInput.value;
          this.floatingInput.value = '';
          this.handleCommandSubmit(txt);
        }
      });
    }

    // Mic Voice Input
    if (this.elBtnMic) {
      this.elBtnMic.addEventListener('click', () => this.toggleSpeechRec());
    }

    // Chips
    document.querySelectorAll('.chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sfx.click();
        const cmd = btn.getAttribute('data-cmd');
        if (this.elCommandInput) this.elCommandInput.value = cmd;
        this.handleCommandSubmit(cmd);
      });
    });

    // Tri-view Tabs
    const tabs = [
      { id: 'tabReactor', view: 'reactor' },
      { id: 'tabTwin', view: 'twin' },
      { id: 'tabRadar', view: 'radar' }
    ];
    tabs.forEach(t => {
      const el = document.getElementById(t.id);
      if (el) {
        el.addEventListener('click', () => {
          tabs.forEach(o => document.getElementById(o.id)?.classList.remove('active'));
          el.classList.add('active');
          this.visualizer.setView(t.view);
        });
      }
    });

    // Sliders
    const setupSlider = (slider, valEl, unit) => {
      if (!slider) return;
      slider.addEventListener('pointerdown', () => { this.isUserDraggingSliders = true; });
      slider.addEventListener('pointerup', () => { this.isUserDraggingSliders = false; });
      slider.addEventListener('input', () => {
        if (valEl) valEl.textContent = `${parseFloat(slider.value).toFixed(unit === ' g' ? 2 : (unit === '°C' ? 1 : 0))}${unit}`;
        this.debouncedSendTelemetry();
      });
    };
    setupSlider(this.sliderTemp, this.valSliderTemp, '°C');
    setupSlider(this.sliderGas, this.valSliderGas, ' ppm');
    setupSlider(this.sliderVib, this.valSliderVib, ' g');

    // Autopilot
    if (this.elAutopilotSwitch) {
      this.elAutopilotSwitch.addEventListener('click', () => this.toggleAutopilot());
    }

    // Action Triggers
    if (this.elBtnAnomaly) this.elBtnAnomaly.addEventListener('click', () => this.triggerAnomaly());
    if (this.elBtnFailure) this.elBtnFailure.addEventListener('click', () => this.triggerFailure());
    if (this.elBtnReset) this.elBtnReset.addEventListener('click', () => this.triggerReset());

    // Audio / Voice Toggles
    if (this.elBtnAudio) {
      this.elBtnAudio.addEventListener('click', () => {
        sfx.sfxEnabled = !sfx.sfxEnabled;
        this.elBtnAudio.textContent = sfx.sfxEnabled ? '🔊 SFX ON' : '🔇 SFX OFF';
      });
    }
    if (this.elBtnVoice) {
      this.elBtnVoice.addEventListener('click', () => {
        sfx.voiceEnabled = !sfx.voiceEnabled;
        this.elBtnVoice.textContent = sfx.voiceEnabled ? '🗣️ VOICE ON' : '🤐 VOICE OFF';
      });
    }

    // Modal Approvals
    if (this.btnApprove) {
      this.btnApprove.addEventListener('click', () => this.handleApprovalDecision(true));
    }
    if (this.btnReject) {
      this.btnReject.addEventListener('click', () => this.handleApprovalDecision(false));
    }

    // Live Clock
    setInterval(() => {
      if (this.elUptimeClock) this.elUptimeClock.textContent = new Date().toLocaleTimeString();
    }, 1000);
  }

  initWebSocket() {
    const wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProto}//${window.location.host}/ws`;

    try {
      this.ws = new WebSocket(wsUrl);
      this.ws.onmessage = (e) => {
        try {
          const msg = json.parse(e.data);
          if (msg.state) this.renderState(msg.state);
          if (msg.type === 'APPROVAL_REQUESTED') {
            this.showApprovalModal(msg.approval);
          }
        } catch (err) {}
      };
      this.ws.onclose = () => {
        setTimeout(() => this.initWebSocket(), 3000);
      };
    } catch (e) {}
  }

  initSpeechRec() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      if (this.elBtnMic) this.elBtnMic.style.display = 'none';
      return;
    }
    this.recognition = new SpeechRec();
    this.recognition.continuous = false;
    this.recognition.lang = 'en-US';

    this.recognition.onstart = () => {
      this.isRecording = true;
      if (this.elBtnMic) this.elBtnMic.classList.add('recording');
      sfx.playTone(800, 'sine', 0.05);
    };
    this.recognition.onresult = (e) => {
      const text = e.results[0][0].transcript;
      if (this.elCommandInput) this.elCommandInput.value = text;
      this.handleCommandSubmit(text);
    };
    this.recognition.onend = () => {
      this.isRecording = false;
      if (this.elBtnMic) this.elBtnMic.classList.remove('recording');
    };
  }

  toggleSpeechRec() {
    if (!this.recognition) return;
    if (this.isRecording) this.recognition.stop();
    else this.recognition.start();
  }

  toggleAutopilot() {
    this.isAutopilot = !this.isAutopilot;
    this.elAutopilotSwitch.classList.toggle('active', this.isAutopilot);

    if (this.isAutopilot) {
      sfx.success();
      sfx.speak("Autopilot mission daemon engaged. Autonomous monitoring loop active.");
      this.appendBothMessages('nexora', '⚡ AUTOPILOT ENGAGED: Autonomous telemetry drift, self-model introspection, and multi-objective optimization running.');

      let step = 0;
      this.autopilotTimer = setInterval(async () => {
        step++;
        const temp = +(25.0 + Math.sin(step * 0.4) * 4.5 + Math.random()).toFixed(1);
        const gas = Math.max(8, Math.round(14 + Math.cos(step * 0.3) * 7));
        const vib = +(0.10 + Math.abs(Math.sin(step * 0.2)) * 0.1).toFixed(2);

        await fetch(`${this.apiBase}/api/telemetry`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ temperature: temp, gas: gas, vibration: vib })
        });

        if (step % 14 === 0) {
          const cmds = ['system status', 'optimize energy', 'security audit', 'predict future risk'];
          const picked = cmds[Math.floor(Math.random() * cmds.length)];
          const res = await fetch(`${this.apiBase}/api/command`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: picked })
          });
          const data = await res.json();
          this.appendBothMessages('nexora', `[AUTONOMOUS LOOP] ${data.result.response}`, data.result);
        }
      }, 3500);

    } else {
      clearInterval(this.autopilotTimer);
      sfx.click();
      sfx.speak("Autopilot disengaged. Operator control restored.");
      this.appendBothMessages('nexora', '⏹️ AUTOPILOT DISENGAGED: Manual control active.');
    }
  }

  debouncedSendTelemetry() {
    clearTimeout(this._telemDebounce);
    this._telemDebounce = setTimeout(async () => {
      const temp = parseFloat(this.sliderTemp.value);
      const gas = parseFloat(this.sliderGas.value);
      const vib = parseFloat(this.sliderVib.value);

      const res = await fetch(`${this.apiBase}/api/telemetry`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temperature: temp, gas: gas, vibration: vib })
      });
      if (res.ok) {
        const data = await res.json();
        this.renderState(data.state);
        if (data.analysis.anomaly) {
          sfx.anomaly();
          sfx.speak("Warning. Sensor anomaly detected.");
        }
      }
    }, 150);
  }

  async fetchInitialData() {
    await Promise.all([
      this.fetchState(),
      this.fetchDevices(),
      this.fetchModels(),
      this.fetchCapabilities(),
      this.fetchGPS()
    ]);
  }

  startPolling() {
    setInterval(async () => {
      await this.fetchState();
      await this.fetchGPS();
    }, 2000);
  }

  async fetchState() {
    try {
      const res = await fetch(`${this.apiBase}/api/state`);
      if (res.ok) this.renderState(await res.json());
    } catch (e) {}
  }

  async fetchDevices() {
    try {
      const res = await fetch(`${this.apiBase}/api/devices`);
      if (res.ok) this.renderDevices(await res.json());
    } catch (e) {}
  }

  async fetchModels() {
    try {
      const res = await fetch(`${this.apiBase}/api/models`);
      if (res.ok) this.renderModels(await res.json());
    } catch (e) {}
  }

  async fetchCapabilities() {
    try {
      const res = await fetch(`${this.apiBase}/api/capabilities`);
      if (res.ok) this.renderCapabilities(await res.json());
    } catch (e) {}
  }

  async fetchGPS() {
    try {
      const res = await fetch(`${this.apiBase}/api/gps`);
      if (res.ok) {
        const gps = await res.json();
        if (this.elGpsCoordinates) {
          this.elGpsCoordinates.textContent = `${gps.latitude}° N, ${gps.longitude}° E (Alt: ${gps.altitude_meters}m)`;
        }
        this.visualizer.update(undefined, undefined, undefined, gps);
      }
    } catch (e) {}
  }

  renderState(state) {
    if (!state) return;

    // Mode
    const mode = state.system.mode || 'NORMAL';
    this.elModeBadge.textContent = mode;
    this.elModeBadge.className = `mode-badge mode-${mode}`;

    // Visualizer update
    this.visualizer.update(mode, state.metrics.health, state.metrics.risk, state.spatial_gps);

    // Metrics
    const m = state.metrics;
    this.elValHealth.textContent = `${m.health.toFixed(1)}%`;
    this.elBarHealth.style.width = `${m.health}%`;

    this.elValSecurity.textContent = `${m.security.toFixed(1)}%`;
    this.elBarSecurity.style.width = `${m.security}%`;

    this.elValRisk.textContent = `${m.risk}%`;
    this.elBarRisk.style.width = `${m.risk}%`;
    this.elBarRisk.className = `progress-bar ${m.risk > 60 ? 'bar-red' : (m.risk > 35 ? 'bar-amber' : 'bar-green')}`;

    this.elValPrediction.textContent = `${m.prediction}%`;
    this.elBarPrediction.style.width = `${m.prediction}%`;

    this.elValEnergy.textContent = `${m.energy}W`;
    this.elBarEnergy.style.width = `${Math.min(m.energy, 100)}%`;

    // Environment
    const env = state.environment;
    if (env) {
      this.elEnvTemp.textContent = `${env.temperature.toFixed(1)}°C`;
      this.elEnvHumidity.textContent = `${env.humidity.toFixed(1)}%`;
      this.elEnvGas.textContent = `${env.gas} ppm`;
      this.elEnvVib.textContent = `${env.vibration.toFixed(2)} g`;
      this.elEnvLight.textContent = `${env.light} lux`;

      if (!this.isUserDraggingSliders) {
        if (this.sliderTemp) {
          this.sliderTemp.value = env.temperature;
          this.valSliderTemp.textContent = `${env.temperature.toFixed(1)}°C`;
        }
        if (this.sliderGas) {
          this.sliderGas.value = env.gas;
          this.valSliderGas.textContent = `${env.gas} ppm`;
        }
        if (this.sliderVib) {
          this.sliderVib.value = env.vibration;
          this.valSliderVib.textContent = `${env.vibration.toFixed(2)} g`;
        }
      }
    }

    // History chart
    if (state.history && this.chart) {
      this.chart.draw(state.history);
    }

    // Events log
    if (state.events && state.events.length !== this.lastEventCount) {
      this.renderEvents(state.events);
      this.lastEventCount = state.events.length;
    }
  }

  renderEvents(events) {
    if (!this.elEventLogs) return;
    this.elEventLogs.innerHTML = '';
    events.forEach((ev, idx) => {
      const div = document.createElement('div');
      div.className = `log-entry ${idx === 0 ? 'log-new' : ''}`;
      if (ev.includes('Failure') || ev.includes('isolation') || ev.includes('QUARANTINED')) div.classList.add('log-error');
      else if (ev.includes('anomaly') || ev.includes('ADAPTIVE') || ev.includes('ALERT')) div.classList.add('log-warn');
      else if (ev.includes('recovered') || ev.includes('resumed') || ev.includes('passed')) div.classList.add('log-heal');
      div.textContent = ev;
      this.elEventLogs.appendChild(div);
    });
  }

  renderDevices(devices) {
    if (!this.elDeviceList) return;
    this.elDeviceList.innerHTML = '';
    devices.forEach(dev => {
      const card = document.createElement('div');
      const isQuar = dev.status === 'QUARANTINED';
      card.className = `device-card ${isQuar ? 'quarantined' : ''}`;
      const statusClass = dev.status === 'online' ? 'status-online' :
                         (dev.status === 'standby' ? 'status-standby' : 'status-quarantined');

      card.innerHTML = `
        <div class="device-left">
          <span class="device-name">${dev.name || dev.id}</span>
          <span class="device-type">${dev.id} • ${dev.type.toUpperCase()} • ${dev.energy}W • IP: ${dev.ip || '192.168.1.x'}</span>
        </div>
        <div class="device-right">
          <span class="status-pill ${statusClass}">${dev.status}</span>
          <button class="btn-device-action" data-dev="${dev.id}" data-action="${isQuar ? 'release' : 'isolate'}">
            ${isQuar ? 'RESTORE' : 'ISOLATE'}
          </button>
        </div>
      `;

      card.querySelector('.btn-device-action').addEventListener('click', (e) => {
        const id = e.target.getAttribute('data-dev');
        const act = e.target.getAttribute('data-action');
        this.toggleDevice(id, act);
      });

      this.elDeviceList.appendChild(card);
    });
  }

  async toggleDevice(devId, action) {
    sfx.click();
    try {
      const res = await fetch(`${this.apiBase}/api/device/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: devId, action: action })
      });
      const data = await res.json();
      if (data.state) this.renderState(data.state);
      await this.fetchDevices();
      sfx.success();
    } catch (e) {}
  }

  renderModels(models) {
    if (!this.elModelList) return;
    this.elModelList.innerHTML = '';
    models.forEach(m => {
      const card = document.createElement('div');
      card.className = 'device-card';
      card.innerHTML = `
        <div class="device-left">
          <span class="device-name">${m.id}</span>
          <span class="device-type">${m.type} • ⏱️ ${m.latency}ms • ⚡ ${m.energy}W • 🛡️ ${m.trust}%</span>
        </div>
        <div class="device-right">
          <span class="status-pill ${m.status === 'online' ? 'status-online' : 'status-standby'}">
            ${m.offline ? 'OFFLINE EDGE' : 'CLOUD'}
          </span>
        </div>
      `;
      this.elModelList.appendChild(card);
    });
  }

  renderCapabilities(caps) {
    if (!this.elCapabilityList) return;
    this.elCapabilityList.innerHTML = '';
    caps.forEach(cap => {
      const badge = document.createElement('div');
      badge.className = `cap-badge ${cap.status === 'degraded' ? 'degraded' : ''}`;
      badge.innerHTML = `<span class="cap-dot"></span><span>${cap.name}</span>`;
      badge.title = `Providers: ${cap.providers.join(', ')} | Status: ${cap.status}`;
      badge.addEventListener('click', () => {
        sfx.click();
        this.appendBothMessages('nexora', `ℹ️ Capability Node [${cap.name}] Category: ${cap.category}. Latency: ${cap.latency_ms || 25}ms. Providers: ${cap.providers.join(', ')}.`);
      });
      this.elCapabilityList.appendChild(badge);
    });
  }

  async handleCommandSubmit(rawText) {
    const text = (rawText || '').trim();
    if (!text) return;
    if (this.elCommandInput) this.elCommandInput.value = '';
    sfx.click();

    this.appendBothMessages('user', text);

    try {
      const res = await fetch(`${this.apiBase}/api/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: text })
      });

      if (!res.ok) throw new Error('API command failed');
      const data = await res.json();
      sfx.success();

      this.appendBothMessages('nexora', data.result.response, data.result);
      sfx.speak(data.result.response);

      if (data.result.governance_gate && data.result.governance_gate.human_approval_required) {
        this.showApprovalModal(data.result.governance_gate);
      }

      if (data.state) this.renderState(data.state);
    } catch (e) {
      this.appendBothMessages('nexora', `⚠️ Command execution error: ${e.message}`);
    }
  }

  appendBothMessages(sender, text, meta = null) {
    this.appendMessageToContainer(this.elChatHistory, sender, text, meta);
    this.appendMessageToContainer(this.floatingMessages, sender, text, meta);
  }

  appendMessageToContainer(container, sender, text, meta) {
    if (!container) return;
    const wrapper = document.createElement('div');
    wrapper.className = `msg-wrapper ${sender}`;
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    const header = document.createElement('div');
    header.className = 'msg-header';
    header.innerHTML = `<span>${sender === 'user' ? 'OPERATOR' : 'NEXORA Ω'}</span><span>${time}</span>`;

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.textContent = text;

    if (meta && meta.intent) {
      const intentBox = document.createElement('div');
      intentBox.className = 'plan-card';
      const conf = Math.round((meta.intent.confidence || 0.9) * 100);
      intentBox.innerHTML = `
        <div class="plan-card-title">🎯 INTENT: ${meta.intent.intent} (${conf}% Conf) [NIST Provenance: ${meta.audit_event_id || 'VERIFIED'}]</div>
        <ul class="plan-steps">
          ${(meta.plan || []).map(step => `<li class="plan-step-item">${step}</li>`).join('')}
        </ul>
      `;
      bubble.appendChild(intentBox);
    }

    wrapper.appendChild(header);
    wrapper.appendChild(bubble);
    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
  }

  showApprovalModal(gate) {
    this.currentPendingApproval = gate.approval_id;
    if (this.approvalAction) this.approvalAction.textContent = gate.action;
    if (this.approvalReason) this.approvalReason.textContent = `Risk level: ${gate.risk_level}. Policy: ${gate.policy}. Human confirmation required.`;
    if (this.modalOverlay) this.modalOverlay.classList.add('active');
    sfx.anomaly();
    sfx.speak("High-risk action intercepted. Operator authorization required.");
  }

  async handleApprovalDecision(approved) {
    if (!this.currentPendingApproval) return;
    try {
      await fetch(`${this.apiBase}/api/governance/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ approval_id: this.currentPendingApproval, approved: approved })
      });
      if (this.modalOverlay) this.modalOverlay.classList.remove('active');
      this.currentPendingApproval = null;
      sfx.success();
      this.appendBothMessages('nexora', `Operator decided: ${approved ? 'APPROVED' : 'REJECTED'}. Action committed to NIST immutable audit log.`);
    } catch (e) {}
  }

  async triggerAnomaly() {
    sfx.anomaly();
    sfx.speak("Warning. Environmental sensor anomaly injected. Safety gates triggered.");
    try {
      const res = await fetch(`${this.apiBase}/api/anomaly`, { method: 'POST' });
      const data = await res.json();
      this.renderState(data.state);
      this.appendBothMessages('nexora', `🚨 ALERT: Anomaly Injected! Signals: ${data.analysis.signals.join(', ')}. Mode transitioned to ADAPTIVE.`);
    } catch (e) {}
  }

  async triggerFailure() {
    sfx.anomaly();
    sfx.speak("Alert. Primary link compromised. Autonomous recovery sequence engaged.");
    try {
      const res = await fetch(`${this.apiBase}/api/failure`, { method: 'POST' });
      const data = await res.json();
      sfx.recovery();
      sfx.speak("Simulation approved. Failover complete. System recovered.");
      this.renderState(data.state);
      await this.fetchDevices();
      await this.fetchCapabilities();
      this.appendBothMessages('nexora', `⚡ SELF-HEALING RECOVERY COMMITTED: Primary node quarantined. Backup channel active. Mission operational.`);
    } catch (e) {}
  }

  async triggerReset() {
    sfx.success();
    sfx.speak("Mission runtime reset to baseline operational parameters.");
    try {
      const res = await fetch(`${this.apiBase}/api/reset`, { method: 'POST' });
      const data = await res.json();
      this.renderState(data);
      await this.fetchDevices();
      await this.fetchCapabilities();
      this.appendBothMessages('nexora', '🔄 Mission runtime reset to baseline. All nodes restored.');
    } catch (e) {}
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.nexoraMaster = new NexoraMasterApp();
});
