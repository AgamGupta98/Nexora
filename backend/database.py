"""
NEXORA Ω — Real-Time Persistent Database Engine
Built on SQLite with WAL mode for ultra-low latency, concurrent access,
and persistent digital twin memory & audit logging.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "nexora_runtime.db"


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Audit Trail Table (NIST AI RMF Governance)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                actor TEXT NOT NULL,
                action_input TEXT,
                decision TEXT NOT NULL,
                model_used TEXT,
                capability_used TEXT,
                device_involved TEXT,
                risk_level TEXT NOT NULL,
                authorization TEXT NOT NULL,
                result TEXT NOT NULL,
                details TEXT
            );
            """)

            # 2. Multi-Layer Memory Engine Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_type TEXT NOT NULL, -- short_term, working, long_term, episodic, semantic, procedural
                key TEXT,
                content TEXT NOT NULL,
                tags TEXT,
                embedding_json TEXT,
                importance REAL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL
            );
            """)

            # 3. Telemetry & GPS Time-Series History Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                gas REAL,
                vibration REAL,
                light REAL,
                cpu_load REAL,
                ram_usage REAL,
                gps_lat REAL,
                gps_lon REAL,
                gps_alt REAL,
                gps_speed REAL,
                health REAL,
                risk REAL,
                security REAL,
                energy REAL
            );
            """)

            # 4. Human-in-the-Loop Approvals Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS human_approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                approval_id TEXT UNIQUE NOT NULL,
                action TEXT NOT NULL,
                risk_level TEXT NOT NULL, -- LOW, MEDIUM, HIGH, CRITICAL
                reason TEXT NOT NULL,
                proposed_changes TEXT,
                status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, AUTO_EXECUTED
                requested_at TEXT NOT NULL,
                resolved_at TEXT,
                resolved_by TEXT
            );
            """)

            # 5. Device Registry & State
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_registry (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                trust_score REAL NOT NULL,
                energy_watts REAL NOT NULL,
                ip_address TEXT,
                firmware_version TEXT,
                last_heartbeat TEXT
            );
            """)

            # 6. Event Stream Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_stream (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL, -- INFO, NOTICE, WARNING, ALERT, CRITICAL
                source TEXT NOT NULL,
                message TEXT NOT NULL,
                metadata_json TEXT
            );
            """)

            conn.commit()

    # --- Audit Trail Methods ---
    def record_audit(self, actor: str, decision: str, risk_level: str, authorization: str,
                     result: str, action_input: str = "", model_used: str = "",
                     capability_used: str = "", device_involved: str = "", details: Dict = None):
        event_id = f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{datetime.now().microsecond // 1000:03d}"
        timestamp = datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO audit_trail (event_id, timestamp, actor, action_input, decision, model_used,
                                     capability_used, device_involved, risk_level, authorization, result, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (event_id, timestamp, actor, action_input, decision, model_used,
                  capability_used, device_involved, risk_level, authorization, result,
                  json.dumps(details or {})))
            conn.commit()
        return event_id

    def get_recent_audits(self, limit: int = 50) -> List[Dict]:
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM audit_trail ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    # --- Memory Store Methods ---
    def store_memory(self, memory_type: str, content: str, key: str = None,
                     tags: List[str] = None, importance: float = 1.0, embedding: List[float] = None) -> int:
        now = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO memory_store (memory_type, key, content, tags, embedding_json, importance, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (memory_type, key, content, json.dumps(tags or []),
                  json.dumps(embedding or []), importance, now, now))
            conn.commit()
            return cursor.lastrowid

    def search_memories(self, query: str = "", memory_type: str = None, limit: int = 20) -> List[Dict]:
        with self.get_connection() as conn:
            if memory_type and query:
                rows = conn.execute(
                    "SELECT * FROM memory_store WHERE memory_type = ? AND content LIKE ? ORDER BY id DESC LIMIT ?",
                    (memory_type, f"%{query}%", limit)
                ).fetchall()
            elif memory_type:
                rows = conn.execute(
                    "SELECT * FROM memory_store WHERE memory_type = ? ORDER BY id DESC LIMIT ?",
                    (memory_type, limit)
                ).fetchall()
            elif query:
                rows = conn.execute(
                    "SELECT * FROM memory_store WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                    (f"%{query}%", limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM memory_store ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
            return [dict(r) for r in rows]

    # --- Telemetry History Methods ---
    def record_telemetry(self, data: Dict[str, Any]):
        timestamp = datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO telemetry_history (
                timestamp, temperature, humidity, gas, vibration, light,
                cpu_load, ram_usage, gps_lat, gps_lon, gps_alt, gps_speed,
                health, risk, security, energy
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                data.get("temperature", 26.4),
                data.get("humidity", 48.2),
                data.get("gas", 12.0),
                data.get("vibration", 0.12),
                data.get("light", 72.0),
                data.get("cpu_load", 18.5),
                data.get("ram_usage", 42.0),
                data.get("gps_lat", 28.6139),
                data.get("gps_lon", 77.2090),
                data.get("gps_alt", 216.0),
                data.get("gps_speed", 0.0),
                data.get("health", 96.8),
                data.get("risk", 39.0),
                data.get("security", 98.4),
                data.get("energy", 54.0)
            ))
            conn.commit()

    def get_telemetry_history(self, limit: int = 40) -> List[Dict]:
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM telemetry_history ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            # Return in chronological order
            return [dict(r) for r in reversed(rows)]

    # --- Human Approvals Methods ---
    def create_approval_request(self, action: str, risk_level: str, reason: str, proposed_changes: Dict) -> str:
        approval_id = f"APPR-{datetime.now().strftime('%H%M%S')}-{datetime.now().microsecond // 1000:03d}"
        now = datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO human_approvals (approval_id, action, risk_level, reason, proposed_changes, status, requested_at)
            VALUES (?, ?, ?, ?, ?, 'PENDING', ?)
            """, (approval_id, action, risk_level, reason, json.dumps(proposed_changes), now))
            conn.commit()
        return approval_id

    def resolve_approval(self, approval_id: str, approved: bool, resolved_by: str = "Operator"):
        now = datetime.now().isoformat()
        status = "APPROVED" if approved else "REJECTED"
        with self.get_connection() as conn:
            conn.execute("""
            UPDATE human_approvals
            SET status = ?, resolved_at = ?, resolved_by = ?
            WHERE approval_id = ?
            """, (status, now, resolved_by, approval_id))
            conn.commit()

    def get_pending_approvals(self) -> List[Dict]:
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM human_approvals WHERE status = 'PENDING' ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    # --- Event Stream Methods ---
    def log_event(self, source: str, message: str, severity: str = "INFO", metadata: Dict = None):
        now = datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute("""
            INSERT INTO event_stream (timestamp, severity, source, message, metadata_json)
            VALUES (?, ?, ?, ?, ?)
            """, (now, severity, source, message, json.dumps(metadata or {})))
            conn.commit()

    def get_recent_events(self, limit: int = 30) -> List[Dict]:
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM event_stream ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]


db = Database()
