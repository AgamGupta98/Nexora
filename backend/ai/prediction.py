class PredictionEngine:

    def predict(
        self,
        current_risk: float,
        anomaly_count: int
    ):

        predicted_risk = (
            current_risk
            + anomaly_count * 13
        )

        predicted_risk = min(
            predicted_risk,
            100
        )

        if predicted_risk >= 80:
            level = "CRITICAL"

        elif predicted_risk >= 60:
            level = "HIGH"

        elif predicted_risk >= 35:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "predicted_risk": predicted_risk,
            "level": level,
            "confidence": 0.86
        }


prediction_engine = PredictionEngine()
