class TrustEngine:

    def __init__(self):

        self.threshold = 40

    def evaluate(
        self,
        trust: float
    ):

        if trust >= 80:
            level = "TRUSTED"

        elif trust >= self.threshold:
            level = "DEGRADED"

        else:
            level = "UNTRUSTED"

        return {
            "trust": trust,
            "level": level,
            "quarantine_required":
                trust < self.threshold
        }


trust_engine = TrustEngine()
