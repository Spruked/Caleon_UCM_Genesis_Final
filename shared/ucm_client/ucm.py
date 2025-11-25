# shared/ucm_client/ucm.py
import requests

class CaleonClient:
    def __init__(self, remote=None):
        self.endpoints = [
            "http://localhost:8000",
            "http://ucm:8000",
        ]
        if remote:
            self.endpoints.append(remote)

        self.base = None

    def _detect(self):
        for url in self.endpoints:
            try:
                r = requests.get(url + "/api/health", timeout=0.3)
                if r.status_code == 200:
                    self.base = url
                    return
            except:
                pass
        raise RuntimeError("UCM not reachable")

    def _ensure(self):
        if not self.base:
            self._detect()

    def ask(self, message, session_id=None):
        self._ensure()
        payload = {"message": message, "session_id": session_id}
        r = requests.post(self.base + "/api/bubble/ask", json=payload)
        return r.json()

    def create_session(self):
        self._ensure()
        return requests.post(self.base + "/api/bubble/session/create").json()

    def learn(self, fact):
        self._ensure()
        requests.post(self.base + "/api/bubble/learn", json={"fact": fact})