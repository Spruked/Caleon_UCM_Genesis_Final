/**
 * React App Integration with UCM
 * Example of how a React app connects to Caleon
 */

import React, { useState, useEffect } from 'react';
import { useCaleon, CaleonBubble } from '../shared/ucm_client/useCaleon.js';

function App() {
    const { ask, createSession, loading } = useCaleon();
    const [sessionId, setSessionId] = useState(null);
    const [message, setMessage] = useState('');
    const [responses, setResponses] = useState([]);

    useEffect(() => {
        // Initialize session on app load
        const initSession = async () => {
            try {
                const session = await createSession();
                setSessionId(session.session_id);
            } catch (error) {
                console.error('Failed to create session:', error);
            }
        };
        initSession();
    }, [createSession]);

    const handleAsk = async () => {
        if (!message.trim() || !sessionId) return;

        try {
            const response = await ask(message, { sessionId });
            setResponses(prev => [...prev, {
                type: 'user',
                content: message
            }, {
                type: 'caleon',
                content: response.reply
            }]);
            setMessage('');
        } catch (error) {
            setResponses(prev => [...prev, {
                type: 'error',
                content: error.message
            }]);
        }
    };

    return (
        <div className="app">
            <h1>My App with Caleon</h1>

            {/* Caleon Bubble Component */}
            <CaleonBubble
                activated={true}
                sessionId={sessionId}
                user="react_user"
                className="my-custom-bubble"
            />

            {/* Custom Caleon Interface */}
            <div className="caleon-chat">
                <div className="messages">
                    {responses.map((response, index) => (
                        <div key={index} className={`message ${response.type}`}>
                            <strong>{response.type === 'caleon' ? 'Caleon:' : 'You:'}</strong>
                            {response.content}
                        </div>
                    ))}
                </div>

                <div className="input-area">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
                        placeholder="Ask Caleon anything..."
                        disabled={loading || !sessionId}
                    />
                    <button onClick={handleAsk} disabled={loading || !sessionId}>
                        {loading ? 'Thinking...' : 'Ask Caleon'}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;

/**
 * Usage in any React app:
 *
 * 1. Copy shared/ucm_client/ to your project
 * 2. Import useCaleon hook
 * 3. Use CaleonBubble component or build custom interface
 * 4. Start asking Caleon questions!
 *
 * The same Caleon instance serves all your apps.
 */