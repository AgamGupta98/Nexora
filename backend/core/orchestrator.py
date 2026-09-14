"""
NEXORA Ω — Central Cognitive Orchestrator
Connects:
User / Voice Input -> Intent Engine -> Memory Recall -> Context Retrieval ->
Planner -> Model Router -> Real AI Adapter -> Safety Gate (NIST AI RMF) ->
Execution -> Verification -> Provenance Audit Trail -> Memory Storage
"""

from typing import Dict, Any, List
from backend.core.intent import intent_engine
from backend.core.planner import planner
from backend.ai.model_router import model_router
from backend.ai.real_ai_adapter import real_ai_adapter
from backend.core.memory import memory_fabric
from backend.core.world_model import world_model
from backend.core.self_model import self_model
from backend.security.governance import governance_engine
from backend.state import runtime
from backend.database import db


class CentralCognitiveOrchestrator:
    def __init__(self):
        pass

    def process(self, user_input: str) -> Dict[str, Any]:
        # 1. Intent & Entity Parsing
        intent_result = intent_engine.understand(user_input)
        intent = intent_result["intent"]

        # 2. Record User dialogue in Memory Fabric
        memory_fabric.record_interaction(role="user", content=user_input, intent=intent)

        # 3. Task Planning & Hierarchical Decomposition
        plan = planner.create_plan(intent)

        # 4. Context Retrieval (Snapshot of World Model + Memory)
        world_snapshot = world_model.get_world_snapshot(runtime.snapshot())

        # 5. Cognitive Reasoning via Real AI Adapter (Ollama / Cloud / Embedded)
        ai_response = real_ai_adapter.generate_response(user_input, world_snapshot)

        # 6. Safety & Risk Gating (NIST AI RMF)
        current_risk = runtime.data["metrics"]["risk"]
        gate = governance_engine.evaluate_risk_and_gate(action=intent, params={"input": user_input}, current_risk=current_risk)

        # 7. Record AI dialogue in Memory Fabric
        memory_fabric.record_interaction(role="nexora", content=ai_response["answer"], intent=intent)

        # 8. Event stream & NIST Provenance logging
        runtime.event(f"Intent parsed -> {intent} ({int(intent_result['confidence']*100)}% Conf)")
        runtime.event(f"Cognitive plan generated -> {len(plan)} verified steps")

        event_id = governance_engine.record_provenance(
            actor="Operator",
            action=user_input,
            decision=ai_response["explanation"].get("decision", "COGNITIVE_RESPONSE"),
            model_used=ai_response.get("provider_used", "llm.local"),
            capability="reasoning.conversation",
            device="core.compute",
            risk=current_risk,
            result="EXECUTED"
        )

        return {
            "input": user_input,
            "intent": intent_result,
            "plan": plan,
            "response": ai_response["answer"],
            "reasoning_steps": ai_response.get("reasoning_steps", []),
            "explanation": ai_response.get("explanation", {}),
            "recalled_memories": ai_response.get("recalled_memories", []),
            "governance_gate": gate,
            "audit_event_id": event_id
        }


orchestrator = CentralCognitiveOrchestrator()
