class IntentEngine:

    def understand(self, text: str):

        text = text.lower().strip()

        if "status" in text:
            return {
                "intent": "SYSTEM_STATUS",
                "confidence": 0.98
            }

        if "energy" in text:
            return {
                "intent": "ENERGY_OPTIMIZATION",
                "confidence": 0.95
            }

        if "security" in text:
            return {
                "intent": "SECURITY_CHECK",
                "confidence": 0.96
            }

        if "simulation" in text:
            return {
                "intent": "SIMULATION",
                "confidence": 0.94
            }

        if "predict" in text:
            return {
                "intent": "PREDICTION",
                "confidence": 0.91
            }

        return {
            "intent": "GENERAL_QUERY",
            "confidence": 0.71
        }


intent_engine = IntentEngine()
