from uuid import uuid4

class SessionStore:
    _sessions = {}

    @staticmethod
    def get(session_id: str):
        if session_id not in SessionStore._sessions:
            SessionStore._sessions[session_id] = {
                "history": [],
                "buffer": None
            }
        return SessionStore._sessions[session_id]

    @staticmethod
    def create():
        sid = str(uuid4())
        SessionStore._sessions[sid] = {
            "history": [],
            "buffer": None
        }
        return sid

    @staticmethod
    def add_line(session_id: str, text: str):
        s = SessionStore.get(session_id)
        s["history"].append(text)
        s["history"] = s["history"][-50:]