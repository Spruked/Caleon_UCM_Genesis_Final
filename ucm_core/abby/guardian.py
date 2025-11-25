class AbbyGuardian:
    def evaluate(self, message: str):
        m = message.lower()

        if "hurt" in m or "scared" in m or "danger" in m:
            return "protection_required"

        if "alone" in m or "lost" in m:
            return "emotional_support_needed"

        return "ok"