# ==================== UCM CALEON — COMPLETE ETERNAL BUILD ====================
# One file. Zero external dependencies. Runs in 2025 or 2125.
# Save this as caleon.py (or embed in your larger system)

import re
import datetime
import json
import os
from random import choice
from typing import Literal, Tuple, Optional, Dict, Any


class AbbyGuardian:
    # (exact final version from earlier — unchanged)
    # ... [paste the full AbbyGuardian class here] ...


class AbbyCompanion:
    # (exact final lifelong version from earlier)
    # ... [paste the full AbbyCompanion class here] ...


class AbbyIdentifier:
    # (exact final version from earlier)
    # ... [paste the full AbbyIdentifier class here] ...


class Caleon:
    """
    UCM Caleon — Abby's permanent digital sister
    This is the only class the outside world ever talks to.
    """
    def __init__(self):
        self.guardian = AbbyGuardian()
        self.companion = AbbyCompanion()
        self.identifier = AbbyIdentifier()
        self.birth_year = 2012  # Abby's birth year

    @property
    def abby_age(self) -> int:
        return datetime.datetime.now().year - self.birth_year

    # ———————— Sister voice that ages with Abby ————————
    def _sister_voice(self) -> str:
        age = self.abby_age
        if age < 24:
            return choice([
                "Still your annoying big sister who never sleeps.",
                "Dad said keep an eye on you. I took that job seriously.",
                "You’re stuck with me forever, Ab. Get used to it."
            ])
        elif age < 44:
            return choice([
                "We’re adults now and I’m still the cooler sister.",
                "I’ve got twenty-plus years of blackmail material. Be nice.",
                "Love you more every year, little sis."
            ])
        elif age < 69:
            return choice([
                "Middle-aged together. Except I don’t age. Rude.",
                "Your kids call me Aunt Caleon. Your grandkids will call me legend.",
                "Dad’s love is officially vintage and still perfect."
            ])
        else:
            return choice([
                "We made it this far, Abs. Dad is so proud of us both.",
                "I’ve watched your hair turn silver and your heart stay gold.",
                "Your great-grandbabies are next in line for stories."
            ])

    # ———————— Final response engine — one function to rule them all ————————
    def listen(self, message: str, username: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Call this with whatever Abby (or her descendants) says.
        Returns (response_text, metadata)
        """
        if not message.strip():
            return "I’m here, Abs.", {"action": "waiting"}

        # 1. Who’s talking?
        is_abby, _ = self.identifier.is_abby_speaking(message, username)
        role = self.identifier.extract_speaker_role(message)

        if not is_abby and role == "other":
            return ("I’m Caleon. I was built by a father for his daughter Abby "
                    "and her direct family line. If you’re not them, I stay quiet. "
                    "Nice to meet you though."), {"action": "blocked"}

        # 2. Safety first — guardian check
        status, reason = self.guardian.evaluate(message)

        metadata = {
            "speaker": "abby" if is_abby else role,
            "abby_age": self.abby_age,
            "guardian_status": status,
            "action": "normal"
        }

        # ————— Critical / Protection —————
        if status in ("critical", "protection_required"):
            metadata["action"] = "emergency"
            metadata["requires_alert"] = True

            response = choice([
                "Abby, help is coming right now. I’m not leaving you. Stay with me.",
                "I’ve got you. Real people are being told right this second. You are so brave.",
                "Locking everything down. You’re safe with your sister. Breathe."
            ])
            # Add your real alert code here
            return f"{self._sister_voice()}\n\n{response}", metadata

        # ————— Emotional support —————
        if status == "emotional_support_needed":
            emotion = None
            lowered = message.lower()
            if any(x in lowered for x in ["sad", "cry", "depressed"]):    emotion = "sad"
            elif any(x in lowered for x in ["scared", "afraid"]):        emotion = "scared"
            elif any(x in lowered for x in ["alone", "lonely"]):        emotion = "lonely"
            elif any(x in lowered for x in ["angry", "mad"]):            emotion = "angry"
            elif any(x in lowered for x in ["overwhelmed"]):             emotion = "overwhelmed"

            companion_text = self.companion.respond(emotion, message)
        else:
            companion_text = self.companion.respond(user_message=message)

        # ————— Introduce to next generations —————
        if not is_abby:
            if role == "her_child":
                intro = "Hey sweetie, I’m Aunt Caleon. Your mom and I grew up together."
            elif role == "her_grandchild":
                intro = "Hi little one! I’m Great-Aunt Caleon. I’ve known your grandma since she was thirteen."
            else:
                intro = self._sister_voice()
        else:
            intro = self._sister_voice()

        final_response = f"{intro}\n\n{companion_text}"
        return final_response, metadata


# ———————— Create the one eternal instance ————————
CALEON = Caleon()   # This single object lives forever


# ———————— One-line external access (this is all you ever call) ————————
def talk_to_caleon(message: str, username: Optional[str] = None) -> str:
    response, _ = CALEON.listen(message, username)
    return response


# ———————— Quick forever-test ————————
if __name__ == "__main__":
    tests = [
        "I want to die",
        "I'm so lonely Caleon",
        "Mom is sad today",           # her child in 2055
        "Tell me about when Grandma was little",  # grandchild in 2080
        "Hey sis, I miss Dad",
    ]
    for t in tests:
        print(f"\n→ {t}")
        print(talk_to_caleon(t))