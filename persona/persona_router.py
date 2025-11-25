from persona.persona_bible import PERSONA_BIBLE
from persona.script_engine import ScriptEngine

class PersonaRouter:

    @staticmethod
    def scripted(category: str, key: str, **vars):
        text = ScriptEngine.get(category, key, **vars)
        if text:
            return {"type": "scripted", "reply": text}

        # fallback: persona bible fallback
        return {
            "type": "scripted",
            "reply": PERSONA_BIBLE["fallback_style"].get("offline", "...")
        }