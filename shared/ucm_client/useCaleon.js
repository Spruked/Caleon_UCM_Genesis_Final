// shared/ucm_client/useCaleon.js
import React, { useState, useEffect } from 'react';
import { CaleonClient } from './index.js';

const client = new CaleonClient();

export function useCaleon(sessionId) {
    const [session, setSession] = useState(sessionId);

    useEffect(() => {
        if (!session) {
            client.createSession().then(s => setSession(s.session_id));
        }
    }, []);

    async function ask(message) {
        return await client.ask(message, session);
    }

    return { ask, session };
}

export function CaleonBubble({ activated=true }) {
    const { ask } = useCaleon();
    const [messages, setMessages] = useState([]);

    async function sendMessage(msg) {
        setMessages(m => [...m, { role: "user", text: msg }]);
        const res = await ask(msg);
        setMessages(m => [...m, { role: "caleon", text: res.reply }]);
    }

    if (!activated) return null;

    return (
        <div className="cali-bubble">
            <div className="cali-chat-log">
                {messages.map((m,i) => (
                    <div key={i} className={m.role}>{m.text}</div>
                ))}
            </div>
            <CaliInput onSend={sendMessage} />
        </div>
    );
}

function CaliInput({ onSend }) {
    const [txt, setTxt] = useState("");
    return (
        <div className="cali-input">
            <input value={txt} onChange={e => setTxt(e.target.value)} />
            <button onClick={() => { onSend(txt); setTxt(""); }}>Send</button>
        </div>
    );
}