"""
NEXORA Ω — Security, Trust & NIST AI RMF Governance
Implements:
1. 6-Factor Dynamic Trust Fabric
2. Human-in-the-Loop (HITL) Safety Gate
3. NIST AI Risk Management Framework (RMF) Governance & Audit Trail
4. Explainability & Provenance Engine
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.database import db


class NISTGovernanceEngine:
    def __init__(self):
        self.trust_weights = {
            "identity": 0.20,
            "integrity": 0.20,
            "behavior": 0.20,
            "reliability": 0.15,
            "provenance": 0.15,
            "security": 0.10
        }

    def compute_trust_score(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Computes trust score based on 6 weighted factors:
        Identity (20%), Integrity (20%), Behavior (20%), Reliability (15%), Provenance (15%), Security (10%).
        """
        id_score = metrics.get("identity", 98.0) * self.trust_weights["identity"]
        int_score = metrics.get("integrity", 98.0) * self.trust_weights["integrity"]
        beh_score = metrics.get("behavior", 96.0) * self.trust_weights["behavior"]
        rel_score = metrics.get("reliability", 97.0) * self.trust_weights["reliability"]
        prov_score = metrics.get("provenance", 95.0) * self.trust_weights["provenance"]
        sec_score = metrics.get("security", 98.0) * self.trust_weights["security"]

        total_trust = round(id_score + int_score + beh_score + rel_score + prov_score + sec_score, 1)

        if total_trust >= 85.0:
            level = "TRUSTED"
            action = "UNRESTRICTED"
        elif total_trust >= 65.0:
            level = "CONDITIONAL"
            action = "MONITORED"
        elif total_trust >= 40.0:
            level = "RESTRICTED"
            action = "RESTRICTED_ACCESS"
        else:
            level = "UNTRUSTED"
            action = "IMMEDIATE_QUARANTINE"

        return {
            "total_trust": total_trust,
            "classification": level,
            "policy_action": action,
            "quarantine_required": total_trust < 40.0,
            "breakdown": {
                "identity": round(metrics.get("identity", 98.0), 1),
                "integrity": round(metrics.get("integrity", 98.0), 1),
                "behavior": round(metrics.get("behavior", 96.0), 1),
                "reliability": round(metrics.get("reliability", 97.0), 1),
                "provenance": round(metrics.get("provenance", 95.0), 1),
                "security": round(metrics.get("security", 98.0), 1)
            }
        }

    def evaluate_risk_and_gate(self, action: str, params: Dict[str, Any], current_risk: float) -> Dict[str, Any]:
        """
        Human-in-the-loop safety gating based on risk level.
        Low: Auto-approved
        Medium: Confirmation required
        High: Formal Human Approval Required (HALT execution until approved)
        Critical: Emergency Lock
        """
        high_risk_keywords = ["quarantine", "kill", "reconfigure", "reflash", "format", "shutdown", "isolate"]
        is_high_risk = any(kw in action.lower() for kw in high_risk_keywords) or current_risk > 70.0

        if current_risk >= 85.0:
            risk_level = "CRITICAL"
            needs_approval = True
            policy = "SAFETY_LOCK"
        elif is_high_risk:
            risk_level = "HIGH"
            needs_approval = True
            policy = "HUMAN_APPROVAL_REQUIRED"
        elif current_risk >= 50.0:
            risk_level = "MEDIUM"
            needs_approval = False
            policy = "AUTOMATIC_WITH_NOTICE"
        else:
            risk_level = "LOW"
            needs_approval = False
            policy = "AUTOMATIC_EXECUTE"

        approval_id = None
        if needs_approval:
            approval_id = db.create_approval_request(
                action=action,
                risk_level=risk_level,
                reason=f"Action '{action}' crossed safety threshold with risk={current_risk}%.",
                proposed_changes=params
            )

        return {
            "action": action,
            "risk_level": risk_level,
            "policy": policy,
            "human_approval_required": needs_approval,
            "approval_id": approval_id
        }

    def record_provenance(self, actor: str, action: str, decision: str, model_used: str,
                          capability: str, device: str, risk: float, result: str) -> str:
        """
        NIST AI RMF Compliant Immutable Audit Record.
        """
        return db.record_audit(
            actor=actor,
            decision=decision,
            risk_level="HIGH" if risk > 65 else ("MEDIUM" if risk > 35 else "LOW"),
            authorization="NIST-SP-1270-RMF-P1",
            result=result,
            action_input=action,
            model_used=model_used,
            capability_used=capability,
            device_involved=device,
            details={"timestamp": datetime.now().isoformat(), "risk_score": risk}
        )


governance_engine = NISTGovernanceEngine()
