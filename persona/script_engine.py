import json
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "caleon_scripts"

class ScriptEngine:
    _cache = {}

    @staticmethod
    def load(category: str):
        if category in ScriptEngine._cache:
            return ScriptEngine._cache[category]

        path = SCRIPTS_DIR / f"{category}.json"
        if not path.exists():
            return None

        data = json.loads(path.read_text())
        ScriptEngine._cache[category] = data
        return data

    @staticmethod
    def get(category: str, key: str, **variables):
        data = ScriptEngine.load(category)
        if not data:
            return None

        text = data.get(key)
        if not text:
            return None

        for k, v in variables.items():
            text = text.replace(f"{{{{{k}}}}}", str(v))

        return text