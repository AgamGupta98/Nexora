from typing import List, Dict


class ModelRouter:

    def __init__(self):

        self.models = {

            "llm.local": {
                "type": "language",
                "offline": True,
                "latency": 120,
                "energy": 3,
                "trust": 97,
                "status": "online"
            },

            "vision.local": {
                "type": "vision",
                "offline": True,
                "latency": 84,
                "energy": 4,
                "trust": 98,
                "status": "online"
            },

            "predictor.local": {
                "type": "prediction",
                "offline": True,
                "latency": 41,
                "energy": 2,
                "trust": 96,
                "status": "online"
            },

            "cloud.llm": {
                "type": "language",
                "offline": False,
                "latency": 310,
                "energy": 7,
                "trust": 94,
                "status": "standby"
            }
        }

    def available(self):

        return [
            {
                "id": model_id,
                **data
            }
            for model_id, data
            in self.models.items()
        ]

    def candidates(self, model_type: str):

        return [
            {
                "id": model_id,
                **data
            }

            for model_id, data
            in self.models.items()

            if data["type"] == model_type
            and data["status"] in [
                "online",
                "standby"
            ]
        ]

    def select(
        self,
        model_type: str,
        offline_required=False,
        low_energy=False
    ):

        candidates = self.candidates(
            model_type
        )

        if offline_required:

            candidates = [
                x for x in candidates
                if x["offline"]
            ]

        if not candidates:
            return None

        def score(model):

            score = model["trust"] * 2

            score -= model["latency"] * 0.1

            if low_energy:
                score -= model["energy"] * 5

            if model["status"] == "online":
                score += 10

            return score

        return max(
            candidates,
            key=score
        )


model_router = ModelRouter()
