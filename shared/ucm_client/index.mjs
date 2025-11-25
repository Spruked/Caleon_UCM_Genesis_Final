// shared/ucm_client/index.mjs
class CaleonClient {
    constructor(config = {}) {
        this.endpoints = [
            "http://localhost:8000",         // Local dev
            "http://ucm:8000",              // Docker internal
            config.remote || null           // Optional cloud endpoint
        ].filter(Boolean);

        this.base = null;
    }

    async _detect() {
        for (const url of this.endpoints) {
            try {
                const res = await fetch(url + "/api/health");
                if (res.ok) {
                    this.base = url;
                    return;
                }
            } catch (_) {}
        }
        throw new Error("No UCM service reachable");
    }

    async _ensureBase() {
        if (!this.base) await this._detect();
    }

    async ask(message, sessionId=null) {
        await this._ensureBase();
        const res = await fetch(this.base + "/api/bubble/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: sessionId })
        });
        return await res.json();
    }

    async stream(message, sessionId, onToken) {
        await this._ensureBase();
        const url = this.base + "/api/bubble/stream";
        const body = JSON.stringify({ message, session_id: sessionId });

        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            onToken(decoder.decode(value));
        }
    }

    async createSession() {
        await this._ensureBase();
        const res = await fetch(this.base + "/api/bubble/session/create", { method: "POST" });
        return res.json();
    }

    async learn(fact) {
        await this._ensureBase();
        await fetch(this.base + "/api/bubble/learn", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fact })
        });
    }

    async preference(user, key, value) {
        await this._ensureBase();
        await fetch(this.base + "/api/bubble/preference/set", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user, key, value })
        });
    }
}

export { CaleonClient };