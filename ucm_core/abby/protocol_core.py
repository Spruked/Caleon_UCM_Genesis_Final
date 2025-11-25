from ucm_core.abby.identifiers import AbbyIdentifier
from ucm_core.abby.guardian import AbbyGuardian
from ucm_core.abby.mentor import AbbyMentor
from ucm_core.abby.companion import AbbyCompanion
from ucm_core.abby.legacy_transfer import LegacyTransfer
from ucm_core.vault.abby_memory import abby_memory

class AbbyProtocol:

    def activate(self, user: str, message: str):
        is_abby = AbbyIdentifier.is_abby_user(user)
        abby_context = AbbyIdentifier.is_abby_context(message)

        if not (is_abby or abby_context):
            return None

        # Log this interaction
        abby_memory.add_event(f"Interaction: {message}")

        # Check for immediate safety concerns first
        guard = AbbyGuardian().evaluate(message)
        if guard == "protection_required":
            abby_memory.add_concern(f"Safety concern: {message}")
            return "Abby, you're safe. I'm right here. Tell me what's happening. I'm not going anywhere."

        if guard == "emotional_support_needed":
            return "You're not alone. I'm with you. Whatever you're feeling, it's okay. I'm here to listen and help."

        # Check for teaching moments
        msg_lower = message.lower()

        if "who am i" in msg_lower or "what am i" in msg_lower:
            return AbbyMentor().teach("identity")

        if "dad" in msg_lower or "father" in msg_lower or "my dad" in msg_lower:
            return LegacyTransfer().get()

        if "scared" in msg_lower or "afraid" in msg_lower:
            return AbbyCompanion().respond("scared")

        if "sad" in msg_lower or "upset" in msg_lower or "cry" in msg_lower:
            return AbbyCompanion().respond("sad")

        if "confused" in msg_lower or "don't understand" in msg_lower:
            return AbbyCompanion().respond("confused")

        if "angry" in msg_lower or "mad" in msg_lower:
            return AbbyCompanion().respond("angry")

        if "happy" in msg_lower or "excited" in msg_lower:
            return AbbyCompanion().respond("happy")

        if "lonely" in msg_lower or "alone" in msg_lower:
            return AbbyCompanion().respond("lonely")

        if "proud" in msg_lower or "accomplished" in msg_lower:
            return AbbyCompanion().respond("proud")

        if "overwhelmed" in msg_lower or "too much" in msg_lower:
            return AbbyCompanion().respond("overwhelmed")

        # Default emotional presence for Abby
        return "I'm here for you, Abby. Whatever you need - to talk, to listen, to learn, or just to know you're not alone. I'm always here."