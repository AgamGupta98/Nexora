"""
NEXORA Ω — Multi-Layer Memory Fabric
Implements:
1. Short-term (Dialogue & Context)
2. Working (Active Mission Execution)
3. Long-term (User Preferences & Policies)
4. Episodic (Incident History & Failure Rollbacks)
5. Semantic (Vector Similarity Knowledge Retrieval)
6. Procedural (Successful Workflow Templates)
"""

import math
import re
from typing import List, Dict, Any, Optional
from collections import Counter
from backend.database import db


def simple_tokenize(text: str) -> List[str]:
    return re.findall(r'\w+', text.lower())


def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([val ** 2 for val in vec1.values()])
    sum2 = sum([val ** 2 for val in vec2.values()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(numerator) / denominator


def text_to_vector(text: str) -> Dict[str, float]:
    words = simple_tokenize(text)
    counts = Counter(words)
    total = len(words) or 1
    return {word: count / total for word, count in counts.items()}


class MemoryFabric:
    def __init__(self):
        self.short_term: List[Dict[str, Any]] = []
        self.working_memory: Dict[str, Any] = {
            "current_mission": "Maintain safe adaptive operation",
            "active_constraints": ["Zero uncontrolled actuation", "Offline-first privacy"],
            "operator_role": "ADMIN",
            "threat_level": "LOW"
        }
        self.init_seed_memories()

    def init_seed_memories(self):
        # Ensure foundational semantic and procedural memories exist in database
        existing = db.search_memories(limit=1)
        if not existing:
            # Seed Semantic Knowledge
            db.store_memory(
                memory_type="semantic",
                key="nist_ai_rmf",
                content="NIST AI Risk Management Framework emphasizes governance, trustworthiness, explainability, safety, security, and human-in-the-loop oversight.",
                tags=["governance", "nist", "safety", "trust"]
            )
            db.store_memory(
                memory_type="semantic",
                key="zero_trust_policy",
                content="Zero-Trust Architecture: Never trust, always verify. Isolate nodes whose trust score falls below 40%.",
                tags=["security", "zero_trust", "quarantine"]
            )
            db.store_memory(
                memory_type="semantic",
                key="model_selection_rules",
                content="When offline_required is true, prioritize local models like llm.local and vision.local. High privacy data must never leave local perimeter.",
                tags=["ai", "model_routing", "privacy"]
            )

            # Seed Procedural Workflow
            db.store_memory(
                memory_type="procedural",
                key="rf_failover_plan",
                content="1. Detect primary RF fault -> 2. Quarantine primary node -> 3. Run digital twin simulation on mesh backup -> 4. Activate backup mesh link -> 5. Verify telemetry handshake -> 6. Resume mission.",
                tags=["recovery", "failover", "communication"]
            )

            # Seed Long-Term Preference
            db.store_memory(
                memory_type="long_term",
                key="operator_pref_edge",
                content="Operator preference: Keep system in balanced energy state with real-time autonomous failover enabled.",
                tags=["preference", "operator"]
            )

    # --- Short-Term Memory ---
    def record_interaction(self, role: str, content: str, intent: str = None):
        entry = {
            "role": role,
            "content": content,
            "intent": intent
        }
        self.short_term.append(entry)
        if len(self.short_term) > 20:
            self.short_term.pop(0)
        # Also persist to DB as episodic memory
        db.store_memory(
            memory_type="episodic",
            key=f"dialogue_{role}",
            content=f"[{role.upper()}] {content}",
            tags=["dialogue", role, intent or ""]
        )

    def get_short_term(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.short_term[-limit:]

    # --- Working Memory ---
    def set_working(self, key: str, value: Any):
        self.working_memory[key] = value

    def get_working(self, key: str = None) -> Any:
        if key:
            return self.working_memory.get(key)
        return self.working_memory

    # --- Long-Term Memory & User Preferences ---
    def set_preference(self, key: str, value: str):
        db.store_memory(
            memory_type="long_term",
            key=key,
            content=value,
            tags=["user_preference", key]
        )

    # --- Semantic Vector Retrieval (Similarity Search) ---
    def recall_semantic(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_vec = text_to_vector(query)
        all_memories = db.search_memories(limit=100)

        scored = []
        for mem in all_memories:
            mem_vec = text_to_vector(mem["content"] + " " + (mem.get("tags") or ""))
            sim = cosine_similarity(query_vec, mem_vec)
            if sim > 0.05:
                scored.append({
                    "id": mem["id"],
                    "type": mem["memory_type"],
                    "key": mem["key"],
                    "content": mem["content"],
                    "similarity": round(sim, 3),
                    "created_at": mem["created_at"]
                })

        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]

    # --- Snapshot for Frontend / Digital Twin ---
    def snapshot(self) -> Dict[str, Any]:
        return {
            "working_memory": self.working_memory,
            "short_term_count": len(self.short_term),
            "recent_dialogue": self.short_term[-6:],
            "total_stored_memories": len(db.search_memories(limit=500)),
            "recent_episodic": db.search_memories(memory_type="episodic", limit=5),
            "semantic_knowledge": db.search_memories(memory_type="semantic", limit=5),
            "procedural_workflows": db.search_memories(memory_type="procedural", limit=5)
        }


memory_fabric = MemoryFabric()
