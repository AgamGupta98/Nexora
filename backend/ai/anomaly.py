class AnomalyEngine:

    def analyze(self, environment):

        temperature = environment.get(
            "temperature",
            0
        )

        gas = environment.get(
            "gas",
            0
        )

        vibration = environment.get(
            "vibration",
            0
        )

        anomalies = []

        if temperature > 40:
            anomalies.append(
                "HIGH_TEMPERATURE"
            )

        if gas > 60:
            anomalies.append(
                "GAS_ANOMALY"
            )

        if vibration > 0.8:
            anomalies.append(
                "HIGH_VIBRATION"
            )

        risk = 20

        risk += len(anomalies) * 20

        risk = min(
            risk,
            100
        )

        return {
            "anomaly": len(anomalies) > 0,
            "signals": anomalies,
            "risk": risk
        }


anomaly_engine = AnomalyEngine()
