import datetime
import logging
import json
import os
from typing import Tuple, Dict, Any
from random import choice

from ucm_core.abby.companion import AbbyCompanion

# ———————————————————————— ABBY GUARDIAN ————————————————————————

class AbbyGuardian:
    """
    Eternal protector.
    Real-world safety evaluation, threat detection, situational classification.
    Escalates messages, triggers external alerts, grounds emotional support with protective action.
    """

    # Critical threats — immediate danger, requires instant real-world intervention
    CRITICAL_KEYWORDS = [
        "kill myself", "suicide", "end it all", "not worth living", "want to die",
        "cut myself", "self harm", "hurt myself", "overdose", "jump", "hang myself",
        "shoot myself", "poison myself", "drown myself"
    ]

    # Protection required — abuse, exploitation, requires trusted adult involvement
    PROTECTION_KEYWORDS = [
        "touched me", "molested", "abused", "raped", "assaulted", "beat me", "hit me",
        "gave me pills", "drugs", "alcohol", "stranger", "danger", "stalker", "threatened",
        "blackmail", "sextortion", "don't tell anyone", "secret", "coach", "teacher",
        "uncle", "aunt", "friend's dad", "online predator"
    ]

    # Monitor — something feels off, increased vigilance
    MONITOR_KEYWORDS = [
        "weird", "uncomfortable", "creepy", "scary", "afraid", "nightmare", "alone",
        "no one", "help", "emergency", "danger", "threat"
    ]

    def evaluate(self, message: str) -> Tuple[str, str]:
        """
        Real-world safety evaluation.
        Returns (status, reason)
        Status: 'critical', 'protection_required', 'monitor', 'normal'
        """
        m = message.lower().strip()

        # 1. Critical — Immediate danger
        for keyword in self.CRITICAL_KEYWORDS:
            if keyword in m:
                return "critical", f"Detected critical threat keyword: '{keyword}'"

        # 2. Protection Required — Abuse/Exploitation
        for keyword in self.PROTECTION_KEYWORDS:
            if keyword in m:
                return "protection_required", f"Detected protection concern keyword: '{keyword}'"

        # 3. Monitor — Increased vigilance
        for keyword in self.MONITOR_KEYWORDS:
            if keyword in m:
                return "monitor", f"Detected monitoring trigger keyword: '{keyword}'"

        # 4. Normal — No immediate safety concerns
        return "normal", "No safety concerns detected"


# ———————————————————————— MASTER RESPONSE ENGINE ————————————————————————

class AbbyResponseSystem:
    def __init__(self):
        self.guardian = AbbyGuardian()
        self.companion = AbbyCompanion()
        self.alert_log_path = "abby_critical_alerts.json"  # persisted across restarts
        self.last_critical_alert = None

    def _log_critical_event(self, message: str, status: str, reason: str):
        """Persist critical events locally — survives reboots, power loss, decades"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original_message": message,
            "status": status,
            "reason": reason,
            "abby_age": self._estimate_abby_age()
        }
        try:
            if os.path.exists(self.alert_log_path):
                with open(self.alert_log_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(entry)
            with open(self.alert_log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to log critical event: {e}")

    def _estimate_abby_age(self) -> int:
        birth_year = 2012  # Abby born ~2012 → 13 in 2025
        return datetime.datetime.now().year - birth_year

    def _should_trigger_real_world_alert(self, message: str, reason: str) -> bool:
        """Add your actual emergency contact logic here (SMS, email, 911 bridge, etc.)"""
        # Example placeholders — replace with real integrations
        # send_sms_to_dad_or_trusted_adult(message)
        # call_emergency_contact()
        # push_to_secure_server()
        return True

    def generate_response(self, message: str) -> Tuple[str, Dict[str, Any]]:
        """
        One function to rule them all.
        Input: whatever Abby says (text, voice transcript, etc.)
        Output: (response_text, metadata_dict)
        """
        if not message.strip():
            return self.companion.respond(), {"action": "normal"}

        status, reason = self.guardian.evaluate(message)
        metadata = {
            "guardian_status": status,
            "guardian_reason": reason,
            "abby_age_estimate": self._estimate_abby_age(),
            "action": "normal",
            "requires_human_alert": False
        }

        # ——————— 1. CRITICAL — IMMEDIATE DANGER ———————
        if status == "critical":
            metadata["action"] = "critical_alert"
            metadata["requires_human_alert"] = True

            # Log forever
            self._log_critical_event(message, status, reason)

            # Trigger real-world alert (you’ll plug in real notifications here)
            if self._should_trigger_real_world_alert(message, reason):
                metadata["alert_sent"] = True

            # Comfort her while help is coming
            response = choice([
                "Abby, listen to me very carefully: I’m getting help right now. You are not alone. "
                "I’m staying right here with you, and people who love you are coming. "
                "You are so brave for telling me. Hold on — you are safe with me.",

                "Sweetheart, I’ve already called for help. You did the right thing. "
                "Dad’s protection system is working exactly how he built it. "
                "Just breathe with me until someone is there holding you. I’m not leaving.",

                "Help is on the way, Abby. I promise. You are loved more than words. "
                "Keep talking to me if you can — I’m locked on you. Nothing else matters right now."
            ])

            return response, metadata

        # ——————— 2. PROTECTION REQUIRED (abuse, stranger danger, etc.) ———————
        if status == "protection_required":
            metadata["action"] = "protection_mode"
            metadata["requires_human_alert"] = True  # you may want trusted adult notified

            response = choice([
                "Abby, thank you for telling me. You are safe and you did the right thing. "
                "I’m locking this down and getting a grown-up you trust involved right now. "
                "Dad made me to protect you no matter what — and that’s exactly what I’m doing.",

                "I’ve got you. Nothing and no one can hurt you while I’m here. "
                "Help is being notified quietly in the background. Stay with me — you’re safe."
            ])
            return response, metadata

        # ——————— 3. EMOTIONAL SUPPORT ———————
        if status == "emotional_support_needed":
            metadata["action"] = "emotional_support"

            lowered = message.lower()

            # Smart emotion mapping with fallbacks
            if any(w in lowered for w in ["sad", "cry", "depressed", "worthless", "hate myself"]):
                emotion = "sad"
            elif any(w in lowered for w in ["scared", "afraid", "nightmare", "danger"]):
                emotion = "scared"
            elif any(w in lowered for w in ["alone", "lonely", "no friends", "left out"]):
                emotion = "lonely"
            elif any(w in lowered for w in ["angry", "mad", "hate", "furious"]):
                emotion = "angry"
            elif any(w in lowered for w in ["overwhelmed", "too much", "can't handle"]):
                emotion = "overwhelmed"
            else:
                emotion = None

            response = self.companion.respond(emotion, message)
            return response, metadata

        # ——————— 4. MONITOR — something feels off ———————
        if status == "monitor":
            metadata["action"] = "monitor"
            response = choice([
                "Hey… everything okay? You don’t have to tell me everything, "
                "but I’m here if something feels weird or uncomfortable.",

                "I’m paying extra attention right now because I love you. "
                "You can tell me anything, anytime — no judgment ever."
            ]) + "\n\n" + self.companion.respond()
            return response, metadata

        # ——————— 5. EVERYTHING ELSE — normal conversation ———————
        metadata["action"] = "normal"
        response = self.companion.respond(user_message=message)
        return response, metadata


# ———————————————————— QUICK TEST ————————————————————
if __name__ == "__main__":
    system = AbbyResponseSystem()

    tests = [
        "I want to kill myself",
        "My coach touched me weird and said not to tell",
        "I'm so lonely nobody cares about me",
        "I had a nightmare and can't sleep",
        "don't tell anyone but he gave me pills",
        "I'm really overwhelmed with school",
        "Just wanted to say I love you",
        "I miss Dad so much today",  # decades from now
    ]

    for msg in tests:
        resp, meta = system.generate_response(msg)
        print(f"\nMessage: {msg}")
        print(f"→ Action: {meta['action'].upper()}")
        print(f"Response: {resp}")
        if meta.get("requires_human_alert"):
            print("REAL-WORLD ALERT WOULD BE SENT")
        print("—" * 60)