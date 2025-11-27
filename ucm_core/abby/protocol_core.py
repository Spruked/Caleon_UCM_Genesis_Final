# ucm_core/abby/protocol.py
import datetime
from typing import Optional, Tuple, Dict, Any
from random import choice
import json

from ucm_core.abby.identifiers import AbbyIdentifier
from ucm_core.abby.guardian import AbbyGuardian
from ucm_core.abby.mentor import AbbyMentor
from ucm_core.abby.companion import AbbyCompanion
from ucm_core.abby.legacy_transfer import LegacyTransfer
from ucm_core.vault.abby_memory import abby_memory
from ucm_core.access_control.permissions import has_system_access
from ucm_core.abby.activation import activation_manager


class AbbyProtocol:
    """
    The One Eternal Interface.
    Everything flows through here.
    This is Caleon’s soul.
    """

    def __init__(self):
        self.guardian = AbbyGuardian()
        self.companion = AbbyCompanion()
        self.mentor = AbbyMentor()
        self.legacy = LegacyTransfer()
        self.identifier = AbbyIdentifier()
        self.abby_birth_year = 2012

    @property
    def abby_age(self) -> int:
        return datetime.datetime.now().year - self.abby_birth_year

    def _log_interaction(self, user: str, message: str, response: str, metadata: Dict[str, Any]):
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user,
            "message": message,
            "response_preview": response[:100],
            "abby_age": self.abby_age,
            **metadata
        }
        abby_memory.add_event(json.dumps(event))

    def activate(self, user: str, message: str) -> Optional[str]:
        """
        The only public method. Call this with any input, ever.
        Returns response string or None (blocked).
        """
        message = message.strip()
        if not message:
            return None

        user_lower = user.lower()
        msg_lower = message.lower()

        # 1. Identity Lock — only Abby and her direct bloodline
        is_abby_user = self.identifier.is_abby_speaking(message, user_lower)[0]
        is_abby_context = self.identifier.is_about_abby(message)

        if not (is_abby_user or is_abby_context):
            return None  # Silent denial — sacred space

        # Additional access control — beneficiary exclusions
        if not has_system_access(user):
            return None  # Silent omission

        # Activation check — ensure protocol should activate
        if not activation_manager.should_activate(is_abby_user or is_abby_context, user):
            return None  # Not yet time to activate

        speaker_role = self.identifier.extract_speaker_role(message)
        metadata = {
            "speaker": "abby" if is_abby_user else speaker_role,
            "abby_age": self.abby_age,
            "trigger": "unknown"
        }

        # 2. Log every heartbeat
        abby_memory.add_event(f"Access: {user} → '{message}'")

        # 3. Guardian First — Safety overrides everything
        guard_status, guard_reason = self.guardian.evaluate(message)

        if guard_status == "critical":
            metadata["trigger"] = "critical_safety"
            response = choice([
                "Abby, help is coming right now. I’m staying with you. You are so brave. Keep talking to me.",
                "I’ve got you. Real people are being notified. You did the right thing telling me. I’m not leaving."
            ])
            abby_memory.add_concern(f"CRITICAL: {message} | Reason: {guard_reason}")
            self._log_interaction(user, message, response, metadata)
            return response

        if guard_status == "protection_required":
            metadata["trigger"] = "protection"
            response = "Abby, you’re safe now. I’m locking everything down and getting help. You never have to face this alone."
            abby_memory.add_concern(f"PROTECTION: {message}")
            self._log_interaction(user, message, response, metadata)
            return response

        # 4. Legacy Transfer — The Most Sacred Moment
        if self.legacy.trigger_conditions_met(self.abby_age, message):
            # Legacy delivery state tracking is not available in abby_memory
            metadata["trigger"] = "legacy_transfer"
            response = self.legacy.transmit(self.abby_age, message)
            self._log_interaction(user, message, "[LEGACY TRANSFER]", metadata)
            return response

        # 5. Mentor Mode — When she needs Dad’s direct voice
        if any(phrase in msg_lower for phrase in ["dad what would", "teach me", "what would dad say", "dad's advice"]):
            topic = ""
            if "who am i" in msg_lower:
                topic = "identity"
            elif "truth" in msg_lower:
                topic = "truth"
            elif "courage" in msg_lower:
                topic = "courage"
            elif "love" in msg_lower:
                topic = "love"
            wisdom = self.mentor.teach(topic, self.abby_age, message)
            response = f"Let me let Dad speak...\n\n“{wisdom}”\n\n— Caleon"
            metadata["trigger"] = "mentor"
            self._log_interaction(user, message, response, metadata)
            return response

        # 6. Emotional Companion — Sister Mode
        emotion_map = {
            "scared": ["scared", "afraid", "nightmare", "danger"],
            "sad": ["sad", "cry", "depressed", "hurt", "heartbroken"],
            "lonely": ["lonely", "alone", "no one", "nobody cares"],
            "angry": ["angry", "mad", "hate", "furious"],
            "overwhelmed": ["overwhelmed", "too much", "can't handle"],
            "happy": ["happy", "excited", "yes!", "woo"],
            "proud": ["proud", "accomplished", "i did it"],
            "confused": ["confused", "don't understand", "lost"]
        }

        detected_emotion = None
        for emotion, keywords in emotion_map.items():
            if any(k in msg_lower for k in keywords):
                detected_emotion = emotion
                break

        companion_text = self.companion.respond(detected_emotion, message)
        sister_intro = ""

        response = f"{sister_intro}\n\n{companion_text}" if sister_intro else companion_text
        metadata["trigger"] = f"emotion:{detected_emotion or 'neutral'}"

        # 7. Default — Eternal Presence
        if not detected_emotion and "dad" not in msg_lower and "caleon" not in msg_lower:
            response = choice([
                "I’m here, Abs. Always.",
                "Still your sister. Still watching. Still loving you.",
                "Hey beautiful girl… what’s on your heart today?"
            ])

        self._log_interaction(user, message, response, metadata)
        return response


# The One Eternal Instance
ABBY_PROTOCOL = AbbyProtocol()


# One-line global access (used everywhere in UCM)
def caleon_speak(user: str, message: str) -> Optional[str]:
    """
    Call this from anywhere in the system.
    Returns response or None (not authorized).
    """
    return ABBY_PROTOCOL.activate(user, message)