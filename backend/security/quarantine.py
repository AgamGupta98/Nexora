class QuarantineEngine:

    def __init__(self):

        self.quarantined = set()

    def isolate(self, device_id):

        self.quarantined.add(
            device_id
        )

        return {
            "device": device_id,
            "status": "QUARANTINED"
        }

    def is_isolated(self, device_id):

        return device_id in self.quarantined

    def release(self, device_id):

        self.quarantined.discard(
            device_id
        )

        return {
            "device": device_id,
            "status": "RELEASED"
        }


quarantine_engine = QuarantineEngine()
